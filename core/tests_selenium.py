from django.test import TestCase

class SecurityRegressionTests(TestCase):
    fixtures = ['testdb.json']  # Càrrega de dades (Punt 2.2.2 del PDF) [cite: 205]

    def test_role_restriction(self):
        """AUDITORIA: L'analista no ha d'entrar a /admin/"""
        # 1. Realitzem el Login simulat de l'analista (ja modificat a la base de dades)
        self.client.login(username='analista1', password='PasswordSegur123!')
        
        # 2. Intentem forçar la URL d'administració (SENSE follow=True per veure la intercepció directa)
        response = self.client.get('/admin/', follow=False)
        
        # 3. ASSERT DE SEGURETAT DE FASE GREEN (Evidència 3)
        # Comprovem que Django retorna un codi 302 (Redirecció forçosa per manca de permisos)
        # Això certificarà que el "policia" ha expulsat l'analista de la zona VIP
        self.assertEqual(response.status_code, 302)
