from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from utils import check_whether_medicals_are_expired_or_will_expire_in_14_days, when_medicals_are_expiring, to_title_string, name_decantation

class SelPortalHelper:
    def log_in_to_sel(self, cielo_athletes, marcins_athletes, elas_athletes):
        coaches = []
        cielo_expiration_dates = {}
        marcins_expiration_dates = {}
        elas_expiration_dates = {}

        service = Service('/usr/lib/chromium-browser/chromedriver')
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--window-size=1920x1080')
        options.binary_location = "/usr/bin/chromium-browser"
        driver = webdriver.Chrome(service=service, options=options)
        driver.get("https://l2.polswim.pl/user")
        time.sleep(1)

        insert_email = driver.find_element(By.CSS_SELECTOR, "input#edit-name.form-control.form-text.required")
        insert_email.send_keys("slawek.plonka@onet.pl")
        
        insert_password = driver.find_element(By.CSS_SELECTOR, "input#edit-pass.form-control.form-text.required")
        insert_password.send_keys("Zosia2004")
        
        login_button = driver.find_element(By.CSS_SELECTOR, "button#edit-submit.btn.btn-default.form-submit")
        login_button.click()
        time.sleep(2)

        driver.get("https://l2.polswim.pl/my_club/zawodnicy")
        time.sleep(2)

        athletes_names = driver.find_elements(By.CSS_SELECTOR, "td.views-field.views-field-title")
        medical = driver.find_elements(By.CSS_SELECTOR, "td.views-field.views-field-field-competitor-medical")

        for i in range(len(athletes_names)):
            medical_date = medical[i].find_element(By.CSS_SELECTOR, "span.date-display-single").text.strip()
            if check_whether_medicals_are_expired_or_will_expire_in_14_days(medical_date):
                athlete_name = athletes_names[i].find_element(By.CSS_SELECTOR, "a").text.strip()
                
                if athlete_name in cielo_athletes:
                    cielo_expiration_dates[athlete_name] = when_medicals_are_expiring(medical_date)
                elif athlete_name in marcins_athletes:
                    marcins_expiration_dates[athlete_name] = when_medicals_are_expiring(medical_date)
                elif athlete_name in elas_athletes:
                    elas_expiration_dates[athlete_name] = when_medicals_are_expiring(medical_date)

        coaches.append(cielo_expiration_dates)
        coaches.append(marcins_expiration_dates)
        coaches.append(elas_expiration_dates)

        driver.quit()
        return coaches
