from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os

def lambda_handler(event, context):
    options = Options()
    options.binary_location = '/opt/headless-chromium'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome('/opt/chromedriver',chrome_options=options)

    # Login Process
    driver.get("https://clublocker.com/login")
    driver.title # => "Google"
    driver.implicitly_wait(0.5)
    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.XPATH, "//*[@id='loginform']/div[4]/button")
    username.send_keys(os.environ.get('USERNAME'))
    password.send_keys(os.environ.get('PASSWORD'))
    login_button.click()
    driver.get("https://clublocker.com/clubs/2270/reservations")

    # Go 4 days in the future 
    time.sleep(2)
    driver.implicitly_wait(10)
    tomorrow_button = driver.find_element(By.XPATH, "//*[@id='mat-tab-content-0-1']/div/div/div/usq-reservation-grid/div/div[1]/mat-toolbar/div/button[2]")
    for i in range(0, 4):
        tomorrow_button.click()
        driver.implicitly_wait(10)
    time.sleep(4)
    
    # Find the time you want to reserve
    reserve_date_button = driver.find_element(By.XPATH, "/html/body/usq-club-locker-app/usq-club-profile/usq-profile/section/div/div/mat-card/mat-tab-group/div/mat-tab-body[2]/div/div/div/usq-reservation-grid/div/div[2]/div[2]/div[2]/div[3]/usq-reservation-grid-slot[12]/div")
    reserve_date_button.click()
    print("Found date")
    
    # Make the actual reservation
    book_button = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/mat-dialog-container/usq-reservation-edit-dialog/div/usq-reservation-edit/div[3]/div/button")
    book_button = driver.find_element(By.XPATH, "//*[@id='mat-dialog-0']/usq-reservation-edit-dialog/div/usq-reservation-edit/div[3]/div/button")
    book_button.click()
    print("Booked Time Sucessfully")
    time.sleep(5) # Keeps the browser open for a while
    
    driver.quit()

    response = {
        "statusCode": 200,
        "body": "Selenium Headless Chrome Initialized"
    }

    return response


