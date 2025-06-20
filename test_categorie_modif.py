import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    time.sleep(2)
    driver.quit()


def test_modifier_categorie(driver):
    # 1. Accès au back-office
    driver.get("http://localhost:3000/admin")

    # 2. Connexion admin
    driver.find_element(By.NAME, "email").send_keys("malyy@mail.com")
    driver.find_element(By.NAME, "password").send_keys("azertyuiopq1")
    driver.find_element(By.TAG_NAME, "button").click()

    # 3. Attente des liens visibles
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

    # 4. Cliquer sur lien contenant "Categories"
    links = driver.find_elements(By.TAG_NAME, "a")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href*="/admin/categories"]'))
    ).click()
    print("Lien 'Categories' cliqué via href.")

    # 5. Attendre et cliquer sur "Chat Test"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Chat Test")))
    driver.find_element(By.LINK_TEXT, "Chat Test").click()

      # 7. Upload image
    image_input = driver.find_element(By.ID, "categoryImageUpload")

    image_path = os.path.abspath("chat copie.jpg")
    assert os.path.exists(image_path), f"Image introuvable : {image_path}"
    image_input.send_keys(image_path)

    # 6. Modifier champ url_key
    url_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "urlKey")))
    url_input.clear()
    url_input.send_keys("brsghir765")

    # 8. Cliquer sur bouton "Save"
    buttons = driver.find_elements(By.CLASS_NAME, "button")
    for btn in buttons:
        if btn.text.strip().lower() == "save":
            btn.click()
            break
    else:
        pytest.fail("Bouton 'Save' non trouvé")

    # 9. Vérifier retour à la liste des catégories
    WebDriverWait(driver, 10).until(EC.url_contains("/admin/categories"))




  
