from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import platform
import os

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    
    # Configuration spécifique pour macOS ARM64
    if platform.system() == 'Darwin' and platform.machine() == 'arm64':
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-software-rasterizer')
        
        # Chemin vers Chrome sur Mac
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.exists(chrome_path):
            chrome_options.binary_location = chrome_path
    
    # Utiliser le driver directement
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def get_base_url():
    return "https://www.evershop.io/"  # URL de base pour les tests

#voici le dossier de config pour ouvrir le navigateur pour mes tests avec selenium
#rajoute la fonction qui me permet d'ouvrir l'url