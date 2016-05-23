import time
from selenium import webdriver
home_page = 'https://solrates.herokuapp.com'
o = 'https://www.upwork.com/jobs/_~01d1e3d8921a520bbb/'
UPPER_BOUND_WAIT_TIME = 20 * 60
sleep_until_wait_for_changing_status = 20


class AbstractTest(object):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.start_client()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.close()


class CloudTest(AbstractTest):
    def setUp(self):
        super(CloudTest, self).setUp()

    def tearDown(self):
        super(CloudTest, self).tearDown()


def test_login():
    cloud = CloudTest()
    cloud.setUp()
    cloud.driver.get(home_page)
    time.sleep(5)
