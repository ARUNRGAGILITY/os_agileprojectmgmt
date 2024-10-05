from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseForbidden
from functools import wraps
from django.db.models import *
from django.http import Http404
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.template import Template, Context
from markdownx.utils import markdownify
from django.conf import settings
from django.db.models import Q
from app_baseline.models.list.model_list import *
from app_baseline.forms.list.form_list import *
from app_xpresskanban.models.core_models import *
from app_xpresskanban.models.delivery_models import *
from app_xpresskanban.forms import *
from app_baseline.models.user.model_user import Profile as AWProfile
from django.db.models.functions import Lower, Trim
from itertools import chain
from markdownx.models import MarkdownxField
from django.conf import settings
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.conf import settings
from django.utils.text import slugify
from django.db.models import Sum, FloatField
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.apps import apps
from datetime import timedelta
from django.contrib.auth.models import Permission
from django.core.serializers.json import DjangoJSONEncoder
from collections import defaultdict
from django.template import Template, Context
from markdownx.utils import markdownify

import base64
import os
import platform
import json
import random

SITE_TITLE = getattr(settings, 'SITE_TITLE', 'MY SITE')
def get_or_create_siteadmin_role():
    role, created = Role.objects.get_or_create(title="SiteAdmin")
    return role
def get_or_create_orgadmin_role():
    role, created = Role.objects.get_or_create(title="OrgAdmin")
    return role
def get_or_create_projectadmin_role():
    role, created = Role.objects.get_or_create(title="ProjectAdmin")
    return role