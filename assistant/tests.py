from django.test import TestCase,Client
from django.contrib.auth.models import User
from .models import Machine,Manual,Passage
from .services import retrieve
class IsolationTests(TestCase):
 def setUp(self):
  self.a=Machine.objects.create(machine_id='A',model='A',name='Machine A'); self.b=Machine.objects.create(machine_id='B',model='B',name='Machine B')
  self.ma=Manual.objects.create(machine=self.a,document_id='A-1',revision='1',title='A',status='ready'); self.mb=Manual.objects.create(machine=self.b,document_id='B-1',revision='1',title='B',status='ready')
  Passage.objects.create(manual=self.ma,page_number=1,text='normal pressure is 120 bar'); Passage.objects.create(manual=self.mb,page_number=1,text='compressor pressure is 8 bar')
 def test_retrieval_is_machine_scoped(self): self.assertTrue(all(p.manual.machine_id==self.a.id for _,p in retrieve(self.a,'compressor pressure')))
 def test_engineer_cannot_upload(self):
  u=User.objects.create_user('eng',password='x'); self.client.login(username='eng',password='x'); self.assertEqual(self.client.get('/upload/').status_code,403)
