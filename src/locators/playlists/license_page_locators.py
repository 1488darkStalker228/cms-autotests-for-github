import random
from selenium.webdriver.common.by import By


class LicensePageLocators:
    FIRST_ITEM_TREE = (By.CSS_SELECTOR, '[class="tree-root"]>li:first-child')
    LAST_ITEM_TREE = (By.CSS_SELECTOR, '[class="tree-root"]>li:last-child')
    RANDOM_ITEM_TREE = (By.CSS_SELECTOR, f'[class="tree-root"]>li:nth-child({random.randint(1, 12)})')
    LAST_ITEM_TREE_XPATH = (By.XPATH, '//ul/li[2]/div')
    ADD_ITEM_BTN = (By.CSS_SELECTOR, '[style="visibility: visible;"]')
    CONTEXT_FIRST_ITEM = (By.CSS_SELECTOR, '[class="v-context"]>:first-child')
    CONTEXT_LAST_ITEM = (By.CSS_SELECTOR, '[class="v-context"]>:last-child')
    SELECTED_ITEM = (By.CSS_SELECTOR, '[class="tree-node selected draggable"]')
    ITEM_INPUT = (By.CSS_SELECTOR, '[class="tree-input"]')
    ADD_CATEGORY_BLOCK = (By.CSS_SELECTOR, '[class="grid"]>div:last-child')
    CREATE_CATEGORY_INPUT = (By.CSS_SELECTOR, '[class="modal-content"] input')
    CONFIRM_BUTTON = (By.CSS_SELECTOR, '[class="modal-footer"]>button:first-child')
    CATEGORY_ITEM = (By.CSS_SELECTOR, '[class="tree-root"]>li:last-child li')
    ROOT_LIST = (By.CSS_SELECTOR, '[class="tree-root"]>li')
    CHANGE_DISPLAY_TYPE_TO_TABLE = (By.CSS_SELECTOR, '[title="Изменить тип отображения"]')
    CHANGE_DISPLAY_TYPE_TO_GRID = (By.CSS_SELECTOR, '[src*="grid.png"]')
    TABLE_TYPE = (By.CSS_SELECTOR, '[class^="playlist-licenses-content"] tbody')
    GRID_TYPE = (By.CSS_SELECTOR, '[class^="playlist-licenses-content"] [class="grid"]')
    GO_TO_DOWN_ITEM_IN_TREE = (By.CSS_SELECTOR, '[class="grid"]>div:first-child')
    RENAME_INPUT = (By.CSS_SELECTOR, '[class^="playlist-licenses-form"]>fieldset:nth-child(2) input')
    DESCRIPTION_TEXTAREA = (By.CSS_SELECTOR, '[class^="playlist-licenses-form"]>fieldset:nth-child(3) textarea')
    DATE_INPUT = (By.CSS_SELECTOR, '[class^="playlist-licenses-form"]>fieldset:nth-child(4) input')
    CLEAR_DATE_INPUT_ICON = (By.CSS_SELECTOR, '[class^="playlist-licenses-form"]>fieldset:nth-child(4) [class="mx-icon-clear"] ')
    LICENSE_CONTENT_TITLE = (By.CSS_SELECTOR, '[class^="playlist-licenses-form"]>div:first-child')
    SAVE_LICENSE_CHANGE = (By.XPATH, '//section[@class="header-buttons__dropdown"]')
    PROMOTION_PERIOD_ICON = (By.CSS_SELECTOR, '[class="tree-node selected draggable"] [class^="star"]')

    SEARCH_ICON = (By.CSS_SELECTOR, '[class="search_button"]')
    SEARCH_INPUT_CATEGORY_PAGE = (By.CSS_SELECTOR, '[class^="playlist-licenses-content"] [class="type-zone active"]')
    RANDOM_TABLE_ITEM = (By.CSS_SELECTOR, f'tbody>a:nth-child({random.randint(1, 11)})')
    FIRST_TABLE_ITEM = (By.CSS_SELECTOR, 'tbody>a:first-child')
    TABLE_ITEMS = (By.CSS_SELECTOR, 'tbody>a')



