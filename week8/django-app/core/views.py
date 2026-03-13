from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .models import Note, Task


@require_http_methods(["GET"])
def dashboard(request: HttpRequest) -> HttpResponse:
    notes = Note.objects.order_by("-created_at")
    tasks = Task.objects.order_by("-created_at")
    return render(
        request,
        "dashboard.html",
        {
            "notes": notes,
            "tasks": tasks,
        },
    )


@require_POST
def add_note(request: HttpRequest) -> HttpResponse:
    content = (request.POST.get("content") or "").strip()
    if content:
        Note.objects.create(content=content)
    return redirect("dashboard")


@require_POST
def add_task(request: HttpRequest) -> HttpResponse:
    description = (request.POST.get("description") or "").strip()
    if description:
        Task.objects.create(description=description)
    return redirect("dashboard")
