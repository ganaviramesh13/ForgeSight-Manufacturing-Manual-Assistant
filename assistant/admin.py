from django.contrib import admin
from .models import Machine,Manual,Passage,Question,Citation,AuditLog
for model in [Machine,Manual,Passage,Question,Citation,AuditLog]: admin.site.register(model)
