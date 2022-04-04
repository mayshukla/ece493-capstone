import os
import subprocess
import time
import unittest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from webdriver_manager.utils import ChromeType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class TestFrontend(unittest.TestCase):
    TIMEOUT = 3

    @classmethod
    def setUpClass(cls):
        # Save webdriver binaries to test/.wdm
        os.environ['WDM_LOCAL'] = '1'
        # Install chromium webdriver (if not already installed)
        cls.driver_manager = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()

        # Run server
        cls.server_process = subprocess.Popen(["python3", "-m", "src", "9000"])

    @classmethod
    def tearDownClass(cls):
        # Stop server and wait for the process to terminate
        cls.server_process.terminate()
        cls.server_process.wait()

    def setUp(self):
        # Wait for server to start up
        time.sleep(2)

        # Open 2 browsers
        options = Options()
        # Must run headless for chromedriver to work in github actions
        options.headless = True
        self.drivers = []
        for _ in range(2):
            self.drivers.append(webdriver.Chrome(service=Service(TestFrontend.driver_manager), options=options))
        for driver in self.drivers:
            driver.get("http://localhost:9000")

    def tearDown(self):
        # Close browsers
        for driver in self.drivers:
            driver.quit()

    def test_exception_during_game(self):
        code_area = WebDriverWait(self.drivers[0], timeout=TestFrontend.TIMEOUT).until(lambda d: d.find_element(By.ID, "codeArea"))
        code_area.clear()
        code_area.send_keys("""
class MyAgent(Agent):
    def run(self):
        raise ValueError()
        """)

        for driver in self.drivers:
            submit_button = driver.find_element(By.ID, "submitButton")
            submit_button.click()

        # Expect to see "ValueError" in pythonErrorsArea
        wait = WebDriverWait(self.drivers[0], timeout=TestFrontend.TIMEOUT)
        wait.until(EC.text_to_be_present_in_element((By.ID, "pythonErrorsArea"), "ValueError"))

        for driver in self.drivers:
            wait = WebDriverWait(driver, timeout=TestFrontend.TIMEOUT)
            wait.until(EC.text_to_be_present_in_element((By.ID, "declareErrorArea"), "Game ended due to error in player code."))

        # Player 0 should be the loser
        wait = WebDriverWait(self.drivers[0], timeout=TestFrontend.TIMEOUT)
        wait.until(EC.text_to_be_present_in_element((By.ID, "declareWinnerArea"), "You Lost, Better Luck Next Time!"))

        # Player 1 should be the winner
        wait = WebDriverWait(self.drivers[1], timeout=TestFrontend.TIMEOUT)
        wait.until(EC.text_to_be_present_in_element((By.ID, "declareWinnerArea"), "You Win, Congratulations!"))

    def test_exception_during_code_submission(self):
        code_area = WebDriverWait(self.drivers[0], timeout=TestFrontend.TIMEOUT).until(lambda d: d.find_element(By.ID, "codeArea"))
        code_area.clear()
        code_area.send_keys("""
class MyAgent(Agent):
    def run(self):
improper syntax!!!
        """)
        submit_button = self.drivers[0].find_element(By.ID, "submitButton")
        submit_button.click()
        # Expect to see "IndentationError" in pythonErrorsArea
        wait = WebDriverWait(self.drivers[0], timeout=TestFrontend.TIMEOUT)
        wait.until(EC.text_to_be_present_in_element((By.ID, "pythonErrorsArea"), "IndentationError"))

    def test_completed_game(self):
        pass


if __name__ == '__main__':
    unittest.main()