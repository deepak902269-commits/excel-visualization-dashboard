from django.urls import path

from . import views

urlpatterns = [

    path(
        '',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'upload/',
        views.upload_file,
        name='upload'
    ),

    path(
        'preview/<int:file_id>/',
        views.preview_file,
        name='preview'
    ),

    path(
        'generate/<int:file_id>/',
        views.generate_visualization,
        name='generate'
    ),

    path(
        'history/',
        views.history,
        name='history'
    ),
]