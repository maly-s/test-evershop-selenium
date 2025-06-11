#crée moi un test avec selenium utilise le fichier config.py je veux un test de login admin

#jeu de données :
#login : admin
#password : gma@mail.com
#password : admin123

#url : http://localhost:3000/admin/login

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import setup_driver
import time

class TestAdminLogin:
    @pytest.fixture(scope="function")
    def driver(self):
        driver = setup_driver()
        yield driver
        driver.quit()

    def test_successful_login(self, driver):
        try:
            # Navigate to login page
            driver.get("http://10.21.6.26:3000/admin/login")
            print("\n=== Début du test de connexion ===")
            
            # Attendre que la page soit chargée
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            print("✓ Page de login chargée")
            
            # Find and fill email field
            email_input = driver.find_element(By.NAME, "email")
            email_input.clear()
            email_input.send_keys("admin@mail.com")
            print("✓ Email saisi: admin@admin.com")
            
            # Find and fill password field
            password_input = driver.find_element(By.NAME, "password")
            password_input.clear()
            password_input.send_keys("admin123")
            print("✓ Mot de passe saisi: admin123")
            
            # Vérifier que les champs sont bien remplis
            print(f"Valeur du champ email: {email_input.get_attribute('value')}")
            print(f"Valeur du champ password: {password_input.get_attribute('value')}")
            
            # Click submit button
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            print("✓ Bouton de connexion trouvé")
            submit_button.click()
            print("✓ Bouton de connexion cliqué")
            
            # Attendre un peu plus longtemps pour la redirection
            time.sleep(5)
            
            # Vérifier s'il y a des messages d'erreur
            try:
                error_messages = driver.find_elements(By.CSS_SELECTOR, "span.text-critical")
                if error_messages:
                    print(f"❌ Messages d'erreur trouvés: {[msg.text for msg in error_messages]}")
            except:
                print("✓ Aucun message d'erreur trouvé")
            
            # Vérifier l'URL actuelle
            current_url = driver.current_url
            print(f"URL actuelle: {current_url}")
            
            # Vérifier si nous sommes toujours sur la page de login
            if "login" in current_url.lower():
                # Vérifier si le formulaire est toujours présent
                try:
                    email_field = driver.find_element(By.NAME, "email")
                    print("❌ Formulaire de login toujours présent")
                except:
                    print("✓ Formulaire de login non trouvé")
                
                # Vérifier le contenu de la page
                page_source = driver.page_source
                if "Invalid email" in page_source:
                    print("❌ Message d'erreur 'Invalid email' trouvé dans la page")
                if "Invalid password" in page_source:
                    print("❌ Message d'erreur 'Invalid password' trouvé dans la page")
                
                pytest.fail(f"Still on login page. Current URL: {current_url}")
            
            print("=== Fin du test de connexion ===\n")
            
        except TimeoutException as e:
            pytest.fail(f"Timeout waiting for element: {str(e)}")
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    def test_invalid_email(self, driver):
        try:
            # Navigate to login page
            driver.get("http://10.21.6.26:3000/admin/login")
            
            # Attendre que la page soit chargée
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            
            # Find and fill email field with invalid email
            email_input = driver.find_element(By.NAME, "email")
            email_input.clear()
            email_input.send_keys("invalid-email")
            
            # Find and fill password field
            password_input = driver.find_element(By.NAME, "password")
            password_input.clear()
            password_input.send_keys("admin123")
            
            # Click submit button
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            
            # Wait for error message
            error_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.text-critical"))
            )
            
            # Verify error message
            assert "Invalid email" in error_message.text
            
            # Verify we're still on the login page
            assert "login" in driver.current_url.lower()
            
        except TimeoutException as e:
            pytest.fail(f"Timeout waiting for element: {str(e)}")
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")
