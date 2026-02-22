import json
from datetime import date, timedelta

from django.core.cache import cache
from django.db.models import Count, Q
from django.db.models.functions import ExtractHour, TruncDay, TruncHour, TruncMonth
from django.shortcuts import render
from django.utils import timezone

from bot.models import LOG
from user.models import User


LOG_TYPE_LABELS = {
    0: "Question",
    1: "Test",
    2: "AI",
    3: "Hint",
    4: "Note",
}
LOG_TYPE_COLORS = {
    0: "#0B84F3",
    1: "#FF8A00",
    2: "#17B26A",
    3: "#F04438",
    4: "#7A5AF8",
}
EN_MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _percent_change(current, previous):
    if previous == 0:
        return 0 if current == 0 else 100
    return round(((current - previous) / previous) * 100, 1)


def _logs_window_metrics(now_dt):
    hour_start = now_dt - timedelta(hours=1)
    hour_prev = hour_start - timedelta(hours=1)
    day_start = now_dt - timedelta(days=1)
    day_prev = day_start - timedelta(days=1)
    month_start = now_dt - timedelta(days=30)
    month_prev = month_start - timedelta(days=30)
    year_start = now_dt - timedelta(days=365)
    year_prev = year_start - timedelta(days=365)

    agg = LOG.objects.aggregate(
        hour_current=Count("id", filter=Q(date_created__gte=hour_start)),
        hour_previous=Count("id", filter=Q(date_created__gte=hour_prev, date_created__lt=hour_start)),
        day_current=Count("id", filter=Q(date_created__gte=day_start)),
        day_previous=Count("id", filter=Q(date_created__gte=day_prev, date_created__lt=day_start)),
        month_current=Count("id", filter=Q(date_created__gte=month_start)),
        month_previous=Count("id", filter=Q(date_created__gte=month_prev, date_created__lt=month_start)),
        year_current=Count("id", filter=Q(date_created__gte=year_start)),
        year_previous=Count("id", filter=Q(date_created__gte=year_prev, date_created__lt=year_start)),
    )

    return {
        "hour": {
            "current": agg["hour_current"],
            "previous": agg["hour_previous"],
            "change": _percent_change(agg["hour_current"], agg["hour_previous"]),
        },
        "day": {
            "current": agg["day_current"],
            "previous": agg["day_previous"],
            "change": _percent_change(agg["day_current"], agg["day_previous"]),
        },
        "month": {
            "current": agg["month_current"],
            "previous": agg["month_previous"],
            "change": _percent_change(agg["month_current"], agg["month_previous"]),
        },
        "year": {
            "current": agg["year_current"],
            "previous": agg["year_previous"],
            "change": _percent_change(agg["year_current"], agg["year_previous"]),
        },
    }


def _users_window_metrics(now_dt):
    hour_start = now_dt - timedelta(hours=1)
    hour_prev = hour_start - timedelta(hours=1)
    day_start = now_dt - timedelta(days=1)
    day_prev = day_start - timedelta(days=1)
    month_start = now_dt - timedelta(days=30)
    month_prev = month_start - timedelta(days=30)
    year_start = now_dt - timedelta(days=365)
    year_prev = year_start - timedelta(days=365)

    agg = User.objects.aggregate(
        hour_current=Count("id", filter=Q(date_created__gte=hour_start)),
        hour_previous=Count("id", filter=Q(date_created__gte=hour_prev, date_created__lt=hour_start)),
        day_current=Count("id", filter=Q(date_created__gte=day_start)),
        day_previous=Count("id", filter=Q(date_created__gte=day_prev, date_created__lt=day_start)),
        month_current=Count("id", filter=Q(date_created__gte=month_start)),
        month_previous=Count("id", filter=Q(date_created__gte=month_prev, date_created__lt=month_start)),
        year_current=Count("id", filter=Q(date_created__gte=year_start)),
        year_previous=Count("id", filter=Q(date_created__gte=year_prev, date_created__lt=year_start)),
    )

    return {
        "hour": {
            "current": agg["hour_current"],
            "previous": agg["hour_previous"],
            "change": _percent_change(agg["hour_current"], agg["hour_previous"]),
        },
        "day": {
            "current": agg["day_current"],
            "previous": agg["day_previous"],
            "change": _percent_change(agg["day_current"], agg["day_previous"]),
        },
        "month": {
            "current": agg["month_current"],
            "previous": agg["month_previous"],
            "change": _percent_change(agg["month_current"], agg["month_previous"]),
        },
        "year": {
            "current": agg["year_current"],
            "previous": agg["year_previous"],
            "change": _percent_change(agg["year_current"], agg["year_previous"]),
        },
    }


def _month_shift(first_day, offset):
    month_index = (first_day.month - 1) + offset
    year = first_day.year + month_index // 12
    month = (month_index % 12) + 1
    return date(year, month, 1)


