import json
from django.views.decorators.csrf import csrf_exempt
from content.models import Grade, Class
from bot import strings
import persian
from .api import *
from user.models import User


