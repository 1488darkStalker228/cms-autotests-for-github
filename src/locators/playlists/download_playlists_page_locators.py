from selenium.webdriver.common.by import By


class DownloadPlaylistsTableLocators:
    PLAYLISTS_ITEMS = (By.CSS_SELECTOR, 'tbody>a')
    PLAYLISTS_FIRST_ITEM_TITLE = (By.CSS_SELECTOR, 'tbody>a:first-child>div:first-child')
    DELETE_ICON = (By.CSS_SELECTOR, '[title*="Удалить архивы"]')
    CONFIRM_DELETE_BUTTON = (By.CSS_SELECTOR, '[class="modal-footer"]>button:first-child')