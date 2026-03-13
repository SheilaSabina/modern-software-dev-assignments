from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("notes/add/", views.add_note, name="add_note"),
    path("tasks/add/", views.add_task, name="add_task"),
]

