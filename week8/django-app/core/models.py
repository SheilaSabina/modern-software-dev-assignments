from django.db import models

class Note(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Note #{self.pk}"


class Task(models.Model):
    description = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        status = "done" if self.done else "todo"
        return f"Task #{self.pk} ({status})"
