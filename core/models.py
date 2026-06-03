from django.db import models
from django.contrib.auth.models import User

class SecurityIncident(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    severity = models.CharField(max_length=10, choices=[
        ('Alta', 'Alta'),
        ('Mitjana', 'Mitjana'),
        ('Baixa', 'Baixa'),
    ])
    detected_at = models.DateTimeField(auto_now_add=True)
    # Camp clau per fer el control d'accés: el propietari de l'incident
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