def _hourly_logs_data(now_dt):
    end_hour = now_dt.replace(minute=0, second=0, microsecond=0)
    points = [end_hour - timedelta(hours=i) for i in reversed(range(24))]
    start_hour = points[0]

    raw = (
        LOG.objects.filter(date_created__gte=start_hour)
        .annotate(bucket=TruncHour("date_created"))
        .values("bucket", "type")
        .annotate(total=Count("id"))
    )
    total_map = {}
    type_maps = {log_type: {} for log_type in LOG_TYPE_LABELS}
    for item in raw:
        bucket = item["bucket"]
        req_type = item["type"]
        total = item["total"]
        total_map[bucket] = total_map.get(bucket, 0) + total
        if req_type in type_maps:
            type_maps[req_type][bucket] = total

    labels = [point.strftime("%H:%M") for point in points]
    total_series = [total_map.get(point, 0) for point in points]
    type_series = {
        LOG_TYPE_LABELS[log_type]: [type_maps[log_type].get(point, 0) for point in points]
        for log_type in LOG_TYPE_LABELS
    }

    return {
        "labels": labels,
        "total": total_series,
        "by_type": type_series,
    }


def _daily_logs_data(days=30):
    today = timezone.localdate()
    points = [today - timedelta(days=i) for i in reversed(range(days))]
    start_day = points[0]

    base = (
        LOG.objects.filter(date_created__date__gte=start_day)
        .annotate(bucket=TruncDay("date_created"))
        .values("bucket")
        .annotate(total=Count("id"))
    )
    total_map = {item["bucket"].date(): item["total"] for item in base}

    user_base = (
        User.objects.filter(date_created__date__gte=start_day)
        .annotate(bucket=TruncDay("date_created"))
        .values("bucket")
        .annotate(total=Count("id"))
    )
    user_map = {item["bucket"].date(): item["total"] for item in user_base}

    labels = [f"{point.day:02d} {EN_MONTH_ABBR[point.month - 1]}" for point in points]
    logs_series = [total_map.get(point, 0) for point in points]
    users_series = [user_map.get(point, 0) for point in points]

    return {
        "labels": labels,
        "logs": logs_series,
        "users": users_series,
    }


def _monthly_logs_data(months=12):
    today = timezone.localdate()
    this_month = date(today.year, today.month, 1)
    points = [_month_shift(this_month, -i) for i in reversed(range(months))]
    start_month = points[0]

    base = (
        LOG.objects.filter(date_created__date__gte=start_month)
        .annotate(bucket=TruncMonth("date_created"))
        .values("bucket")
        .annotate(total=Count("id"))
    )
    total_map = {
        date(item["bucket"].year, item["bucket"].month, 1): item["total"] for item in base
    }

    user_base = (
        User.objects.filter(date_created__date__gte=start_month)
        .annotate(bucket=TruncMonth("date_created"))
        .values("bucket")
        .annotate(total=Count("id"))
    )
    user_map = {
        date(item["bucket"].year, item["bucket"].month, 1): item["total"]
        for item in user_base
    }

    labels = [f"{EN_MONTH_ABBR[point.month - 1]} {point.year}" for point in points]
    logs_series = [total_map.get(point, 0) for point in points]
    users_series = [user_map.get(point, 0) for point in points]

    return {
        "labels": labels,
        "logs": logs_series,
        "users": users_series,
    }


def _request_mix(period_days=None):
    queryset = LOG.objects.all()
    if period_days:
        start_dt = timezone.now() - timedelta(days=period_days)
        queryset = queryset.filter(date_created__gte=start_dt)

    raw = queryset.values("type").annotate(total=Count("id"))
    count_map = {item["type"]: item["total"] for item in raw}
    labels = [LOG_TYPE_LABELS[key] for key in LOG_TYPE_LABELS]
    data = [count_map.get(key, 0) for key in LOG_TYPE_LABELS]
    colors = [LOG_TYPE_COLORS[key] for key in LOG_TYPE_LABELS]

    return {
        "labels": labels,
        "data": data,
        "colors": colors,
    }


def _hour_of_day_profile(days=14):
    start_dt = timezone.now() - timedelta(days=days)
    raw = (
        LOG.objects.filter(date_created__gte=start_dt)
        .annotate(hour=ExtractHour("date_created"))
        .values("hour")
        .annotate(total=Count("id"))
    )
    profile = {item["hour"]: item["total"] for item in raw}

    labels = [f"{h:02d}:00" for h in range(24)]
    data = [profile.get(h, 0) for h in range(24)]

    return {
        "labels": labels,
        "data": data,
    }


