import unittest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


class SearchText(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get("http://10.10.0.255:5000/")

    def test_search(self):
        self.search_field = self.driver.find_element(By.ID, "city")
        self.search_field.send_keys("Chicago")
        self.search_field.submit()
        bodyText = self.driver.find_element(By.TAG_NAME, 'h1').text
        self.assertIn("Day and Night Temperatures for the next 7 days", bodyText)

    def test_error(self):
        self.search_field = self.driver.find_element(By.ID, "city")
        self.search_field.send_keys("hdfgadsg")
        self.search_field.submit()
        bodyText = self.driver.find_element(By.TAG_NAME, 'h1').text
        self.assertIn("Sorry!", bodyText)


    def tearDown(self):
        self.driver.quit()


class test_flaskapp(unittest.TestCase):
    def test_active(self):
        url = requests.head("http://10.10.0.255:5000/")
        self.assertEqual(url.status_code, 200)


if __name__ == "__main__":
    unittest.main()
