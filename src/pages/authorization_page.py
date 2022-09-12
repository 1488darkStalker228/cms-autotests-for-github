from src.base_classes.selenium_base import SeleniumBase
from src.locators.authorization.authorization_page_locators import AuthorizationPageLocators


class AuthorizationPage(SeleniumBase):

    def fill_fields_and_login(self) -> None:
        email = 'konstantin88178@gmail.com'
        password = 'j9Nu7Bm6'
        self.is_visible(AuthorizationPageLocators.EMAIL).send_keys(email)
        self.is_visible(AuthorizationPageLocators.PASSWORD).send_keys(password)
        self.is_visible(AuthorizationPageLocators.LOGIN_BUTTON).click()