def _platform_split():
    raw = User.objects.values("platform").annotate(total=Count("id"))
    label_map = {
        "TG": "Telegram",
        "BALE": "Bale",
    }
    labels = []
    data = []
    for row in raw:
        labels.append(label_map.get(row["platform"], row["platform"]))
        data.append(row["total"])

    if not labels:
        labels = ["Telegram", "Bale"]
        data = [0, 0]

    return {
        "labels": labels,
        "data": data,
    }


def _core_context():
    cache_key = "dashboard_core_context_v2"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    now_dt = timezone.now()

    request_windows = _logs_window_metrics(now_dt)
    user_windows = _users_window_metrics(now_dt)
    requests_hour = request_windows["hour"]
    requests_day = request_windows["day"]
    requests_month = request_windows["month"]
    requests_year = request_windows["year"]

    total_users = User.objects.count()
    total_requests = LOG.objects.count()

    summary_cards = [
        {
            "label": "Total Requests",
            "value": total_requests,
            "change": None,
            "sub": "all-time",
        },
        {
            "label": "Requests (Past Hour)",
            "value": requests_hour["current"],
            "change": requests_hour["change"],
            "sub": "vs previous hour",
        },
        {
            "label": "Requests (Past 24 Hours)",
            "value": requests_day["current"],
            "change": requests_day["change"],
            "sub": "vs previous 24 hours",
        },
        {
            "label": "Requests (Past 30 Days)",
            "value": requests_month["current"],
            "change": requests_month["change"],
            "sub": "vs previous 30 days",
        },
    ]
    user_summary_cards = [
        {
            "label": "Total Users",
            "value": total_users,
            "change": None,
            "sub": "all-time",
        },
        {
            "label": "Users (Past Hour)",
            "value": user_windows["hour"]["current"],
            "change": user_windows["hour"]["change"],
            "sub": "vs previous hour",
        },
        {
            "label": "Users (Past 24 Hours)",
            "value": user_windows["day"]["current"],
            "change": user_windows["day"]["change"],
            "sub": "vs previous 24 hours",
        },
        {
            "label": "Users (Past 30 Days)",
            "value": user_windows["month"]["current"],
            "change": user_windows["month"]["change"],
            "sub": "vs previous 30 days",
        },
    ]

    progression = [
        {"window": "Past Hour", **requests_hour},
        {"window": "Past Day", **requests_day},
        {"window": "Past Month", **requests_month},
        {"window": "Past Year", **requests_year},
    ]
    user_progression = [
        {"window": "Past Hour", **user_windows["hour"]},
        {"window": "Past Day", **user_windows["day"]},
        {"window": "Past Month", **user_windows["month"]},
        {"window": "Past Year", **user_windows["year"]},
    ]

    top_type = (
        LOG.objects.values("type")
        .annotate(total=Count("id"))
        .order_by("-total")
        .first()
    )
    top_type_label = LOG_TYPE_LABELS.get(top_type["type"], "N/A") if top_type else "N/A"
    top_type_count = top_type["total"] if top_type else 0
    top_type_share = round((top_type_count / total_requests) * 100, 1) if total_requests else 0

    avg_requests_per_user = round(total_requests / total_users, 2) if total_users else 0

    context = {
        "now_label": timezone.localtime(now_dt).strftime("%Y-%m-%d %H:%M"),
        "user_summary_cards": user_summary_cards,
        "summary_cards": summary_cards,
        "user_progression": user_progression,
        "progression": progression,
        "kpi": {
            "total_requests": total_requests,
            "total_users": total_users,
            "requests_past_24h": requests_day["current"],
            "requests_past_30d": requests_month["current"],
            "avg_requests_per_user": avg_requests_per_user,
            "top_type_label": top_type_label,
            "top_type_share": top_type_share,
        },
        "chart_hourly": _hourly_logs_data(now_dt),
        "chart_daily": _daily_logs_data(30),
        "chart_monthly": _monthly_logs_data(12),
        "chart_mix_total": _request_mix(),
        "chart_mix_30d": _request_mix(30),
        "chart_hour_profile": _hour_of_day_profile(14),
        "chart_platform": _platform_split(),
    }

    context["chart_json"] = {
        "hourly": json.dumps(context["chart_hourly"]),
        "daily": json.dumps(context["chart_daily"]),
        "monthly": json.dumps(context["chart_monthly"]),
        "mix_total": json.dumps(context["chart_mix_total"]),
        "mix_30d": json.dumps(context["chart_mix_30d"]),
        "hour_profile": json.dumps(context["chart_hour_profile"]),
        "platform": json.dumps(context["chart_platform"]),
    }

    cache.set(cache_key, context, 30)
    return context


def home(request):
    context = _core_context()
    return render(request, "home.html", context=context)


def statistics(request):
    context = _core_context()
    return render(request, "statistics.html", context=context)


def charts(request):
    context = _core_context()
    return render(request, "charts.html", context=context)
