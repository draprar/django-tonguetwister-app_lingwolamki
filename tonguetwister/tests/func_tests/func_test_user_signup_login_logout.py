import os
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class SignupLoginLogoutTest(unittest.TestCase):

    def setUp(self):
        # Initialize the Chrome driver and maximize the browser window
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_signup_login_logout(self):
        # Open application homepage
        self.driver.get("http://127.0.0.1:8000/")

        # Sign up for an account
        self.driver.find_element(By.LINK_TEXT, "Rejestracja").click()
        self.driver.find_element(By.NAME, "username").send_keys("testuser")
        self.driver.find_element(By.NAME, "email").send_keys("test@user.com")
        self.driver.find_element(By.NAME, "password1").send_keys("password123")
        self.driver.find_element(By.NAME, "password2").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.driver.find_element(By.ID, "back-registration").click()

        # Log in with the new account
        self.driver.find_element(By.LINK_TEXT, "Logowanie").click()
        self.driver.find_element(By.NAME, "username").send_keys("test")
        self.driver.find_element(By.NAME, "password").send_keys("Qwerty100!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Verify that the settings button is not visible for standard users
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "button[aria-label='settings']"))
            )
            settings_not_visible = True
        except TimeoutException:
            settings_not_visible = False

        self.assertTrue(settings_not_visible, "Settings button is visible")

        # Log out from the application
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.LINK_TEXT, "Wyloguj"))
        )
        self.driver.find_element(By.LINK_TEXT, "Wyloguj").click()

    def test_signup_login_logout_mobile(self):
        # Open application homepage in mobile view
        self.driver.get("http://127.0.0.1:8000/")
        self.driver.set_window_size(375, 667)

        # Sign up for an account
        self.driver.find_element(By.CSS_SELECTOR, "a[aria-label='register']").click()
        self.driver.find_element(By.NAME, "username").send_keys("mobileuser")
        self.driver.find_element(By.NAME, "email").send_keys("test@user.com")
        self.driver.find_element(By.NAME, "password1").send_keys("password123")
        self.driver.find_element(By.NAME, "password2").send_keys("password123")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        self.driver.find_element(By.ID, "back-registration").click()

        # Verify that the settings button is not visible for standard users
        try:
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, "button[aria-label='settings']"))
            )
            settings_not_visible = True
        except TimeoutException:
            settings_not_visible = False

        self.assertTrue(settings_not_visible, "Settings button is visible")

        # Log in with the new account
        self.driver.find_element(By.CSS_SELECTOR, "a[aria-label='login']").click()
        self.driver.find_element(By.NAME, "username").send_keys("test")
        self.driver.find_element(By.NAME, "password").send_keys("Qwerty100!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Log out from the application
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "a[aria-label='logout']"))
        )
        self.driver.find_element(By.CSS_SELECTOR, "a[aria-label='logout']").click()

    def tearDown(self):
        # Close the browser session
        self.driver.quit()


if __name__ == "__main__":
    # Define output directory and file for test results
    test_dir = os.path.join(os.getcwd(), 'tests_outcomes')
    os.makedirs(test_dir, exist_ok=True)
    test_outcome_file = os.path.join(test_dir, 'test_user_signup_login_logout_outcome.txt')

    # Run tests and save results to a file
    with open(test_outcome_file, 'w') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        result = unittest.main(testRunner=runner, exit=False)

    print(f"Test results written to {test_outcome_file}")
