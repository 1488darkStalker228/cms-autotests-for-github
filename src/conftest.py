import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.pages.authorization_page import AuthorizationPage
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


@pytest.fixture
def get_chrome_options():
    options = chrome_options()
    # options.add_argument('headless')
    options.add_argument('chrome')
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1920,1080')
    return options


@pytest.fixture
def get_webdriver(get_chrome_options):
    #driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub', DesiredCapabilities.CHROME)
    driver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=get_chrome_options, service=driver_service, port=4444)
    return driver


@pytest.fixture
def setup(request, get_webdriver):
    driver = get_webdriver
    if request.cls is not None:
        request.cls.driver = driver
    yield driver
    driver.quit()


@pytest.fixture
def authorization(get_webdriver):
    authorization_page = AuthorizationPage(get_webdriver, 'https://cms-test.cubicservice.ru/')
    authorization_page.open()
    authorization_page.fill_fields_and_login()
