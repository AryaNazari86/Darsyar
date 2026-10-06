#!/bin/bash
# Pull a full Darsyar backup from the production server to this Mac.
#
# Runs FROM the Mac (the server cannot reach a laptop behind NAT) and writes
# nothing on the server: pg_dump streams to stdout over SSH.
#
# Produces three artifacts per run, all small:
#   db.dump      pg_dump custom format  - the canonical restore artifact
#   db.sql.gz    plain SQL, gzipped     - greppable, restorable with just psql
#   csv/*.csv    the user-side tables   - readable, survives schema drift
#
# Scheduled by ~/Library/LaunchAgents/net.darsyar.backup.plist (1st and 15th).
# Notification config (optional): $DEST/.notify with BALE_TOKEN and BALE_CHAT_ID.

set -uo pipefail

SSH_HOST="${DARSYAR_HOST:-root@87.248.156.117}"
SSH_PORT="${DARSYAR_PORT:-9011}"
DB="darsyardb"
DEST="$HOME/Darsyar-Backups"
KEEP=12                      # ~6 months at one run per fortnight

STAMP="$(date +%Y%m%d-%H%M)"
RUN="$DEST/$STAMP"
LOG="$DEST/backup.log"

mkdir -p "$RUN/csv"
exec 3>&1                    # keep a handle to the real stdout for progress
log() { printf '%s  %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" | tee -a "$LOG" >&3; }

SSH=(ssh -p "$SSH_PORT" -o BatchMode=yes -o ConnectTimeout=20 "$SSH_HOST")
fail() { log "FAILED: $*"; notify "❌ Darsyar backup FAILED%0A$*"; exit 1; }

notify() {
    # Best-effort only; never let a notification problem fail the backup.
    [ -f "$DEST/.notify" ] || return 0
    # shellcheck disable=SC1090
    . "$DEST/.notify" 2>/dev/null || return 0
    [ -n "${BALE_TOKEN:-}" ] && [ -n "${BALE_CHAT_ID:-}" ] || return 0
    curl -sS -m 20 -o /dev/null \
        --data-urlencode "chat_id=$BALE_CHAT_ID" \
        --data-urlencode "text=$(printf '%b' "${1//%0A/\\n}")" \
        "https://tapi.bale.ai/bot$BALE_TOKEN/sendMessage" || true
}

log "=== backup $STAMP -> $RUN ==="

"${SSH[@]}" true 2>/dev/null || fail "cannot reach $SSH_HOST:$SSH_PORT over SSH"

# 1. canonical custom-format dump
log "pg_dump (custom format)..."
"${SSH[@]}" "sudo -u postgres pg_dump -Fc $DB" > "$RUN/db.dump" 2>"$RUN/.err" \
    || fail "pg_dump -Fc failed: $(head -c 300 "$RUN/.err")"

# 2. plain SQL, for grep-ability and psql-only restores
log "pg_dump (plain SQL, gzipped)..."
"${SSH[@]}" "sudo -u postgres pg_dump $DB | gzip -9" > "$RUN/db.sql.gz" 2>"$RUN/.err" \
    || fail "plain pg_dump failed: $(head -c 300 "$RUN/.err")"

# 3. the irreplaceable tables as CSV
for t in user_user user_userquestionrel bot_log content_notepackage \
         content_notepackage_upvotes content_notepackage_downvotes auth_user; do
    "${SSH[@]}" "sudo -u postgres psql -d $DB -c \"\\copy (select * from $t) to stdout with csv header\"" \
        > "$RUN/csv/$t.csv" 2>>"$RUN/.err" || log "WARN: csv export failed for $t"
done

# 4. secrets that exist nowhere else (not in git, by design)
"${SSH[@]}" "cat /opt/darsyar/.env" > "$RUN/env.txt" 2>>"$RUN/.err" \
    && chmod 600 "$RUN/env.txt" || log "WARN: could not fetch /opt/darsyar/.env"

rm -f "$RUN/.err"

# ---- verify, without needing postgres client tools locally ----
[ -s "$RUN/db.dump" ] || fail "db.dump is empty"
[ "$(head -c 5 "$RUN/db.dump")" = "PGDMP" ] || fail "db.dump is not a valid pg_dump archive"
gzip -t "$RUN/db.sql.gz" 2>/dev/null || fail "db.sql.gz is corrupt"
gzip -cd "$RUN/db.sql.gz" | grep -q 'COPY public.user_user' \
    || fail "db.sql.gz has no user_user data - wrong database?"

USERS=$(( $(wc -l < "$RUN/csv/user_user.csv") - 1 ))
QUESTIONS=$(gzip -cd "$RUN/db.sql.gz" | grep -c '^INSERT INTO public.content_question' || true)
[ "$USERS" -ge 0 ] || fail "could not count users"

SIZE=$(du -sh "$RUN" | cut -f1)
{
    echo "darsyar backup $STAMP"
    echo "host:      $SSH_HOST:$SSH_PORT"
    echo "database:  $DB"
    echo "users:     $USERS"
    echo "size:      $SIZE"
    echo
    echo "sha256:"
    ( cd "$RUN" && shasum -a 256 db.dump db.sql.gz csv/*.csv 2>/dev/null )
} > "$RUN/MANIFEST.txt"

log "OK  users=$USERS  size=$SIZE"

# ---- prune, keeping the newest $KEEP runs ----
PRUNED=0
while IFS= read -r old; do
    rm -rf "$old" && PRUNED=$((PRUNED + 1))
done < <(find "$DEST" -maxdepth 1 -type d -name '20*-*' | sort -r | tail -n +$((KEEP + 1)))
[ "$PRUNED" -gt 0 ] && log "pruned $PRUNED old backup(s), keeping $KEEP"

notify "✅ Darsyar backup OK%0Ausers: $USERS%0Asize: $SIZE%0A$STAMP"
log "=== done ==="
