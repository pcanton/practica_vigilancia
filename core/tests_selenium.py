from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class SecurityRegressionTests(TestCase):
    fixtures = ['testdb.json']  # Càrrega de dades (Punt 2.2.2 del PDF)

    def test_role_restriction(self):
        """AUDITORIA: L'analista no ha d'entrar a /admin/"""
        # 1. Realitzem el Login simulat utilitzant l'usuari de les nostres dades del JSON
        # Passem l'usuari 'analista1' i la seva credencial
        self.client.login(username='analista1', password='PasswordSegur123!')
        
        # 2. Intentem forçar l'accés a la URL d'administració protegida
        response = self.client.get('/admin/', follow=True)
        
        # 3. ASSERT DE SEGURETAT (Fase RED - Forcem el FAIL per a l'Evidència 2)
        # Comprovem si ha pogut entrar responent amb un codi d'èxit 200 de l'admin
        # Això fallarà (FAIL) perquè actualment l'analista té els permisos trets i el sistema el redirigirà
        self.assertEqual(response.status_code, 200)
