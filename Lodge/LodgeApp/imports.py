from django.shortcuts import render as render, get_object_or_404 as get_object_or_404, redirect as redirect
from django.urls import reverse as reverse
from django.views.decorators.csrf import csrf_exempt as csrf_exempt
from django.http import JsonResponse as JsonResponse, HttpResponse as HttpResponse
from django.core.exceptions import PermissionDenied

from django.conf import settings as settings

import csv as csv

from .models import Room as Room, Guest as Guest, GuestHistory as GuestHistory, Log as Log, Revenue as Revenue, CheckIns as CheckIns, Company as Company, Suite as Suite, Subscriptions as Subscriptions

from django.contrib.auth import login as login, authenticate as authenticate, logout as logout, get_user_model as get_user_model
from django.contrib import messages as messages

from django.db import IntegrityError as IntegrityError, transaction as transaction

Staff = get_user_model()

from datetime import datetime as datetime, date as date, timedelta as timedelta
from django.utils import timezone as timezone
from dateutil.relativedelta import relativedelta as relativedelta
import calendar as calendar

from django.db.models.functions import ExtractYear as ExtractYear, ExtractMonth as ExtractMonth, ExtractDay as ExtractDay, TruncWeek as TruncWeek
from django.db.models import Sum as Sum, Avg as Avg, Count as Count, Q as Q

from collections import defaultdict as defaultdict

from decimal import Decimal as Decimal

from django.core.mail import send_mail as send_mail

import numpy as np
import re as re