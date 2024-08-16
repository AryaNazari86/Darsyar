from django.http import HttpResponse
from django.shortcuts import render
from bot.models import LOG
from user.models import User
from django.utils import timezone
from datetime import timedelta


def home(request):
    context = {
        "all_users": User.objects.count(),
        "student_users": User.objects.filter(is_student=1).count(),
        "teacher_users": User.objects.filter(is_student=0).count(),
        "logs_count": LOG.objects.count(),
        "questions": LOG.objects.filter(type=0).count(),
        "pdfs": LOG.objects.filter(type=1).count(),
        "ai": LOG.objects.filter(type=2).count(),
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
    print(previous24_users)
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
    context = {
        "all_users": User.objects.count(),
        "last24_users": last24_users,
        "last24_users_increase_percent": last24_users_increase_percent,
        "last1_users": last1_users,
        "last1_users_increase_percent": last1_users_increase_percent,
        "nograde_users": User.objects.filter(grade=None).count(),
        "student_users": User.objects.filter(is_student=1).count(),
        "teacher_users": User.objects.filter(is_student=0).count(),
    }
    return render(request, 'statistics.html', context=context)


def charts(request):
    context = {
    }
    return render(request, 'charts.html', context=context)
