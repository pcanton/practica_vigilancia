from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import SecurityIncident

# ---- VISTA APARTAT 2 I 3 SECURITZADA AMB L'ORM ----
def cerca_incidents_vulnerable(request):
    resultats = []
    query_usuari = request.GET.get('q', '')

    if query_usuari:
        # L'ORM de Django utilitza icontains per fer un 'LIKE' d'SQL de manera segura.
        # Això converteix automàticament l'entrada en un paràmetre sanititzat.
        resultats_orm = SecurityIncident.objects.filter(title__icontains=query_usuari)
        
        # Convertim el QuerySet de l'ORM a tuples d'estil (id, title, description...) 
        # perquè continuï sent 100% compatible amb la teva plantilla HTML actual.
        resultats = [(i.id, i.title, i.description) for i in resultats_orm]

    return render(request, 'cerca_resultats.html', {
        'resultats': resultats, 
        'query': query_usuari
    })

# ---- VISTA APARTAT 4 SECURITZADA AMB L'ORM ----
@login_required
def actualitzar_correu_vulnerable(request):
    missatge = ""
    if request.method == 'POST':
        nou_email = request.POST.get('email', '')
        
        if nou_email:
            # L'ORM aïlla el valor de 'nou_email'. El tracta estrictament com un text (string)
            # i impedeix que s'executin ordres com modifies columnes extra (is_superuser).
            User.objects.filter(id=request.user.id).update(email=nou_email)
            
            missatge = "Perfil actualitzat correctament de forma segura."

    return render(request, 'actualitzar_correu.html', {'missatge': missatge})
from django.shortcuts import get_object_or_404

@login_required
# Comenta aquesta línia posant un # al davant:
# @login_required
def detall_incident_vulnerable(request, id):
    # Busquem l'incident directament per la ID de la URL
    incident = get_object_or_404(SecurityIncident, id=id)
    
    return render(request, 'detall_incident.html', {'incident': incident})
