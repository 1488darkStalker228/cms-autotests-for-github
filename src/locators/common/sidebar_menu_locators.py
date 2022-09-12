from selenium.webdriver.common.by import By


class SidebarMenuLocators:
    SIDEBAR = (By.CSS_SELECTOR, '[class*="app-sidebar"]>div')
    PLAYLISTS = (By.CSS_SELECTOR, '[class*="app-sidebar"]>div>div:nth-child(9)')
    PLAYLISTS_DOWNLOAD_LINK = (By.CSS_SELECTOR, '[class*="submenu"]>a:nth-child(4)')




