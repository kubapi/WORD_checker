from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# used in make beep function to make sound 
import winsound
import time
import datetime


def make_beep():
    frequency = 2500
    duration = 100
    for i in range(1,10):
        winsound.Beep(frequency, duration)
        time.sleep(0.5/i)

def text_to_date(text):
    return int(text.split(" ")[1].split(".")[0])
 

def wait_for_clickable_and_click(driver, xpath, timeout = 20):
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    # using js executor
    driver.execute_script("arguments[0].click();", element)

def get_status(email, password): 
    driver.get("https://info-car.pl/new/prawo-jazdy/sprawdz-wolny-termin")

    # click login button
    wait_for_clickable_and_click(driver, "/html/body/app-root/app-layout/app-check-exam-availability/div/main/app-exam-availability-exam-center-step/div/ic-ghost-button/button/div/span")

    # send email
    driver.find_element_by_xpath("//*[@id='username']").send_keys(email)
    # send password
    driver.find_element_by_xpath("//*[@id='password']").send_keys(password)
    # click login button
    wait_for_clickable_and_click(driver, "//*[@id='register-button']")

    # select Mazowieckie
    wait_for_clickable_and_click(driver, "//*[@id='province']")
    wait_for_clickable_and_click(driver, "//*[@id='mazowieckie']")
    # select Radarowa
    wait_for_clickable_and_click(driver, "//*[@id='organization']")
    wait_for_clickable_and_click(driver, "//*[@id='word-warszawa m/e radarowa']")
    # select B
    wait_for_clickable_and_click(driver, "//*[@id='category-select']")
    wait_for_clickable_and_click(driver, "//*[@id='b']")
    # click continue 
    wait_for_clickable_and_click(driver, "/html/body/app-root/app-layout/app-check-exam-availability/div/main/app-exam-availability-exam-center-step/section[2]/div/ic-ghost-button/button")

    #select practical exam (using js executor to overpass)
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='practical-container']/input").send_keys(Keys.ENTER);
    time.sleep(2)

    result = driver.find_element_by_xpath("//*[@id='ngb-panel-0-header']/div[2]/h5").text
    driver.close()
    return text_to_date(result)

def login():
    print("Dane wymagane są do zalogowania się na stronie! Nie martw się nigdzie nie są przechowywane.")
    email = input("Podaj email do swojego konta:")
    password = input("Podaj hasło do swojego konta:")
    return email, password

# get login details
email, password = login()
current_best = 22

# setup webdriver with loggin switch excluded 
options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)

while(True):
    try:
        result = get_status(email, password)
        if current_best > result:
            current_best = result
            make_beep()
    except:
        time.sleep(60)
