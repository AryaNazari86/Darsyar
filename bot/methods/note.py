import json
from random import randint
from bot import strings
from bot.credintials import PLATFORM, notes_gc, note_report_gc
from bot.methods.logs import log_requests
from user.models import User
from .api import *
from content.models import Grade, Class, Unit, Question, NotePackage
import persian

def choose_class_note(chat_id, user_id):
    user = User.objects.get(platform=PLATFORM, user_id=user_id)

    classes = []
    
    for cls in user.grade.classes.all():
        if cls.notes.filter(platform = PLATFORM, confirmed = True).count() > 0:
            classes.append(cls)

    #print(len(classes))
    send(
        'sendMessage',
        {
            "chat_id": chat_id,
            "text": strings.choose_class,
            "reply_markup": json.dumps({
                "inline_keyboard": [
                    [{"text": cls.name, "callback_data": 'n' + str(cls.id)}] for cls in classes
                ]
            })
        }
    )

    log_requests(user, 0, 0, 4)

def choose_class_addnote(chat_id, user_id):
    user = User.objects.get(platform=PLATFORM, user_id=user_id)

    send(
        'sendMessage',
        {
            "chat_id": chat_id,
            "text": strings.choose_class_note,
            "reply_markup": json.dumps({
                "inline_keyboard": [
                    [{"text": cls.name, "callback_data": 'm' + str(cls.id)}] for cls in user.grade.classes.all()
                ]
            })
        }
    )

def send_note(chat_id, cls_id):
    cls = Class.objects.all().get(
        id=int(cls_id)
    )
    q = randint(0, cls.notes.filter(confirmed = True, platform = PLATFORM).count()-1)
    note = cls.notes.filter(confirmed = True, platform = PLATFORM)[q]
    note.views += 1
    #note.upvotes.add(User.objects.get(user_id = chat_id, platform = PLATFORM))
    note.save()


    send(
        'sendDocument',
        {
            "chat_id": chat_id,
            "document": note.file_id,
            "caption": strings.note_caption.format(cls.name, note.author, persian.convert_en_numbers(note.views), persian.convert_en_numbers(note.rating())),
            "reply_markup": json.dumps({
                "inline_keyboard": [
                    [
                        {"text": strings.upvote_note, "callback_data": "&" + str(note.id)},
                        {"text": strings.downvote_note, "callback_data": "*" + str(note.id)}
                    ],
                    [{"text": strings.report_note, "callback_data": "@" + str(note.id)}],
                    [{"text": strings.next_note, "callback_data": 'n' + str(cls.id)}],
                    [{"text": strings.show_menu_note, "callback_data": '!'}],
                ]
            })
        }
    )

def upvote_note(chat_id, user_id, note_id):
    user = User.objects.get(platform=PLATFORM, user_id=user_id)
    note = NotePackage.objects.get(id = note_id)

    note.upvotes.add(user)
    user.save()

    send(
        'sendMessage',
        {
            "chat_id": chat_id,
            "text": strings.vote_note_suc,
            "reply_marup": MENU
        }
    )

def downvote_note(chat_id, user_id, note_id):
    user = User.objects.get(platform=PLATFORM, user_id=user_id)
    note = NotePackage.objects.get(id = note_id)

    note.downvotes.add(user)
    user.save()

    send(
        'sendMessage',
        {
            "chat_id": chat_id,
            "text": strings.vote_note_suc,
            "reply_marup": MENU
        }
    )

def add_note(chat_id, user_id, cls_id):
    user = User.objects.get(platform=PLATFORM, user_id=user_id)
    user.state = -int(cls_id)
    user.save()

    send(
        'sendMessage',
        {
            "chat_id": chat_id,
            "text": strings.send_note,
            "reply_markup": json.dumps({
                "inline_keyboard": [
                    [{"text": strings.reset_state, "callback_data": '^'}]
                ]
            })
        }
    )

def receive_note(chat_id, user_id, msg):
    try:
        user = User.objects.get(platform=PLATFORM, user_id=user_id)
        cls = Class.objects.get(id = -user.state)
        note = NotePackage.objects.create(
            author = user,
            class_rel = cls,
            file_id = msg['document']['file_id'],
            platform=PLATFORM,
        )

        user.state = 0
        user.save()

        send(
            'sendMessage',
            {
                "chat_id": chat_id,
                "text": strings.receive_note,
                "reply_markup": MENU
            }
        )

        send(
            'sendDocument',
            {
                "chat_id": notes_gc,
                "document": note.file_id,
                "caption": f"ℹ️: {note.id}\n👤 {note.author.user_id}",
            }
        )
    except Exception as e:
        print(e)
        send(
            'sendMessage',
            {
                "chat_id": chat_id,
                "text": strings.tryagain_note,
                "reply_markup": json.dumps({
                    "inline_keyboard": [
                        [{"text": strings.reset_state, "callback_data": '^'}]
                    ]
                })
            }
        )

def report(chat_id, msg, note_id):
    send(
        'deleteMessage',
        {
            "chat_id": chat_id,
            "message_id": msg["message_id"]
        }
    )

    note = NotePackage.objects.get(id = note_id)
    #note.confirmed = 0
    note.save()

    send(
        'sendMessage',
        {
            "chat_id": chat_id,
            "text": strings.report_received,
            "reply_markup": MENU,
        }
    )

    send(
        'sendDocument',
        {
            "chat_id": note_report_gc,
            "document": note.file_id,
            "caption": f"ℹ️: {note.id}",
        }
    )