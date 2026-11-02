import csv, os
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse,FileResponse,Http404
from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import *
from .services import ingest_manual,retrieve,answer_from_evidence

def role(u):
    if u.is_superuser or u.username.lower() == 'admin': return 'admin'
    if u.username.lower() == 'supervisor': return 'supervisor'
    return 'engineer'
def home(request): return render(request,'home.html')
def login_view(request):
 if request.method=='POST':
  u=authenticate(request,username=request.POST.get('username'),password=request.POST.get('password'))
  if u: login(request,u); return redirect('dashboard')
  messages.error(request,'Invalid credentials.')
 return render(request,'login.html')
def logout_view(request): logout(request); return redirect('home')
@login_required
def dashboard(request):
 r=role(request.user); ctx={'role':r,'machines':Machine.objects.all(),'questions':Question.objects.filter(user=request.user).select_related('machine')[:10],'stats':{'machines':Machine.objects.count(),'manuals':Manual.objects.count(),'passages':Passage.objects.count(),'questions':Question.objects.count()}}
 if r=='supervisor': ctx['questions']=Question.objects.select_related('machine','user').order_by('-created_at')[:50]
 return render(request,'dashboard.html',ctx)
@login_required
@require_http_methods(['GET','POST'])
def upload_manual(request):
 if role(request.user)!='admin': return JsonResponse({'detail':'Only administrators can upload manuals.'},status=403)
 if request.method=='POST':
  f=request.FILES.get('pdf'); machine=get_object_or_404(Machine,pk=request.POST.get('machine')); 
  if not f or not f.name.lower().endswith('.pdf'): messages.error(request,'Upload a PDF file.'); return redirect('upload')
  m=Manual.objects.create(machine=machine,document_id=request.POST.get('document_id','UPLOAD'),revision=request.POST.get('revision','1.0'),title=request.POST.get('title',f.name),pdf=f)
  try: ingest_manual(m); messages.success(request,f'Indexed {m.title}.')
  except Exception as e: messages.error(request,f'Ingestion failed: {e}')
  return redirect('dashboard')
 return render(request,'upload.html',{'machines':Machine.objects.all()})
@login_required
@require_http_methods(['POST'])
def ask(request):
 machine=get_object_or_404(Machine,pk=request.POST.get('machine_id')); query=request.POST.get('question','').strip()
 if not query: return JsonResponse({'error':'Question is required.'},status=400)
 hits=retrieve(machine,query); answer,status=answer_from_evidence(query,hits)
 q=Question.objects.create(user=request.user,machine=machine,question=query,answer=answer,status=status)
 cites=[]
 for score,p in hits:
  if score>=.035: Citation.objects.create(question=q,passage=p,score=score); cites.append({'title':p.manual.title,'document_id':p.manual.document_id,'revision':p.manual.revision,'machine_id':machine.machine_id,'page':p.page_number,'passage':p.text,'url':f'/manuals/{p.manual_id}/page/{p.page_number}/'})
 return JsonResponse({'id':q.id,'answer':answer,'status':status,'citations':cites})
def pdf_page(request,manual_id,page):
 m=get_object_or_404(Manual,pk=manual_id)
 if not os.path.exists(m.pdf.path): raise Http404
 return FileResponse(open(m.pdf.path,'rb'),content_type='application/pdf')
def api_machines(request): return JsonResponse({'machines':list(Machine.objects.values('id','machine_id','model','name'))})
