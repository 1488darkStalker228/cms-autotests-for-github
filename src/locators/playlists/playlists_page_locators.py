from selenium.webdriver.common.by import By


class PlaylistsHeaderLocators:
    SWITCH_FILTER_PLAYLISTS = (By.CSS_SELECTOR, '[data-testid="switch-filter-playlists"]')
    DELETE_PLAYLIST = (By.CSS_SELECTOR, '[data-testid="delete-playlist"]')
    DOWNLOAD_PLAYLIST = (By.CSS_SELECTOR, '[data-testid="download-playlist"]')
    CREATE_PLAYLIST = (By.CSS_SELECTOR, '[data-testid="create-playlist"]')
    EDIT_PLAYLIST = (By.CSS_SELECTOR, '[data-testid="edit-playlist"]')
    EDIT_PLAYLIST_INNER = (By.CSS_SELECTOR, '[data-testid="edit-playlist-inner"]')
    IMPORT_TRACKS = (By.XPATH, '/html/body/main/section/div[2]/div[2]/main/section/section[3]')


class PlaylistDeletionModal:
    TOGGLE_SHOW_DETAILS = (By.CSS_SELECTOR, '[class="toggle"]')
    PLAYLIST_TITLE = (By.CSS_SELECTOR, '[class="name"]')
    CONFIRM_DELETE_BUTTON = (By.CSS_SELECTOR, '[class="modal-footer"]>button:first-child')
    CONFIRM_CHANGE_LICENSE_BUTTON = (By.CSS_SELECTOR, '[class="modal-footer"]>button:first-child')


class PlaylistsEditorLocators:
    TITLE_INPUT = (By.CSS_SELECTOR, '[data-testid="playlist-title-input"]')
    CLIENT_INPUT = (By.CSS_SELECTOR, '[data-testid="client-input"]')
    CATALOG_INPUT = (By.CSS_SELECTOR, '[data-testid="catalog-input"]')
    PLAY_ORDER_INPUT = (By.CSS_SELECTOR, '[data-testid="play-order-list-input"]')
    LICENSE_INPUT = (By.CSS_SELECTOR, '[data-testid="license-input"]')
    RESPONSIBLE_INPUT = (By.CSS_SELECTOR, '[data-testid="responsible-input"]')
    PLAYLIST_CHECKBOXES = (By.CSS_SELECTOR, '[class="ui-checkbox"]>section:first-child')
    DESCRIPTION_TEXTAREA = (By.CSS_SELECTOR, '[class="ui-textarea"]')
    # УДАЛИТЬ НА ФРОНТЕ
    # CLIENT_DROPDOWN = 'div[data-testid="client-dropdown"]'

    CLIENT_ITEMS = (By.CSS_SELECTOR, '[data-testid="client-list"]>section')
    CATALOG_ITEMS = (By.CSS_SELECTOR, '[data-testid="catalog-list"]>section')
    ORDER_ITEM_SECOND = (By.CSS_SELECTOR, '[data-testid="play-order-list-list"]>section:nth-child(2)')
    # УДАЛИТЬ НА ФРОНТЕ
    # LICENSE_DROPDOWN = 'div[data-testid="license-dropdown"]'
    LICENSE_ITEMS = (By.CSS_SELECTOR, '[data-testid="license-list"]>section')
    RESPONSIBLE_ITEMS = (By.CSS_SELECTOR, '[data-testid="responsible-list"]>section')
    CATEGORY_TYPE_BLOCK = (By.CSS_SELECTOR, '[class*="modal-playlist-properties__category-types"]>div:first-child>main>section:last-child')
    CATEGORY_ITEMS = (By.CSS_SELECTOR, '[class*="ui-dropdown-multiple__mapped-item"]>section:first-child')
    DELETE_CATEGORY_ICON = (By.CSS_SELECTOR, '[class*="ui-dropdown-multiple__selected-items"]>span:first-child>main')
    CLEAR_CATEGORY_ICON = (By.CSS_SELECTOR, '[class*="modal-playlist-properties__category-types"]>div:first-child div>section>main')
    SIMILAR_PLAYLISTS_SECTION = (By.XPATH, '/html/body/div[4]/div[1]/div/div/div/div/section/section[2]/section/main/div[5]/div[1]/main[1]')
    SIMILAR_PLAYLIST_FIRST_CHECKBOX = (By.XPATH, '//main[contains(@class, "ui-checkbox ui-dropdown-multiple__mapped-item")][1]//section[1]')
    COVER_FILE_INPUT = (By.CSS_SELECTOR, '[id=file]')
    CREATE_PLAYLIST_BUTTON = (By.CSS_SELECTOR, '[data-testid="create-playlist-button"]')
    CLOSE_MODAL = (By.XPATH, '/html/body/div[4]/div[1]/div/div/div/div/section/section[1]/section/main')


class PlaylistsTableLocators:
    PLAYLISTS_FIRST_ITEM = (By.CSS_SELECTOR, '[data-testid="playlists-table"]>a')
    PLAYLISTS_FIRST_ITEM_FOR_CLICK = (By.CSS_SELECTOR, '[data-testid="playlists-table"]>a:first-child>div:nth-child(2)')
    PLAYLIST_FIRST_ITEM_TITLE = (By.CSS_SELECTOR, '[data-testid="playlists-table"]>a:first-child a')


class PlaylistPageLocators:
    BREADCRUMBS = (By.CSS_SELECTOR, '[href="/playlists/list"]')
    ADD_TRACK_CHECKBOXES = (By.CSS_SELECTOR, '[class*="playlist-editor-media-item__checkbox"]')
    ADD_TRACK_BUTTON = (By.XPATH, '/html/body/main/section/div[1]/div[2]/section/div[1]/div[1]/div/div/button')
    DELETE_TRACK_CHECKBOXES = (By.CSS_SELECTOR, '[class*="playlist-editor-tracks-item__checkbox"]')
    DELETE_TRACK_BUTTON = (By.XPATH, '/html/body/main/section/div[1]/div[2]/section/div[2]/div[1]/div/div/button')
    TRACK_LIST_SEARCH_INPUT = (By.XPATH, '/html/body/main/section/div[1]/div[2]/section/div[1]/div[1]/div/div/div/div/div/div')
    PLAYLIST_SEARCH_INPUT = (By.XPATH, '/html/body/main/section/div[1]/div[2]/section/div[2]/div[1]/div/div/div/div/div/div')
    CLEAR_SEARCH_INPUT_ICON = (By.CSS_SELECTOR, '[class*=text-muted]')
    TRACK_LIST_ITEMS = (By.CSS_SELECTOR, '[class*="playlist-editor-media__list"]>section')
    PLAYLIST_ITEMS = (By.CSS_SELECTOR, '[class*="playlist-editor-tracks__list"]>section')


class PlaylistsSelectedModalLocators:
    SEARCH_INPUT = (By.XPATH, '/html/body/div[4]/div[1]/div/div/div/div/div[2]/div[1]/input')
    FIRST_ITEM = (By.CSS_SELECTOR, 'tbody>a:first-child')
    CHECKBOXES = (By.CSS_SELECTOR, 'tbody label')
    CONFIRM_IMPORT_PLAYLISTS = (By.CSS_SELECTOR, '[class="modal-footer"] button:first-child')
    TABLE_ITEMS = (By.CSS_SELECTOR, 'tbody a')