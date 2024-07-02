from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import date

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 100)

driver.get('https://my.rotary.org/en/login?destination=/district/671948d6-9f76-4698-acde-3ee3c65679f4/clubs')
submit_btn = wait.until(EC.element_to_be_clickable((By.ID, 'okta-signin-submit')))

username = driver.find_element(By.ID, 'okta-signin-username')
password = driver.find_element(By.ID, 'okta-signin-password')

username.clear()
password.clear()
username.send_keys('nimna.rotaract3220@gmail.com')
password.send_keys('@T9q8G5efDDn')

submit_btn.click()

dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="dropdown"]')))
dropdown.click()

checkboxeses = wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//div[@data-testid="option"]//div[2]//div')))
for cb in checkboxeses:
    if 'rotaract' in cb.text.lower():
        cb.click()

apply_btn = driver.find_element(By.XPATH, '//button[@data-testid="apply-button"]')
apply_btn.click()

data = []

while True:
    next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@data-testid="pagination-next-btn"]')))

    rows = driver.find_elements(By.XPATH, '//div[@data-testid="result-row"]')
    for row in rows:
        name_element = row.find_element(By.CLASS_NAME, 'result-info__name')
        count_element = row.find_element(By.CLASS_NAME, 'result-memberships')
        data.append([name_element.text, count_element.text.replace(' Active members', '')])

    if 'pointer-events-none' in next_btn.get_attribute('class').lower():
        break

    next_btn.click()

today = date.today()
data_csv = pd.DataFrame(data, columns=['club', 'members'])
data_csv.to_csv(f'RI Active members list-{today}.csv', index=False)




