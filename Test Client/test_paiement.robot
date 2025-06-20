*** Settings ***
Library           Browser
Suite Setup       Open Browser To Login Page
Suite Teardown    Close Browser

*** Variables ***
${URL}            http://localhost:3000/
${EMAIL}          test2@test.com
${PASSWORD}       azerty

*** Test Cases ***
Connexion Et Paiement
    Remplir Formulaire De Connexion
    Valider Connexion
    Attendre Chargement Page Paiement
    Effectuer Paiement
    Vérifier Paiement Réussi

*** Keywords ***
Open Browser To Login Page
    New Browser    headless=false
    New Context
    New Page    ${URL}

Remplir Formulaire De Connexion
    Fill Text    input[name="email"]     ${EMAIL}
    Fill Text    input[name="password"]  ${PASSWORD}

Valider Connexion
    Click        button[type="submit"]

Attendre Chargement Page Paiement
    Wait For Elements State    text=Paiement    visible    timeout=10s

Effectuer Paiement
    # Adapter selon ta page
    Fill Text    input[name="card_number"]    4242 4242 4242 4242
    Fill Text    input[name="expiry_date"]    04/26
    Fill Text    input[name="cvc"]            287
    Click        button[name="payer"]         Place Order 

Vérifier Paiement Réussi
    Wait For Elements State    text=Paiement effectué avec succès    visible    timeout=10s
