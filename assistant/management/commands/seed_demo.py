from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from assistant.models import Machine
class Command(BaseCommand):
 def handle(self,*args,**kwargs):
  for mid,model,name in [('M-HP200','HP-200','Hydraulic forming press'),('M-AC90','AC-90','Air compressor')]: Machine.objects.get_or_create(machine_id=mid,defaults={'model':model,'name':name})
  for username,role in [('admin','admin'),('engineer','engineer'),('supervisor','supervisor')]:
   u,_=User.objects.get_or_create(username=username); u.set_password('demo1234'); u.is_staff=(role=='admin'); u.is_superuser=(role=='admin'); u.save()
  self.stdout.write(self.style.SUCCESS('Demo users: admin, engineer, supervisor / password demo1234'))
