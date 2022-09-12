from selenium.webdriver.common.by import By


class AuthorizationPageLocators:
    EMAIL = (By.CSS_SELECTOR, '[id="username"]')
    PASSWORD = (By.CSS_SELECTOR, '[id="password"]')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '[name="button"]')

