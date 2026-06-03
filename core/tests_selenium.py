from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

class SecurityRegressionTests(StaticLiveServerTestCase):
    fixtures = ['testdb.json']  # Càrrega de dades automàtica des de la fixture [cite: 205]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        opts.add_argument("--headless")  # Mode invisible obligatori per a la CI de GitHub [cite: 222, 256]
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(10)  # Evita problemes de velocitat de càrrega [cite: 224, 257]

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_role_restriction(self):
        """AUDITORIA: L'analista no ha d'entrar a /admin/"""
        # 1. Anem a la pàgina de login de la nostra aplicació [cite: 231]
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        
        # 2. Omplim el formulari de login amb l'usuari de la fixture [cite: 232, 234]
        self.selenium.find_element(By.NAME, "username").send_keys("analista1")
        self.selenium.find_element(By.NAME, "password").send_keys("PasswordSegur123!")
        
        # Envia el formulari buscant el botó de submissió (adapta el tipus si cal, o per ID)
        self.selenium.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # 3. Intentem forçar l'accés a la URL protegida d'administració [cite: 235, 236]
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/'))
        
        # 4. ASSERT DE SEGURETAT DE LA FASE GREEN 
        # Com que prèviament li hem tret el permís de staff a la base de dades, 
        # Django el redirigirà fora de l'administració. El títol NO ha de ser el de gestió. 
        self.assertNotEqual(self.selenium.title, "Site administration | Django site admin") [cite: 237, 238, 239]
