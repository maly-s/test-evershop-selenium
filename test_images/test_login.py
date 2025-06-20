import time

from selenium import webdriver



driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.

driver.get('http://localhost:3000/admin/login')

time.sleep(5) # Let the user actually see something!

driver.find_element(By.Name, 'email').send_keys('admin@mail.com')
driver.find_element(By.Name, 'password').send_keys('123456')

driver.find_element(By.CSS_SELECTOR, '.for-submit-button').find_element(By.CSS_SELECTOR)


time.sleep(5) # Let the user actually see something!

driver.find_elements(By.CSS_SELECTOR, '.flex justify-left')[4].click()

time.sleep(5)

driver.find_element(By.CSS_SELECTOR, '.button.primary').click()

driver.find_element(By.SS_SELECTOR, '#name').send_keys('Homme')
driver.find_element(By.SS_SELECTOR, '#urlKey').send_keys('homme')
driver.find_element(By.SS_SELECTOR, '.button.primary').click()

time.sleep(5)
