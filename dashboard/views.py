from django.http import HttpResponse
from django.shortcuts import render
from bot.models import LOG
from content.models import Question, Unit
from user.models import User
from django.utils import timezone
from datetime import timedelta


def home(request):
    oneday_threshold = timezone.now() - timedelta(days=1)

    twoday_threshold = oneday_threshold - timedelta(days=1)
    
    last24_questions = LOG.objects.filter(
        date_created__gte=oneday_threshold, type=0).count()
    previous24_questions = LOG.objects.filter(
        date_created__gte=twoday_threshold, date_created__lte=oneday_threshold, type=0).count()
    if (previous24_questions > 0):
        previous24_questions_increase_percent = (
            last24_questions - previous24_questions) * 100 // previous24_questions
    else:
        previous24_questions_increase_percent = 0

    last24_pdfs = LOG.objects.filter(
        date_created__gte=oneday_threshold, type=1).count()
    previous24_pdfs = LOG.objects.filter(
        date_created__gte=twoday_threshold, date_created__lte=oneday_threshold, type=1).count()
    if (previous24_pdfs > 0):
        previous24_pdfs_increase_percent = (
            last24_pdfs - previous24_pdfs) * 100 // previous24_pdfs
    else:
        previous24_pdfs_increase_percent = 0

    last24_ai = LOG.objects.filter(
        date_created__gte=oneday_threshold, type=2).count()
    previous24_ai = LOG.objects.filter(
        date_created__gte=twoday_threshold, date_created__lte=oneday_threshold, type=2).count()
    if (previous24_ai > 0):
        previous24_ai_increase_percent = (
            last24_ai - previous24_ai) * 100 // previous24_ai
    else:
        previous24_ai_increase_percent = 0
    context = {
        "all_users": User.objects.count(),
        "student_users": User.objects.filter(is_student=1).count(),
        "teacher_users": User.objects.filter(is_student=0).count(),
        "logs_count": LOG.objects.count(),
        "questions": LOG.objects.filter(type=0).count(),
        "pdfs": LOG.objects.filter(type=1).count(),
        "ai": LOG.objects.filter(type=2).count(),
        "all_questions_logs": LOG.objects.filter(type=0).count(),
        "all_pdfs_logs": LOG.objects.filter(type=1).count(),
        "all_ai_logs": LOG.objects.filter(type=2).count(),
        "last24_questions_logs": LOG.objects.filter(type=0, date_created__gte=oneday_threshold).count(),
        "last24_pdfs_logs": LOG.objects.filter(type=1, date_created__gte=oneday_threshold).count(),
        "last24_ai_logs": LOG.objects.filter(type=2, date_created__gte=oneday_threshold).count(),
        "previous24_questions_increase_percent": previous24_questions_increase_percent,
        "previous24_pdfs_increase_percent": previous24_pdfs_increase_percent,
        "previous24_ai_increase_percent": previous24_ai_increase_percent,
    }
    return render(request, 'home.html', context=context)


def statistics(request):
    oneday_threshold = timezone.now() - timedelta(days=1)
    onehour_threshold = timezone.now() - timedelta(hours=1)

    twoday_threshold = oneday_threshold - timedelta(days=1)
    twohour_threshold = onehour_threshold - timedelta(hours=1)

    last24_users = User.objects.filter(
        date_created__gte=oneday_threshold).count()
    previous24_users = User.objects.filter(
        date_created__gte=twoday_threshold, date_created__lte=oneday_threshold).count()
    if (previous24_users > 0):
        last24_users_increase_percent = (
            last24_users - previous24_users) * 100 // previous24_users
    else:
        last24_users_increase_percent = 0
    last1_users = User.objects.filter(
        date_created__gte=onehour_threshold).count()
    previous1_users = User.objects.filter(
        date_created__gte=twohour_threshold, date_created__lte=onehour_threshold).count()
    if (previous1_users > 0):
        last1_users_increase_percent = (
            last1_users - previous1_users) * 100 // previous1_users
    else:
        last1_users_increase_percent = 0

    last24_questions = LOG.objects.filter(
        date_created__gte=oneday_threshold, type=0).count()
    previous24_questions = LOG.objects.filter(
        date_created__gte=twoday_threshold, date_created__lte=oneday_threshold, type=0).count()
    if (previous24_questions > 0):
        previous24_questions_increase_percent = (
            last24_questions - previous24_questions) * 100 // previous24_questions
    else:
        previous24_questions_increase_percent = 0

    last24_pdfs = LOG.objects.filter(
        date_created__gte=oneday_threshold, type=1).count()
    previous24_pdfs = LOG.objects.filter(
        date_created__gte=twoday_threshold, date_created__lte=oneday_threshold, type=1).count()
    if (previous24_pdfs > 0):
        previous24_pdfs_increase_percent = (
            last24_pdfs - previous24_pdfs) * 100 // previous24_pdfs
    else:
        previous24_pdfs_increase_percent = 0

    last24_ai = LOG.objects.filter(
        date_created__gte=oneday_threshold, type=2).count()
    previous24_ai = LOG.objects.filter(
        date_created__gte=twoday_threshold, date_created__lte=oneday_threshold, type=2).count()
    if (previous24_ai > 0):
        previous24_ai_increase_percent = (
            last24_ai - previous24_ai) * 100 // previous24_ai
    else:
        previous24_ai_increase_percent = 0
    context = {
        "all_users": User.objects.count(),
        "last24_users": last24_users,
        "last24_users_increase_percent": last24_users_increase_percent,
        "last1_users": last1_users,
        "last1_users_increase_percent": last1_users_increase_percent,
        "nograde_users": User.objects.filter(grade=None).count(),
        "student_users": User.objects.filter(is_student=1).count(),
        "teacher_users": User.objects.filter(is_student=0).count(),
        "all_questions": Question.objects.count(),
        "all_units": Unit.objects.count(),
        "all_questions_logs": LOG.objects.filter(type=0).count(),
        "all_pdfs_logs": LOG.objects.filter(type=1).count(),
        "all_ai_logs": LOG.objects.filter(type=2).count(),
        "last24_questions_logs": LOG.objects.filter(type=0, date_created__gte=oneday_threshold).count(),
        "last24_pdfs_logs": LOG.objects.filter(type=1, date_created__gte=oneday_threshold).count(),
        "last24_ai_logs": LOG.objects.filter(type=2, date_created__gte=oneday_threshold).count(),
        "previous24_questions_increase_percent": previous24_questions_increase_percent,
        "previous24_pdfs_increase_percent": previous24_pdfs_increase_percent,
        "previous24_ai_increase_percent": previous24_ai_increase_percent,
    }
    return render(request, 'statistics.html', context=context)


def charts(request):
    context = {
    }
    return render(request, 'charts.html', context=context)
