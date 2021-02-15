from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from news import views as news_view

urlpatterns = [
    #path('',news_view.show_home,name='show_home'),
    path('upload',news_view.upload,name='upload'),
    path('view',news_view.view,name='view'),
    path('edit/<id>',news_view.edit,name='edit'),
    path('delete/<id>',news_view.delete,name='delete'),
    path('read/',news_view.show_news,name='show_news'),
    path('list/',news_view.list,name='list_news'),

]

#urlpatterns += staticf1iles_urlpatterns()