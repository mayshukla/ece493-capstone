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
        if not "GUI" in os.environ or os.environ['GUI'] == "":
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

    def get_code_from_file(self, filename):
        with open(filename) as f:
            contents = f.read()
        return contents

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
        """This test can be run in headed mode with the following command:
        GUI=1 python -m unittest test.test_frontend.TestFrontend.test_completed_game
        """
        agent_code = [
            self.get_code_from_file("test/agent_code/agent1.py"),
            self.get_code_from_file("test/agent_code/agent2.py"),
        ]
        agent_names = [
            "Agent1",
            "Agent2",
        ]
        for i in range(len(self.drivers)):
            code_area = WebDriverWait(self.drivers[i], timeout=TestFrontend.TIMEOUT).until(lambda d: d.find_element(By.ID, "codeArea"))
            code_area.clear()
            code_area.send_keys(agent_code[i])

            class_name_area = self.drivers[i].find_element(By.ID, "classNameArea")
            class_name_area.clear()
            class_name_area.send_keys(agent_names[i])

        for driver in self.drivers:
            submit_button = driver.find_element(By.ID, "submitButton")
            submit_button.click()

        wait = WebDriverWait(self.drivers[0], timeout=60)
        wait.until(EC.text_to_be_present_in_element((By.ID, "declareWinnerArea"), "You Lost, Better Luck Next Time!"))

        wait = WebDriverWait(self.drivers[1], timeout=60)
        wait.until(EC.text_to_be_present_in_element((By.ID, "declareWinnerArea"), "You Win, Congratulations!"))


if __name__ == '__main__':
    unittest.main()