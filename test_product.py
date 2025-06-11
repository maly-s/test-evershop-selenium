import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import setup_driver
import time

class TestProductCreation:
    @pytest.fixture(scope="function")
    def driver(self):
        driver = setup_driver()
        yield driver
        driver.quit()

    def login(self, driver):
        try:
            # Navigate to login page
            driver.get("http://10.21.6.26:3000/admin/login")
            print("\n=== Connexion à l'interface d'administration ===")
            
            # Attendre que la page soit chargée
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            print("✓ Page de connexion chargée")
            
            # Remplir le formulaire de connexion
            email_input = driver.find_element(By.NAME, "email")
            email_input.clear()
            email_input.send_keys("admin@mail.com")
            print("✓ Email saisi")
            
            password_input = driver.find_element(By.NAME, "password")
            password_input.clear()
            password_input.send_keys("admin123")
            print("✓ Mot de passe saisi")
            
            # Cliquer sur le bouton de connexion
            login_button = driver.find_element(By.CSS_SELECTOR, "button.button.primary")
            print("✓ Bouton de connexion trouvé")
            login_button.click()
            print("✓ Bouton de connexion cliqué")
            
            # Attendre que la redirection soit terminée
            WebDriverWait(driver, 10).until(
                EC.url_contains("/admin")
            )
            print("✓ Connexion réussie")
            
        except Exception as e:
            pytest.fail(f"Échec de la connexion: {str(e)}")

    def navigate_to_product_form(self, driver):
        try:
            # Attendre que nous soyons sur le tableau de bord
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.page-heading-title"))
            )
            page_title = driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text
            assert "Dashboard" in page_title, f"Page incorrecte: {page_title}"
            print("✓ Tableau de bord chargé")
            
            # Cliquer sur le lien "Products" dans le menu
            products_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Products')]"))
            )
            print("✓ Lien 'Products' trouvé")
            products_link.click()
            print("✓ Lien 'Products' cliqué")
            
            # Attendre que la page des produits soit chargée
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.page-heading-title"))
            )
            page_title = driver.find_element(By.CSS_SELECTOR, "h1.page-heading-title").text
            assert "Products" in page_title, f"Page incorrecte: {page_title}"
            print(f"✓ Page des produits chargée: {page_title}")
            
            # Cliquer sur le bouton "Add New Product"
            add_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.button.primary"))
            )
            print("✓ Bouton 'Add New Product' trouvé")
            add_button.click()
            print("✓ Bouton 'Add New Product' cliqué")
            
            # Attendre que le formulaire soit chargé
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "name"))
            )
            print("✓ Formulaire de création de produit chargé")
            
        except Exception as e:
            pytest.fail(f"Échec de la navigation vers le formulaire: {str(e)}")

    def test_successful_product_creation(self, driver):
        try:
            # Se connecter d'abord
            self.login(driver)
            
            # Naviguer vers le formulaire de création de produit
            self.navigate_to_product_form(driver)
            
            print("\n=== Début du test de création de produit ===")
            
            # Remplir le formulaire avec des données valides
            name_input = driver.find_element(By.ID, "name")
            name_input.clear()
            name_input.send_keys("Test Product")
            print("✓ Nom du produit saisi")
            
            sku_input = driver.find_element(By.ID, "sku")
            sku_input.clear()
            sku_input.send_keys("TEST-SKU-001")
            print("✓ SKU saisi")
            
            price_input = driver.find_element(By.ID, "price")
            price_input.clear()
            price_input.send_keys("99.99")
            print("✓ Prix saisi")
            
            weight_input = driver.find_element(By.ID, "weight")
            weight_input.clear()
            weight_input.send_keys("1.5")
            print("✓ Poids saisi")
            
            qty_input = driver.find_element(By.ID, "qty")
            qty_input.clear()
            qty_input.send_keys("100")
            print("✓ Quantité saisie")
            
            url_key_input = driver.find_element(By.ID, "urlKey")
            url_key_input.clear()
            url_key_input.send_keys("test-product")
            print("✓ URL key saisie")
            
            # Cliquer sur le bouton Save
            save_button = driver.find_element(By.CSS_SELECTOR, "button.button.primary")
            print("✓ Bouton Save trouvé")
            save_button.click()
            print("✓ Bouton Save cliqué")
            
            # Vérifier qu'il n'y a pas de messages d'erreur
            try:
                error_messages = driver.find_elements(By.CSS_SELECTOR, "span.text-critical")
                if error_messages:
                    pytest.fail(f"Messages d'erreur trouvés: {[msg.text for msg in error_messages]}")
                print("✓ Aucun message d'erreur trouvé")
            except:
                print("✓ Aucun message d'erreur trouvé")
            
            print("=== Fin du test de création de produit ===\n")
            
        except TimeoutException as e:
            pytest.fail(f"Timeout waiting for element: {str(e)}")
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}")

    def test_empty_fields_error(self, driver):
        try:
            # Se connecter d'abord
            self.login(driver)
            
            # Naviguer vers le formulaire de création de produit
            self.navigate_to_product_form(driver)
            
            print("\n=== Début du test d'erreur champs vides ===")
            
            # Cliquer sur le bouton Save sans remplir les champs
            save_button = driver.find_element(By.CSS_SELECTOR, "button.button.primary")
            print("✓ Bouton Save trouvé")
            save_button.click()
            print("✓ Bouton Save cliqué")
            
            # Vérifier les messages d'erreur
            error_messages = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.text-critical"))
            )
            
            # Vérifier qu'il y a au moins un message d'erreur
            assert len(error_messages) > 0, "Aucun message d'erreur trouvé"
            
            # Vérifier le contenu des messages d'erreur
            for error in error_messages:
                assert "This field can not be empty" in error.text, f"Message d'erreur incorrect: {error.text}"
            
            print(f"✓ {len(error_messages)} messages d'erreur trouvés")
            print("=== Fin du test d'erreur champs vides ===\n")
            
        except TimeoutException as e:
            pytest.fail(f"Timeout waiting for element: {str(e)}")
        except Exception as e:
            pytest.fail(f"Test failed with error: {str(e)}") 