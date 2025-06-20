import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    time.sleep(2)
    driver.quit()

def test_categorie_supp(driver):
    nom_categorie = "Chat Test"

    print("Connexion à l'admin")
    driver.get("http://localhost:3000/admin")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "email"))
    ).send_keys("malyy@mail.com")

    driver.find_element(By.NAME, "password").send_keys("azertyuiopq1")
    driver.find_element(By.TAG_NAME, "button").click()

    print("Accès à la page des catégories")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href*="/admin/categories"]'))
    ).click()

    print("Attente du tableau des catégories")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "table"))
    )

    print("Recherche et sélection de la case à cocher pour la catégorie 'Chat Test'")
    lignes = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
    )

    selection_ok = False
    for ligne in lignes:
        if nom_categorie.lower() in ligne.text.lower():
            try:
                cellule_checkbox = ligne.find_element(By.CSS_SELECTOR, "td[style='width:2rem']")
                checkbox = cellule_checkbox.find_element(By.CSS_SELECTOR, "input[type='checkbox']")
                
                # Scroll vers la checkbox pour la rendre visible
                driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                time.sleep(0.2)

                if checkbox.is_displayed() and checkbox.is_enabled():
                    try:
                        checkbox.click()
                        print("Checkbox cliquée via .click()")
                        selection_ok = True
                        break
                    except Exception as e:
                        print(f"Échec click() direct : {e}")
                        checkbox.send_keys(Keys.SPACE)
                        print("Checkbox cochée via SPACE")
                        selection_ok = True
                        break
                else:
                    print("Checkbox non cliquable directement. Tentative clic sur label parent.")
                    labels = cellule_checkbox.find_elements(By.CSS_SELECTOR, "label")
                    for label in labels:
                        try:
                            label.click()
                            selection_ok = True
                            print("Checkbox cochée via clic sur label")
                            break
                        except Exception as e:
                            print(f"Échec clic sur label : {e}")
            except Exception as e:
                print(f"Erreur lors de la recherche ou du clic checkbox: {e}")

    if not selection_ok:
        print("Case non cochée")
        raise Exception(f"Case à cocher pour '{nom_categorie}' non trouvée.")

    print("➡️ Recherche du lien 'Delete' dans la barre d'action")
    liens = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td a"))
    )

    delete_trouve = False
    for lien in liens:
        spans = lien.find_elements(By.TAG_NAME, "span")
        for span in spans:
            if span.text.strip().lower() == "delete":
                lien.click()
                delete_trouve = True
                print("Lien 'Delete' cliqué")
                break
        if delete_trouve:
            break

    if not delete_trouve:
        raise Exception("Lien 'Delete' introuvable après sélection.")

    print("Confirmation du bouton 'Delete' dans la popup")
    try:
        bouton_delete = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.critical"))
        )
        span = bouton_delete.find_element(By.TAG_NAME, "span")
        if span.text.strip().lower() == "delete":
            bouton_delete.click()
            print("Suppression confirmée")
        else:
            raise Exception("Le bouton critique ne contient pas le texte 'Delete'")
    except Exception as e:
        raise Exception(f"Bouton 'Delete' de confirmation non trouvé ou non cliquable: {e}")

    print("➡️ Vérification finale que la catégorie a été supprimée")
    WebDriverWait(driver, 5).until(EC.url_contains("/admin/categories"))
    time.sleep(1)
    driver.refresh()
    time.sleep(1)

    elements = driver.find_elements(By.LINK_TEXT, nom_categorie)
    assert len(elements) == 0, f"La catégorie '{nom_categorie}' est toujours présente."
    print(f"🎉 Catégorie '{nom_categorie}' supprimée avec succès.")
