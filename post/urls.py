from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<slug:title>/', views.postpage, name='postpage'),


    # page url links

    path('page/it', views.it, name='it'),
    path('page/python', views.python, name='python'),
    path('page/webdevloper', views.webdevloper, name='webdevloper'),
    path('page/tkinter', views.tkinter, name='tkinter'),
    path('page/django', views.django, name='django'),
    path('page/gaming', views.gaming, name='gaming'),
]
