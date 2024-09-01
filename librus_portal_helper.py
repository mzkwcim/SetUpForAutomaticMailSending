from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

class LibrusPortalHelper:
    def __init__(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--window-size=1920x1080')
        service = Service('/usr/lib/chromium-browser/chromedriver')
        self.driver = webdriver.Chrome(service=service, options=options)

    def log_in(self, username, password):
        self.driver.get("https://portal.librus.pl/szkola/synergia/loguj")
        time.sleep(0.5)

        try:
            self.driver.find_element(By.CSS_SELECTOR, "button.modal-button__primary[data-modal-submit-all='']").click()
        except NoSuchElementException:
            print("Cookie files Acceptance button hasn't been found")

        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, "a.btn-synergia-top.btn-navbar.d-none.d-lg-block").click()
        time.sleep(0.5)

        # Przełączenie się do iframe
        self.driver.switch_to.frame(self.driver.find_element(By.ID, "caLoginIframe"))

        self.driver.find_element(By.CSS_SELECTOR, "input#Login.form-control").send_keys(username)
        self.driver.find_element(By.ID, "Pass").send_keys(password)
        self.driver.find_element(By.ID, "LoginBtn").click()

        time.sleep(0.5)
        self.driver.switch_to.default_content()
        time.sleep(0.5)
        self.driver.find_element(By.XPATH, "//*[@id='centrumPowiadomien']/div[2]/div[1]/span[2]").click()

    def send_message(self, recipient, subject, message):
        time.sleep(0.5)
        self.driver.get(self.driver.find_element(By.CSS_SELECTOR, "a#icon-wiadomosci").get_attribute("href"))
        time.sleep(0.5)
        self.driver.get(self.driver.find_element(By.CSS_SELECTOR, "a#wiadomosci-napisz.button.left.blue").get_attribute("href"))

        self.driver.find_element(By.ID, "radio_rodzic_klasami").click()
        time.sleep(0.5)

        # Wybór odbiorcy wiadomości
        self.driver.find_element(By.XPATH, "//*[@id='adresaci']/table/tbody/tr[45]/td[3]/input").click()
        self.driver.find_element(By.XPATH, "//*[@id='adresaci']/table/tbody/tr[49]/td[3]/input").click()
        time.sleep(0.5)

        label_elements = self.driver.find_elements(By.XPATH, "//table//label")
        for label_element in label_elements:
            if recipient in label_element.text:
                for_value = label_element.get_attribute("for")
                checkbox_element = self.driver.find_element(By.ID, for_value)
                if checkbox_element and checkbox_element.is_enabled():
                    checkbox_element.click()
                    break

        time.sleep(0.5)
        self.driver.find_element(By.CSS_SELECTOR, "input#temat.stretch").send_keys(subject)
        self.driver.find_element(By.CSS_SELECTOR, "textarea#tresc_wiadomosci.stretch").send_keys(message)
        time.sleep(0.5)
        # Kliknięcie przycisku wysyłania wiadomości (możesz odkomentować poniższą linię, aby faktycznie wysłać wiadomość)
        # self.driver.find_element(By.CSS_SELECTOR, "input#sendButton.medium.ui-button.ui-widget.ui-state-default.ui-corner-all").click()

    def close(self):
        self.driver.quit()

# Przykład użycia
if __name__ == "__main__":
    librus_helper = LibrusPortalHelper()
    librus_helper.log_in("twoj_login", "twoje_haslo")
    librus_helper.send_message("Imię Nazwisko", "Temat wiadomości", "Treść wiadomości")
    librus_helper.close()
