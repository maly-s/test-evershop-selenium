import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    time.sleep(2)
    driver.quit()


def test_creation_categorie(driver):
    nom_categorie = "Chat Test"
    url_key = "azerty12"

    print("➡️ Ouverture du back-office")
    driver.get("http://localhost:3000/admin")

    print("➡️ Remplissage du formulaire de connexion")
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "email"))).send_keys("malyy@mail.com")
    driver.find_element(By.NAME, "password").send_keys("azertyuiopq1")

    print("➡️ Cliquer sur le bouton de connexion")
    buttons = driver.find_elements(By.TAG_NAME, "button")
    for btn in buttons:
        if btn.is_displayed() and btn.is_enabled():
            btn.click()
            break
    else:
        raise Exception("Bouton de connexion introuvable")

    print("➡️ Attente du dashboard")
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))

    print("➡️ Aller à la page des catégories")
    WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href*="/admin/categories"]'))
    ).click()

    time.sleep(1)  # laisse la liste se charger

    print(f"➡️ Vérifier si la catégorie '{nom_categorie}' existe")
    categories = driver.find_elements(By.LINK_TEXT, nom_categorie)
    if categories:
        print(f"✅ La catégorie '{nom_categorie}' existe déjà, fin du test.")
        return

    print(f"ℹ️ Catégorie '{nom_categorie}' absente, création...")

    print("➡️ Cliquer sur le lien 'New Category'")
    new_cat_links = driver.find_elements(By.CSS_SELECTOR, 'a.button.primary')
    for link in new_cat_links:
        if "New Category" in link.text:
            link.click()
            break
    else:
        raise Exception("Lien 'New Category' introuvable")

    print("➡️ Remplir le formulaire de nouvelle catégorie")
    name_input = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "name")))
    name_input.send_keys(nom_categorie)

    url_input = driver.find_element(By.ID, "urlKey")
    url_input.send_keys(url_key)

    print("➡️ Cliquer sur le bouton 'Save'")
    save_buttons = driver.find_elements(By.CSS_SELECTOR, 'button.button.primary')
    for btn in save_buttons:
        if "Save" in btn.text:
            btn.click()
            break
    else:
        raise Exception("Bouton 'Save' introuvable")

    print("➡️ Attente que la catégorie apparaisse dans la liste")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, nom_categorie)))
    print(f"✅ Catégorie '{nom_categorie}' créée avec succès.")
