import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

class TestProductDeletion:
    @pytest.fixture
    def driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        
        # Utiliser le gestionnaire de pilotes intégré de Selenium
        driver = webdriver.Chrome(options=chrome_options)
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
        
        # Attendre que la page soit complètement chargée
        time.sleep(3)
        
        # Vérifier que le produit est présent
        try:
            # Trouver la ligne du produit en cherchant le texte
            product_row = WebDriverWait(driver, 5
            ).until(
                EC.presence_of_element_located((By.XPATH, "//tr[contains(., 'Sabre laser modifié')]"))
            )
            print("Produit trouvé : Sabre laser modifié")
            
            # Trouver la case à cocher dans cette ligne
            checkbox = product_row.find_element(By.XPATH, ".//input[@type='checkbox']")
            print("HTML de la ligne produit :", product_row.get_attribute('outerHTML'))
            print("Case à cocher trouvée")
            
            # Trouver le label parent de la case à cocher et cliquer dessus
            label = checkbox.find_element(By.XPATH, "ancestor::label")
            label.click()
            print("Label cliqué (case à cocher activée)")

            # ✅ Étape 2 : Attendre que la barre d'action s'affiche (celle contenant "Delete")
            action_bar = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".inline-flex"))
            )
            print("Barre d'action trouvée")
            # ✅ Étape 3 : Récupère tous les boutons de la barre et clique sur celui qui contient "Delete"
            buttons = action_bar.find_elements(By.CSS_SELECTOR, "a.font-semibold")
            for button in buttons:
                if "Delete" in button.text:
                    button.click()
                    print("Bouton de suppression trouvé et cliqué")
                    break
        
            # Afficher le HTML de la page pour diagnostiquer
            print("HTML de la page après clic sur 'Delete':", driver.page_source)
            
            # Confirmer la suppression
            confirm_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            confirm_button.click()
            print("Suppression confirmée")
            
            # Vérifier que le produit n'est plus présent
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.XPATH, "//tr[contains(., 'Sabre laser modifié')]"))
            )
            print("Produit supprimé avec succès")
        except Exception as e:
            print(f"Erreur lors de la suppression du produit: {e}")
       