import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class TestProductDeletion:
    @pytest.fixture
    def driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        yield driver
        driver.quit()

    def find_input(self, driver, ids_or_names, timeout=10):
        for by, value in ids_or_names:
            try:
                return WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((by, value))
                )
            except Exception:
                continue
        raise Exception(f"Aucun champ trouvé pour {ids_or_names}")

    def admin_login(self, driver):
        driver.get("http://localhost:3000/admin/login")
        email_input = self.find_input(driver, [
            (By.ID, "email"),
            (By.NAME, "email"),
            (By.XPATH, "//input[contains(translate(@placeholder, 'EMAIL', 'email'), 'email')]")
        ])
        email_input.send_keys("malyy@mail.com")
        password_input = self.find_input(driver, [
            (By.ID, "password"),
            (By.NAME, "password"),
            (By.XPATH, "//input[contains(translate(@placeholder, 'PASSWORD', 'password'), 'password')]")
        ])
        password_input.send_keys("azertyuiopq1")
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit'] | //input[@type='submit']"))
        )
        submit_button.click()
        WebDriverWait(driver, 10).until(
            lambda driver: "/login" not in driver.current_url
        )

    def test_delete_product(self, driver):
        self.admin_login(driver)
        driver.get("http://localhost:3000/admin/products")
        
        # Trouver le produit à supprimer
        product_row = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//tr[contains(., 'Sabre laser modifié')]"))
        )
        
        # Cliquer sur l'input checkbox en utilisant JavaScript
        select_checkbox = product_row.find_element(By.XPATH, ".//input[@type='checkbox']")
        driver.execute_script("arguments[0].click();", select_checkbox)
        
        # Attendre un peu pour que l'interface se mette à jour
        time.sleep(1)
        
        # Trouver et cliquer sur le lien de suppression
        delete_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'font-semibold') and contains(., 'Delete')]"))
        )
        delete_link.click()
        
        # Confirmer la suppression dans la boîte de dialogue en utilisant JavaScript
        confirm_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Delete') or contains(., 'Supprimer')]"))
        )
        driver.execute_script("arguments[0].click();", confirm_button)
        
        # Vérifier que le produit n'est plus présent
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, "//tr[contains(., 'Sabre laser modifié')]"))
        ) 