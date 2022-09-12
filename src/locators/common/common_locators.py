from selenium.webdriver.common.by import By


class CommonLocators:
    ITEMS_COUNTER = (By.CSS_SELECTOR, '[class="ml-2"]')
    SEARCH_INPUT = (By.CSS_SELECTOR, '[class*="type-zone"]')
    CLEAR_SEARCH_INPUT = (By.CSS_SELECTOR, '[class^="text-muted"]')
