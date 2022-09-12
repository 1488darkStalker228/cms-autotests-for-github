from selenium.webdriver.common.by import By


class ComparePlaylistsPageLocators:
    COMPARE_BUTTON = (By.XPATH, '/html/body/main/section/div[2]/div[2]/main/section/button')
    PLAYLISTS_ITEMS = (By.CSS_SELECTOR, 'tbody>a')
    FIRST_TABLE_ITEMS_FOR_CHECK = (By.CSS_SELECTOR, '[class="grid_item"]:first-child tbody>a>div:first-child')
    SECOND_TABLE_ITEMS_FOR_CHECK = (By.CSS_SELECTOR, '[class="grid_item"]:nth-child(2) tbody>a>div:first-child')
    THIRD_TABLE_ITEMS_FOR_CHECK = (By.CSS_SELECTOR, '[class="grid_item"]:nth-child(3) tbody>a>div:first-child')
    SEARCH_PLAYLISTS_INPUT = (By.CSS_SELECTOR, '[placeholder*="Поиск"]')
