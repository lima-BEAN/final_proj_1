import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class FeastFreedomHomeSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.FireFox

    def test_search_in_feastfreedom(self):
        driver = self.driver
        driver.get("http://100.24.4.172/")
        self.assertIn("FeastFreedom Home Page", driver.title)
        #TODO: read DOCS: https://selenium-python.readthedocs.io/getting-started.html#simple-usage
        # elem = driver.find_element_by_name("q")
        # elem.send_keys("pycon")
        # elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

class FeastFreedomKitchenSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.FireFox
"""
    def test_search_in_feastfreedom_kitchen(self):
        driver = self.driver
        driver.get("http://0.0.0.0:8000/kitchen")
        self.assertIn("Kitchen App List Page", driver.title)
        #TODO: read DOCS: https://selenium-python.readthedocs.io/getting-started.html#simple-usage
        # elem = driver.find_element_by_name("q")
        # elem.send_keys("pycon")
        # elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

    def test_search_in_feastfreedom_kitchen_detail(self):
        driver = self.driver
        #driver.get("http://100.24.4.172/kitchen/1")
        driver.get("http://0.0.0.0:8000/kitchen/1")
        self.assertIn("Kitchen App Detail Page", driver.title)
        assert "No results found." not in driver.page_source

    def test_search_in_feastfreedom_kitchen_create(self):
        driver = self.driver
        #driver.get("http://100.24.4.172/kitchen/create")
        driver.get("http://0.0.0.0:8000/kitchen/create")
        self.assertIn("Kitchen App Create Page", driver.title)
        assert "No results found." not in driver.page_source

    def test_search_in_feastfreedom_kitchen_update(self):
        driver = self.driver
        #driver.get("http://100.24.4.172/kitchen/1/update")
        driver.get("http://0.0.0.0:8000/kitchen/1/update")
        self.assertIn("Kitchen App Update Page", driver.title)
        assert "No results found." not in driver.page_source

    def test_search_in_feastfreedom_kitchen_delete(self):
        driver = self.driver
        #driver.get("http://100.24.4.172/kitchen/1/delete")
        driver.get("http://0.0.0.0:8000/kitchen/1/delete")
        self.assertIn("Kitchen App Delete Page", driver.title)
        assert "No results found." not in driver.page_source

    def tearDown(self):
        self.driver.close()
"""

if __name__ == "__main__":
    unittest.main()