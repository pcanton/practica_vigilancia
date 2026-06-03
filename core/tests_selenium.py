from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class SecurityRegressionTests(TestCase):
    fixtures = ['testdb.json']  # Càrrega de dades obligatòria

    def test_role_restriction(self):
        """AUDITORIA: L'analista no ha d'entrar a /admin/"""
        # 1. Realitzem el Login simulat de l'usuari analista
        self.client.login(username='analista1', password='PasswordSegur123!')
        
        # 2. Intentem forçar l'accés a la URL d'administració protegida
        response = self.client.get('/admin/', follow=True)
        
        # 3. ASSERT DE SEGURETAT (Fase GREEN - El test ha de passar)
        # Verifiquem que l'analista NO rep un codi de visualització exitós (200) de l'admin
        self.assertNotEqual(response.status_code, 200)
