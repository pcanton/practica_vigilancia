from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class SecurityRegressionTestCase(TestCase):

    def setUp(self):
        # 1. Creem un usuari normal per a la prova
        self.username = 'analista_test'
        self.password = 'PasswordSegur123!'
        self.user = User.objects.create_user(
            username=self.username, 
            password=self.password,
            email='test@copernic.cat'
        )
        # Ens assegurem que comença sent un usuari NO administrador
        self.user.is_superuser = False
        self.user.save()

    def test_escalada_privilegis_sqli(self):
        # 2. Iniciem sessió amb el client de simulació de Django
        self.client.login(username=self.username, password=self.password)

        # 3. Definim el payload maliciós que vam dissenyar a l'Apartat 4
        payload_malicios = "hacker@copernic.cat', is_superuser = '1' --"

        # 4. Simulem l'enviament del formulari (POST) cap a la vista vulnerable
        url = reverse('actualitzar_correu')
        self.client.post(url, {'email': payload_malicios})

        # 5. Tornem a carregar l'usuari des de la base de dades per veure si s'ha modificat
        self.user.refresh_from_db()

        # 6. L'ASSERT DE L'AUDITOR:
        # Com que som auditors, volem que l'aplicació sigui SEGURA. 
        # Per tant, comprovem si l'usuari SEGUEIX SENT FALSE (no administrador).
        # Si la vulnerabilitat existeix, l'usuari s'haurà convertit en True, l'assert fallarà, 
        # i el test ens avisarà que el sistema és vulnerable (FAIL).
        self.assertFalse(
            self.user.is_superuser, 
            msg="ALERTA DE SEGURETAT: El sistema permet l'escalada de privilegis via SQLi!"
        )
