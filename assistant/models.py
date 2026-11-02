from django.db import models
from django.contrib.auth.models import User

class Machine(models.Model):
    machine_id=models.CharField(max_length=40,unique=True); model=models.CharField(max_length=80); name=models.CharField(max_length=160); created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.machine_id} · {self.model}'
class Manual(models.Model):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE,related_name='manuals'); document_id=models.CharField(max_length=80); revision=models.CharField(max_length=20); title=models.CharField(max_length=200); pdf=models.FileField(upload_to='manuals/'); status=models.CharField(max_length=20,default='pending'); error=models.TextField(blank=True); uploaded_at=models.DateTimeField(auto_now_add=True)
class Passage(models.Model):
    manual=models.ForeignKey(Manual,on_delete=models.CASCADE,related_name='passages'); page_number=models.PositiveIntegerField(); text=models.TextField(); chunk_index=models.PositiveIntegerField(default=0); embedding_text=models.TextField(blank=True)
class Question(models.Model):
    STATUS=[('answered','Answered'),('insufficient','Insufficient evidence')]
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True); machine=models.ForeignKey(Machine,on_delete=models.PROTECT); question=models.TextField(); answer=models.TextField(); status=models.CharField(max_length=20,choices=STATUS); created_at=models.DateTimeField(auto_now_add=True)
class Citation(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE,related_name='citations'); passage=models.ForeignKey(Passage,on_delete=models.PROTECT); score=models.FloatField(default=0)
class AuditLog(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True); action=models.CharField(max_length=100); detail=models.TextField(blank=True); created_at=models.DateTimeField(auto_now_add=True)
