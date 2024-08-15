from django.http import HttpResponse
from django.shortcuts import render
from user.models import User
from django.utils import timezone
from datetime import timedelta

def home(request):
    return render(request, 'home.html')

def statistics(request):
    oneday_threshold = timezone.now() - timedelta(days=1)
    onehour_threshold = timezone.now() - timedelta(hours=1)

    context = {
        "all_users": User.objects.count(),
        "last24_users": User.objects.filter(date_created__gte=oneday_threshold).count(),
        "last1_users": User.objects.filter(date_created__gte=onehour_threshold).count(),
        "nograde_users": User.objects.filter(grade=None).count(),
        "student_users": User.objects.filter(is_student=1).count(),
        "teacher_users": User.objects.filter(is_student=0).count(),
    }
    return render(request, 'statistics.html', context=context)