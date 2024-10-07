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
from django.db import transaction
from collections import defaultdict
from django.template.loader import get_template, TemplateDoesNotExist
import base64
import os
import platform
import json
import random
import logging
logger = logging.getLogger(__name__)
SITE_TITLE = getattr(settings, 'SITE_TITLE', 'MY SITE')

##################################  CONSTANTS ##################################


COMMON_ROLE_CONFIG = {
    "SCRUM_MASTER": {"name": "Scrum Master", "count": 2},
    "PRODUCT_OWNER": {"name": "Product Owner", "count": 2},
    "TEAM_MEMBER": {"name": "TeamMember", "count": 20},
    "ADMIN": {"name": "Admin", "count": 1},
    "EDITOR": {"name": "Editor", "count": 1},
    "VIEWER": {"name": "Viewer", "count": 2},
    "MANAGER": {"name": "Manager", "count": 2},
    "CONTRIBUTOR": {"name": "Contributor", "count": 2},
    "DEVELOPER": {"name": "Developer", "count": 2},
    "DESIGNER": {"name": "Designer", "count": 2},
    "UI_UX": {"name": "UI/UX", "count": 5},
    "SYSTEM_ARCHITECT": {"name": "System Architect", "count": 5},
    "ENTERPRISE_ARCHITECT": {"name": "Enterprise Architect", "count": 5},
    "BUSINESS_OWNER": {"name": "Business Owner", "count": 5},
    "PROGRAM_MANAGER": {"name": "Program Manager", "count": 5},
    "PROJECT_MANAGER": {"name": "Project Manager", "count": 5},
    "PORTFOLIO_MANAGER": {"name": "Portfolio Manager", "count": 5},
    "BLOG_ADMIN": {"name": "Blog Admin", "count": 5},
    "BLOG_WRITER": {"name": "Blog Writer", "count": 5},
    "BLOG_EDITOR": {"name": "Blog Editor", "count": 5},
    "BLOG_VIEWER": {"name": "Blog Viewer", "count": 5},
    "SITE_ADMIN": {"name": "Site Admin", "count": 1},
    "ORG_ADMIN": {"name": "Org Admin", "count": 1},
    "PROJECT_ADMIN": {"name": "Project Admin", "count": 1},
    "QA": {"name": "QA", "count": 2},
    "ARCHITECT": {"name": "Architect", "count": 2},
    "DEVOPS": {"name": "DevOps", "count": 2},
    "SECURITY": {"name": "Security", "count": 2},
    "BUSINESS_ANALYST": {"name": "Business Analyst", "count": 2},
    "IT_ENGINEER": {"name": "IT Engineer", "count": 2},
    "NETWORK_ENGINEER": {"name": "Network Engineer", "count": 2},
    "TECH_LEAD": {"name": "Tech Lead", "count": 2},
    "PROJECT_LEAD": {"name": "Project Lead", "count": 2},
    "SUPER_USER": {"name": "Super User", "count": 0},
    "NO_ROLE": {"name": "No Role", "count": 0},
}


COMMON_PROJECT_ROLE_CONFIG = {
    "PROJECT_ADMIN": "Admin",
    "PROJECT_EDITOR": "Editor",
    "PROJECT_VIEWER": "Viewer",
    "PROJECT_NOROLE": "No Role",   
}
################################################################################