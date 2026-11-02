from django.urls import path
from . import views
urlpatterns=[path('',views.home,name='home'),path('login/',views.login_view,name='login'),path('logout/',views.logout_view,name='logout'),path('dashboard/',views.dashboard,name='dashboard'),path('upload/',views.upload_manual,name='upload'),path('ask/',views.ask,name='ask'),path('api/machines/',views.api_machines,name='api_machines'),path('manuals/<int:manual_id>/page/<int:page>/',views.pdf_page,name='pdf_page')]
