from django.shortcuts import render as render, get_object_or_404 as get_object_or_404, redirect as redirect
from django.urls import reverse as reverse
from django.views.decorators.csrf import csrf_exempt as csrf_exempt
from django.http import JsonResponse as JsonResponse, HttpResponse as HttpResponse

import csv as csv

from .models import Room as Room, Guest as Guest, Log as Log, Revenue as Revenue, CheckIns as CheckIns, Company as Company, Suite as Suite

from django.contrib.auth import login as login, authenticate as authenticate, logout as logout, get_user_model as get_user_model

Staff = get_user_model()

from datetime import datetime as datetime, date as date, timedelta as timedelta
from django.utils import timezone as timezone

import numpy as np
import re as re