from selenium.webdriver.support import expected_conditions as e_c
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome import webdriver


class SeleniumBase:
    def __init__(self, driver: webdriver, url: str = None) -> None:
        self.driver = driver
        self.url = url
        self.__wait = WebDriverWait(driver, 5)

    def open(self) -> None:
        self.driver.get(self.url)

    def is_visible(self, locator: tuple[str, str], locator_name: str = None) -> WebElement:
        return self.__wait.until(e_c.visibility_of_element_located(locator), locator_name)

    def is_present(self, locator: tuple[str, str], locator_name: str = None) -> WebElement:
        return self.__wait.until(e_c.presence_of_element_located(locator), locator_name)

    # Возможно, возвращает не то, что описано в методе;
    def is_not_present(self, locator: tuple[str, str], locator_name: str = None) -> WebElement:
        return self.__wait.until(e_c.invisibility_of_element_located(locator), locator_name)

    def are_visible(self, locator: tuple[str, str], locator_name: str = None) -> list[WebElement]:
        return self.__wait.until(e_c.visibility_of_all_elements_located(locator), locator_name)

    def are_present(self, locator: tuple[str, str], locator_name: str = None) -> list[WebElement]:
        return self.__wait.until(e_c.presence_of_all_elements_located(locator), locator_name)

    def go_to_element(self, element: WebElement) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
