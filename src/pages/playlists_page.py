import os
import time
import random
import datetime
from selenium.common import TimeoutException
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.remote.webelement import WebElement
from src.base_classes.selenium_base import SeleniumBase
from src.generators.generator import generated_data_for_fill_fields
from src.locators.common.common_locators import CommonLocators
from src.locators.playlists.compare_playlists_page_locators import ComparePlaylistsPageLocators
from src.locators.playlists.download_playlists_page_locators import DownloadPlaylistsTableLocators
from src.locators.playlists.license_page_locators import LicensePageLocators
from src.locators.playlists.playlists_page_locators import PlaylistsHeaderLocators, PlaylistsEditorLocators, \
    PlaylistsTableLocators, PlaylistPageLocators, PlaylistsSelectedModalLocators, PlaylistDeletionModal
from src.locators.common.sidebar_menu_locators import SidebarMenuLocators
from src.base_classes.common_methods import CommonMethods


class PlaylistsListPage(SeleniumBase):
    def create_playlist(self) -> list[list[str | list[str]], list[str | list[str]]]:
        data_for_playlist_fields = next(generated_data_for_fill_fields())

        self.is_visible(PlaylistsHeaderLocators.CREATE_PLAYLIST).click()
        title_input: WebElement = self.is_visible(PlaylistsEditorLocators.TITLE_INPUT)
        title_input.send_keys(data_for_playlist_fields.title)

        client_input: WebElement = self.is_visible(PlaylistsEditorLocators.CLIENT_INPUT)
        client_input.click()
        self.are_present(PlaylistsEditorLocators.CLIENT_ITEMS)[0].click()

        catalog_input: WebElement = self.is_visible(PlaylistsEditorLocators.CATALOG_INPUT)
        catalog_input.click()
        self.are_present(PlaylistsEditorLocators.CATALOG_ITEMS)[0].click()

        property_checkboxes: list[WebElement] = self.are_visible(PlaylistsEditorLocators.PLAYLIST_CHECKBOXES)
        self.click_random_checkboxes(property_checkboxes)

        license_input: WebElement = self.is_visible(PlaylistsEditorLocators.LICENSE_INPUT)
        license_input.click()
        self.are_present(PlaylistsEditorLocators.LICENSE_ITEMS)[0].click()

        responsible_input: WebElement = self.is_visible(PlaylistsEditorLocators.RESPONSIBLE_INPUT)
        responsible_input.click()
        self.are_present(PlaylistsEditorLocators.RESPONSIBLE_ITEMS)[0].click()

        self.is_visible(PlaylistsEditorLocators.CATEGORY_TYPE_BLOCK).click()
        category_items: list[WebElement] = self.are_present(PlaylistsEditorLocators.CATEGORY_ITEMS)[0:7]
        self.click_random_checkboxes(category_items)

        self.scroll_top_editor_playlist()

        self.is_visible(PlaylistsEditorLocators.SIMILAR_PLAYLISTS_SECTION).click()
        # Множественный выбор похожих плейлистов не работает;
        time.sleep(4)
        similar_playlist: WebElement = self.is_visible(PlaylistsEditorLocators.SIMILAR_PLAYLIST_FIRST_CHECKBOX)
        similar_playlist.click()

        # Запись в текстареа идёт, хоть элемент и перекрыт;
        description_textarea: WebElement = self.is_visible(PlaylistsEditorLocators.DESCRIPTION_TEXTAREA)
        description_textarea.send_keys(data_for_playlist_fields.description)

        self.is_present(PlaylistsEditorLocators.COVER_FILE_INPUT).send_keys(
            os.path.abspath('../images/create_playlist.png')
        )

        result_from_create_modal: list[str | list[str]] = self.get_result_from_playlist_editor_modal()
        self.is_visible(PlaylistsEditorLocators.CREATE_PLAYLIST_BUTTON).click()
        self.is_visible(PlaylistsHeaderLocators.EDIT_PLAYLIST_INNER).click()
        result_from_edit_modal: list[str | list[str]] = self.get_result_from_playlist_editor_modal()
        self.is_visible(PlaylistsEditorLocators.CLOSE_MODAL).click()
        self.is_visible(PlaylistPageLocators.BREADCRUMBS).click()
        return [result_from_create_modal, result_from_edit_modal]

    def get_text_playlist_item(self) -> list[str | list[str | None]]:
        first_item_text: str = self.is_present(PlaylistsTableLocators.PLAYLISTS_FIRST_ITEM).get_attribute('text')
        first_item_text_list: list[str] = first_item_text[1:].split('  ')[0:9]

        result: list[str | list[str | None]] = []
        result_1: list[str | None] = []
        # Можно убрать continue если заменить if на elif;
        for item in first_item_text_list:
            if item == 'Да' or item == 'Публичный':
                result_1.append('true')
                continue
            if item == 'Нет' or item == 'Приватный':
                result_1.append(None)
                continue
            else:
                result.append(item)
        result.append(result_1)
        return result

    def get_result_from_playlist_editor_modal(self) -> list[str | list[str]]:
        # Без этого ошибка в assert на офисном ноутбуке;
        time.sleep(1)
        result: list[str | list[str]] = [
            self.is_present(PlaylistsEditorLocators.TITLE_INPUT).get_attribute('value'),
            self.is_present(PlaylistsEditorLocators.CLIENT_INPUT).get_attribute('value'),
            self.is_present(PlaylistsEditorLocators.CATALOG_INPUT).get_attribute('value'),
            self.is_present(PlaylistsEditorLocators.LICENSE_INPUT).get_attribute('value'),
            self.is_present(PlaylistsEditorLocators.RESPONSIBLE_INPUT).get_attribute('value'),
            self.get_value_checkboxes(self.are_present(PlaylistsEditorLocators.PLAYLIST_CHECKBOXES)),
            self.is_present(PlaylistsEditorLocators.PLAY_ORDER_INPUT).get_attribute('value'),
            self.is_visible(PlaylistsEditorLocators.DESCRIPTION_TEXTAREA).get_attribute('value')
        ]
        # Нужно для запуска на офисном ноутбуке;
        self.scroll_top_editor_playlist()
        self.is_visible(PlaylistsEditorLocators.CATEGORY_TYPE_BLOCK).click()
        # Без этого, ошибка получения данных из чекбоксов;
        time.sleep(5)
        result.append(
            self.get_value_checkboxes(self.are_present(PlaylistsEditorLocators.CATEGORY_ITEMS)[0:7])
        )
        self.is_visible(PlaylistsEditorLocators.SIMILAR_PLAYLISTS_SECTION).click()
        result.append(
            self.get_value_checkboxes([self.is_visible(PlaylistsEditorLocators.SIMILAR_PLAYLIST_FIRST_CHECKBOX)])
        )
        return result

    def edit_playlist(self) -> list[list[str | list[str]], list[str | list[str]]]:
        data_for_playlist_fields = next(generated_data_for_fill_fields())

        self.is_visible(PlaylistsTableLocators.PLAYLISTS_FIRST_ITEM_FOR_CLICK).click()
        self.is_visible(PlaylistsHeaderLocators.EDIT_PLAYLIST).click()
        title_input: WebElement = self.is_visible(PlaylistsEditorLocators.TITLE_INPUT)
        title_input.send_keys(Keys.CONTROL + 'a')
        title_input.send_keys(data_for_playlist_fields.title)

        client_input: WebElement = self.is_visible(PlaylistsEditorLocators.CLIENT_INPUT)
        client_input.click()
        self.are_present(PlaylistsEditorLocators.CLIENT_ITEMS)[random.randint(1, 5)].click()

        catalog_input: WebElement = self.is_visible(PlaylistsEditorLocators.CATALOG_INPUT)
        catalog_input.click()
        self.are_present(PlaylistsEditorLocators.CATALOG_ITEMS)[random.randint(1, 5)].click()

        property_checkboxes: list[WebElement] = self.are_visible(PlaylistsEditorLocators.PLAYLIST_CHECKBOXES)
        self.click_random_checkboxes(property_checkboxes)

        play_order_input: WebElement = self.is_visible(PlaylistsEditorLocators.PLAY_ORDER_INPUT)
        play_order_input.click()
        self.is_visible(PlaylistsEditorLocators.ORDER_ITEM_SECOND).click()

        self.is_visible(PlaylistsEditorLocators.DELETE_CATEGORY_ICON).click()
        self.is_visible(PlaylistsEditorLocators.CLEAR_CATEGORY_ICON).click()

        license_input: WebElement = self.is_visible(PlaylistsEditorLocators.LICENSE_INPUT)
        license_input.click()
        self.are_present(PlaylistsEditorLocators.LICENSE_ITEMS)[random.randint(1, 5)].click()
        self.is_visible(PlaylistDeletionModal.CONFIRM_CHANGE_LICENSE_BUTTON).click()
        # Когда меняем лицензию, то элементы в DOM обновляются, и без задержки не успевают прогрузиться;
        time.sleep(1)

        self.is_visible(PlaylistsEditorLocators.CATEGORY_TYPE_BLOCK).click()
        category_items: list[WebElement] = self.are_present(PlaylistsEditorLocators.CATEGORY_ITEMS)[0:7]
        self.click_random_checkboxes(category_items)

        responsible_input: WebElement = self.is_visible(PlaylistsEditorLocators.RESPONSIBLE_INPUT)
        responsible_input.click()
        self.are_present(PlaylistsEditorLocators.RESPONSIBLE_ITEMS)[random.randint(1, 5)].click()

        self.scroll_top_editor_playlist()

        self.is_visible(PlaylistsEditorLocators.SIMILAR_PLAYLISTS_SECTION).click()
        # Множественный выбор похожих плейлистов не работает;
        similar_playlist: WebElement = self.is_visible(PlaylistsEditorLocators.SIMILAR_PLAYLIST_FIRST_CHECKBOX)
        similar_playlist.click()

        description_textarea: WebElement = self.is_visible(PlaylistsEditorLocators.DESCRIPTION_TEXTAREA)
        description_textarea.send_keys(Keys.CONTROL + 'a')
        description_textarea.send_keys(data_for_playlist_fields.description)

        self.is_present(PlaylistsEditorLocators.COVER_FILE_INPUT).send_keys(
            os.path.abspath('../images/edit_playlist.jpg')
        )

        data_for_edit: list[str | list[str]] = self.get_result_from_playlist_editor_modal()
        self.is_visible(PlaylistsEditorLocators.CREATE_PLAYLIST_BUTTON).click()
        # Для того, чтобы мы могли кликнуть на первый айтем в таблице плейлистов;
        time.sleep(1)
        self.is_visible(PlaylistsTableLocators.PLAYLISTS_FIRST_ITEM_FOR_CLICK).click()
        self.is_visible(PlaylistsHeaderLocators.EDIT_PLAYLIST).click()
        result_after_edit: list[str | list[str]] = self.get_result_from_playlist_editor_modal()
        return [data_for_edit, result_after_edit]

    def download_playlist(self) -> list[str]:
        result: list[str] = []
        self.is_visible(PlaylistsTableLocators.PLAYLISTS_FIRST_ITEM_FOR_CLICK).click()
        result.append(self.is_visible(PlaylistsTableLocators.PLAYLIST_FIRST_ITEM_TITLE).text)
        self.is_visible(PlaylistsHeaderLocators.DOWNLOAD_PLAYLIST).click()
        self.go_to_element(self.is_present(SidebarMenuLocators.PLAYLISTS))
        ActionChains(self.driver).move_to_element(self.is_present(SidebarMenuLocators.PLAYLISTS)).perform()
        # Ждём, пока меню выедет;
        time.sleep(1)
        self.go_to_element(self.is_visible(SidebarMenuLocators.PLAYLISTS_DOWNLOAD_LINK))
        self.is_visible(SidebarMenuLocators.PLAYLISTS_DOWNLOAD_LINK).click()
        # Без этого - ошибка;
        time.sleep(1)
        result.append(self.is_visible(DownloadPlaylistsTableLocators.PLAYLISTS_FIRST_ITEM_TITLE).text)
        return result

    def delete_playlist(self) -> list[str]:
        title_from_table_item: str = self.is_visible(PlaylistsTableLocators.PLAYLIST_FIRST_ITEM_TITLE).text
        self.is_visible(PlaylistsTableLocators.PLAYLISTS_FIRST_ITEM_FOR_CLICK).click()
        self.is_visible(PlaylistsHeaderLocators.DELETE_PLAYLIST).click()
        self.is_visible(PlaylistDeletionModal.TOGGLE_SHOW_DETAILS).click()
        title_from_details: str = self.is_visible(PlaylistDeletionModal.PLAYLIST_TITLE).text
        self.is_visible(PlaylistDeletionModal.CONFIRM_DELETE_BUTTON).click()
        return [title_from_table_item, title_from_details]

    def add_remove_track(self) -> list[tuple[int]]:
        self.is_visible(PlaylistsTableLocators.PLAYLIST_FIRST_ITEM_TITLE).click()
        add_track_button: WebElement = self.is_visible(PlaylistPageLocators.ADD_TRACK_BUTTON)
        del_track_button: WebElement = self.is_visible(PlaylistPageLocators.DELETE_TRACK_BUTTON)

        add_track: tuple[int] = self.get_counter_selected_track(
            # На домашнем компе не находит список элементов с помощью are_visible;
            add_track_button, self.are_visible(PlaylistPageLocators.ADD_TRACK_CHECKBOXES)[0:8]
        )
        add_track_button.click()
        # Не успевают подгрузиться данные;
        time.sleep(1)
        delete_track: tuple[int] = self.get_counter_selected_track(
            del_track_button, self.are_visible(PlaylistPageLocators.DELETE_TRACK_CHECKBOXES)[0:8]
        )
        del_track_button.click()
        # Не успевают подгрузиться данные;
        time.sleep(1)
        # На домашнем компе не находит список элементов с помощью are_visible;
        add_track_with_active_checkboxes = self.get_counter_selected_track(
            add_track_button, self.are_visible(PlaylistPageLocators.ADD_TRACK_CHECKBOXES)[0:4]
        )
        # Не успевают подгрузиться данные;
        time.sleep(1)
        del_track_with_active_checkboxes = self.get_counter_selected_track(
            del_track_button, self.are_visible(PlaylistPageLocators.DELETE_TRACK_CHECKBOXES)[0:4]
        )
        add_track_button.click()
        del_track_button.click()
        return [add_track, delete_track, add_track_with_active_checkboxes, del_track_with_active_checkboxes]

    def search_tracks_in_track_list(self) -> list[str]:
        return CommonMethods(self.driver).search(
            PlaylistPageLocators.TRACK_LIST_SEARCH_INPUT,
            PlaylistPageLocators.TRACK_LIST_ITEMS,
            18
        )

    def search_tracks_in_playlist(self) -> list[str]:
        return CommonMethods(self.driver).search(
            PlaylistPageLocators.PLAYLIST_SEARCH_INPUT,
            PlaylistPageLocators.PLAYLIST_ITEMS,
            18
        )

    def check_state_track_lists_table(self) -> list[list[str] | str]:
        self.is_visible(PlaylistsTableLocators.PLAYLIST_FIRST_ITEM_TITLE).click()
        return CommonMethods(self.driver).check_table_state_after_search(
            PlaylistPageLocators.TRACK_LIST_SEARCH_INPUT,
            PlaylistPageLocators.TRACK_LIST_ITEMS,
            1
        )

    def check_state_playlist_table(self) -> list[list[str] | str]:
        return CommonMethods(self.driver).check_table_state_after_search(
            PlaylistPageLocators.PLAYLIST_SEARCH_INPUT,
            PlaylistPageLocators.PLAYLIST_ITEMS,
            1
        )

    def get_counter_selected_track(self, button: WebElement, checkboxes: list[WebElement]) -> tuple[int, int]:
        checkboxes_counter: int = self.click_random_checkboxes(checkboxes)
        self.go_to_element(button)
        counter_from_button: int = int(''.join(reversed(button.text))[1:2])
        return checkboxes_counter, counter_from_button

    def import_tracks_from_other_playlists(self) -> list[int, int]:
        self.is_visible(PlaylistsTableLocators.PLAYLIST_FIRST_ITEM_TITLE).click()
        self.is_visible(PlaylistsHeaderLocators.IMPORT_TRACKS).click()
        self.is_visible(PlaylistsSelectedModalLocators.SEARCH_INPUT).send_keys('Тестовый для импорта')

        for checkbox in self.are_visible(PlaylistsSelectedModalLocators.CHECKBOXES):
            checkbox.click()

        self.is_visible(PlaylistsSelectedModalLocators.CONFIRM_IMPORT_PLAYLISTS).click()

        tracks_from_import_playlists: list[str] = [
            '01_The_Scythe', '01_The_Weight_pn', '001_Cubicmedia_music_-_Sticky_Beats',
            '001_Cubic_Media_November_-_Gravity_pn', '014_Alіta_Kum_--advert-06', '11',
            'media-01', 'media-02', 'media-03', '3D_Print', '50s_Christmas_1', 'Rue_Saint-Antoine'
        ]
        import_tracks: list[str] = []
        counter_after_import: int = 0
        counter_currents_items: int = 0
        # Некорректно получает данные;
        time.sleep(1)

        for item in self.are_present(PlaylistPageLocators.PLAYLIST_ITEMS)[0:12]:
            item_replace_space: list[str] = item.text.replace(' ', '_').split()
            if len(item_replace_space) > 0:
                import_tracks.append(item_replace_space[1])
                counter_currents_items += 1

        for track_1 in tracks_from_import_playlists:
            for track_2 in import_tracks:
                if track_1 == track_2:
                    counter_after_import += 1
        return [counter_currents_items, counter_after_import]

    # Можно создать отдельный класс для проверки модалки;
    def search_playlists_in_selected_modal(self) -> list[str]:
        return CommonMethods(self.driver).search(
            PlaylistsSelectedModalLocators.SEARCH_INPUT,
            PlaylistsSelectedModalLocators.TABLE_ITEMS,
            0
        )

    def check_state_selected_modal_table(self) -> list[list[str] | str]:
        self.is_visible(PlaylistsTableLocators.PLAYLIST_FIRST_ITEM_TITLE).click()
        self.is_visible(PlaylistsHeaderLocators.IMPORT_TRACKS).click()
        return CommonMethods(self.driver).check_table_state_after_search(
            PlaylistsSelectedModalLocators.SEARCH_INPUT,
            PlaylistsSelectedModalLocators.TABLE_ITEMS
        )

    @staticmethod
    def get_value_checkboxes(elements: list[WebElement]) -> list[str]:
        """
        Метод обращается к данному массиву, чекает его атрибуты, и получает их актуальное состояние;
        Невидимость элементов в текущий момент преодолевается тем,
        что элементы уже были найдены и сохранены в переменную;
        """
        return [element.get_attribute('data-active') for element in elements]

    def click_random_checkboxes(self, items: list[WebElement]) -> int:
        counter: int = 1
        self.go_to_element(items[0])
        items[0].click()

        for item in items[1:]:
            tmp: int = random.randint(0, 1)
            if tmp > 0:
                counter += 1
                self.go_to_element(item)
                item.click()
        return counter

    def scroll_top_editor_playlist(self) -> None:
        self.driver.execute_script(
            'const elem = document.querySelector(".modal-playlist__content-inner");'
            'elem.scrollTop = elem.scrollHeight'
        )


class PlaylistsDownloadPage(SeleniumBase):
    def delete_playlists(self) -> list[int, int]:
        playlist_items: list[WebElement] = self.are_present(DownloadPlaylistsTableLocators.PLAYLISTS_ITEMS)[0:3]
        playlist_items[0].click()

        for item in playlist_items[1:]:
            ActionChains(self.driver).key_down(Keys.SHIFT).click(item).perform()

        delete_icon: WebElement = self.is_visible(DownloadPlaylistsTableLocators.DELETE_ICON)
        selected_items_amount: int = len(playlist_items)
        delete_icon_counter: int = int(delete_icon.get_attribute('title').replace('[', '').replace(']', '').split()[2])
        delete_icon.click()
        self.is_visible(DownloadPlaylistsTableLocators.CONFIRM_DELETE_BUTTON).click()
        return [selected_items_amount, delete_icon_counter]

    def search_playlist(self) -> list[str]:
        return CommonMethods(self.driver).search(
            CommonLocators.SEARCH_INPUT,
            DownloadPlaylistsTableLocators.PLAYLISTS_ITEMS,
            18
        )

    def check_state_playlists_table(self) -> list[list[str] | str]:
        return CommonMethods(self.driver).check_table_state_after_search(
            CommonLocators.SEARCH_INPUT,
            DownloadPlaylistsTableLocators.PLAYLISTS_ITEMS
        )


class PlaylistsComparePage(SeleniumBase):
    def check_status_and_counter_compare_button(self) -> list[list]:
        check_status_button: list[str] = []
        check_button_counter: list[str] = []

        compare_button: WebElement = self.is_visible(ComparePlaylistsPageLocators.COMPARE_BUTTON)
        check_status_button.append(compare_button.get_attribute('disabled'))
        check_button_counter.append(compare_button.text.replace('(', '').replace(')', '').split()[1])
        playlists_items: list[WebElement] = self.are_present(ComparePlaylistsPageLocators.PLAYLISTS_ITEMS)[0:12]

        for i in range(0, 11):
            self.go_to_element(playlists_items[i])
            playlists_items[i].click()
            if i == 0:
                check_status_button.append(compare_button.get_attribute('disabled'))
                check_button_counter.append(compare_button.text.replace('(', '').replace(')', '').split()[1])
            elif i == 1:
                check_status_button.append(compare_button.get_attribute('disabled'))
                check_button_counter.append(compare_button.text.replace('(', '').replace(')', '').split()[1])
            elif i == 9:
                check_status_button.append(compare_button.get_attribute('disabled'))
                check_button_counter.append(compare_button.text.replace('(', '').replace(')', '').split()[1])
            elif i == 10:
                check_status_button.append(compare_button.get_attribute('disabled'))
                check_button_counter.append(compare_button.text.replace('(', '').replace(')', '').split()[1])
        return [check_status_button, check_button_counter]

    def compare_playlists(self) -> int | bool:
        self.is_visible(ComparePlaylistsPageLocators.SEARCH_PLAYLISTS_INPUT).send_keys('Тестовый для сравнения')

        for playlist in self.are_visible(ComparePlaylistsPageLocators.PLAYLISTS_ITEMS):
            playlist.click()

        self.is_visible(ComparePlaylistsPageLocators.COMPARE_BUTTON).click()
        first_pl: int = self.get_background_color(
            self.are_visible(ComparePlaylistsPageLocators.FIRST_TABLE_ITEMS_FOR_CHECK)
        )
        second_pl: int = self.get_background_color(
            self.are_visible(ComparePlaylistsPageLocators.SECOND_TABLE_ITEMS_FOR_CHECK)
        )
        third_pl: int = self.get_background_color(
            self.are_visible(ComparePlaylistsPageLocators.THIRD_TABLE_ITEMS_FOR_CHECK)
        )

        if first_pl == 3 and second_pl == 3 and third_pl == 3:
            return 3
        else:
            return False

    @staticmethod
    def get_background_color(items: list[WebElement]) -> int:
        counter: int = 0
        for item in items:
            if 'background-color: rgb(250, 215, 100)' in item.get_attribute('style'):
                counter += 1
        return counter


class PlaylistsLicensesPage(SeleniumBase):
    ITEM_TITLE: str = 'TEST_CREATE_AND_DELETE'
    TITLE_FOR_RENAME_FROM_CONTEXT: str = 'TEST_RENAME'
    TITLE_FOR_RENAME_FROM_BLOCK: str = 'TEST_RENAME_1'
    CATEGORY_TITLE: str = 'Best music'
    NOT_FOUND_MESSAGE: str = 'Element not found'
    ICON_FOUND_MESSAGE: str = 'Promotion icon is missing'
    MISS_ICON_MESSAGE: str = 'Promotion icon is missing'

    def search_in_license_tree(self) -> list[str]:
        result: list[str] = []
        search_input: WebElement = self.is_visible(CommonLocators.SEARCH_INPUT)
        random_item_title: str = self.is_visible(LicensePageLocators.RANDOM_ITEM_TREE).text.splitlines()[0]
        search_input.send_keys(random_item_title)
        # Ждём загрузки данных;
        time.sleep(2)
        for item in self.are_visible(LicensePageLocators.ROOT_LIST):
            if search_input.text in item.text:
                result.append(item.text.splitlines()[0])
                break
        result.append(search_input.text)
        return result

    def check_state_license_tree(self) -> list[list[str] | str]:
        return CommonMethods(self.driver).check_table_state_after_search(
            CommonLocators.SEARCH_INPUT,
            LicensePageLocators.ROOT_LIST
        )

    def create_license(self) -> str:
        return self.create_item(
            LicensePageLocators.FIRST_ITEM_TREE,
            LicensePageLocators.ADD_ITEM_BTN,
            LicensePageLocators.CONTEXT_FIRST_ITEM
        )

    def create_category_type(self) -> str:
        self.is_visible(CommonLocators.SEARCH_INPUT).send_keys(self.ITEM_TITLE)
        # Без этого - ошибка при создании выпадающих списков;
        time.sleep(1)
        return self.create_item(
            LicensePageLocators.LAST_ITEM_TREE,
            LicensePageLocators.ADD_ITEM_BTN,
            LicensePageLocators.CONTEXT_LAST_ITEM
        )

    def create_category(self) -> str:
        self.is_visible(LicensePageLocators.LAST_ITEM_TREE).click()
        self.is_visible(LicensePageLocators.ADD_CATEGORY_BLOCK).click()
        self.is_visible(LicensePageLocators.ADD_CATEGORY_BLOCK).click()
        self.is_visible(LicensePageLocators.CREATE_CATEGORY_INPUT).send_keys(self.ITEM_TITLE)
        self.is_visible(LicensePageLocators.CONFIRM_BUTTON).click()
        return self.is_visible(LicensePageLocators.SELECTED_ITEM).text.splitlines()[0]

    def create_item(self, selected_itm: tuple, button: tuple, itm_type: tuple) -> str:
        self.is_visible(selected_itm).click()
        self.is_present(button).click()
        self.is_visible(itm_type).click()
        self.is_visible(LicensePageLocators.ITEM_INPUT).send_keys(self.ITEM_TITLE)
        self.is_visible(selected_itm).click()
        # Чтобы данные успели загрузиться;
        time.sleep(1)
        return self.is_visible(LicensePageLocators.SELECTED_ITEM).text.splitlines()[0]

    def change_display_type_in_license(self) -> list[str]:
        self.is_visible(CommonLocators.SEARCH_INPUT).send_keys(self.ITEM_TITLE)
        # Ожидаем загрузки;
        time.sleep(1)
        self.is_visible(LicensePageLocators.FIRST_ITEM_TREE).click()
        return self.change_display_type()

    def change_display_type_in_category_tree(self) -> list[str]:
        return self.change_display_type()

    def go_to_down_item_in_tree(self) -> None:
        self.is_visible(LicensePageLocators.GO_TO_DOWN_ITEM_IN_TREE).click()

    def change_display_type(self) -> list[str, str, str]:
        grid_type: str = self.check_display_type(LicensePageLocators.GRID_TYPE)
        self.is_visible(LicensePageLocators.CHANGE_DISPLAY_TYPE_TO_TABLE).click()
        table_type: str = self.check_display_type(LicensePageLocators.TABLE_TYPE)
        self.is_visible(LicensePageLocators.CHANGE_DISPLAY_TYPE_TO_GRID).click()
        type_after_change: str = self.check_display_type(LicensePageLocators.GRID_TYPE)
        return [table_type, grid_type, type_after_change]

    def check_display_type(self, disp_type: tuple[str, str]) -> str:
        try:
            self.is_present(disp_type)
            return 'Success change display type'
        except TimeoutException:
            return 'Failed change display type'

    def edit_category_fields(self) -> list[list[str], list[str]]:
        data_for_category_fields = next(generated_data_for_fill_fields())

        self.is_visible(CommonLocators.SEARCH_INPUT).send_keys(self.CATEGORY_TITLE)
        self.is_visible(LicensePageLocators.CATEGORY_ITEM).click()
        desc_area: WebElement = self.is_visible(LicensePageLocators.DESCRIPTION_TEXTAREA)
        desc_area.send_keys(Keys.CONTROL + 'a')
        desc_area.send_keys(data_for_category_fields.description)
        date_input: WebElement = self.is_visible(LicensePageLocators.DATE_INPUT)
        ActionChains(self.driver).move_to_element(date_input).perform()
        self.is_visible(LicensePageLocators.CLEAR_DATE_INPUT_ICON).click()
        dt_now = datetime.date.today().strftime('%d.%m.%Y')
        date_input.send_keys(f'{dt_now} - {dt_now}')
        date_input.send_keys(Keys.ENTER)
        self.is_visible(LicensePageLocators.SAVE_LICENSE_CHANGE).click()
        fields_values: list[str] = self.get_fields_values_cat_page()
        self.driver.refresh()
        fields_values_after_refresh: list[str] = self.get_fields_values_cat_page()
        return [fields_values, fields_values_after_refresh]

    def check_promotion_period(self) -> bool | str:
        try:
            self.is_visible(LicensePageLocators.PROMOTION_PERIOD_ICON)
            return self.ICON_FOUND_MESSAGE
        except TimeoutException:
            return self.MISS_ICON_MESSAGE

    def get_fields_values_cat_page(self) -> list[str]:
        return [
            self.is_visible(LicensePageLocators.DESCRIPTION_TEXTAREA).get_attribute('value'),
            self.is_visible(LicensePageLocators.DATE_INPUT).get_attribute('value')
        ]

    def search_playlists_in_category_page(self) -> list[str]:
        return CommonMethods(self.driver).search(
            LicensePageLocators.SEARCH_INPUT_CATEGORY_PAGE,
            LicensePageLocators.TABLE_ITEMS,
            0,
            0
        )

    def check_state_cat_page_table(self) -> list[list[str] | str]:
        self.is_visible(CommonLocators.SEARCH_INPUT).send_keys(self.CATEGORY_TITLE)
        self.is_visible(LicensePageLocators.CATEGORY_ITEM).click()
        self.is_visible(CommonLocators.CLEAR_SEARCH_INPUT).click()
        self.is_visible(LicensePageLocators.CHANGE_DISPLAY_TYPE_TO_TABLE).click()
        self.is_visible(LicensePageLocators.SEARCH_ICON).click()

        return CommonMethods(self.driver).check_table_state_after_search(
            LicensePageLocators.SEARCH_INPUT_CATEGORY_PAGE,
            LicensePageLocators.TABLE_ITEMS
        )

    def rename_license(self) -> list[str]:
        self.is_visible(CommonLocators.SEARCH_INPUT).send_keys(self.ITEM_TITLE)
        # Ожидаем загрузки данных;
        time.sleep(1)
        return self.rename_item(LicensePageLocators.FIRST_ITEM_TREE)

    def rename_category_type(self) -> list[str]:
        return self.rename_item(LicensePageLocators.LAST_ITEM_TREE_XPATH)

    def rename_category(self) -> list[str]:
        return self.rename_item(LicensePageLocators.CATEGORY_ITEM)

    def rename_item(self, itm_for_rename: tuple[str, str]) -> list[str, str]:
        ActionChains(self.driver).context_click(self.is_visible(itm_for_rename)).perform()
        self.is_visible(LicensePageLocators.CONTEXT_FIRST_ITEM).click()
        self.is_visible(LicensePageLocators.ITEM_INPUT).send_keys(self.TITLE_FOR_RENAME_FROM_CONTEXT)
        self.is_visible(LicensePageLocators.ITEM_INPUT).send_keys(Keys.ENTER)
        # Для загрузки данных
        time.sleep(1)
        after_rename_from_context: str = self.check_result_names_after_rename(
            self.get_titles_items_after_rename(itm_for_rename),
            self.TITLE_FOR_RENAME_FROM_CONTEXT
        )
        self.is_visible(LicensePageLocators.RENAME_INPUT).send_keys('_1')
        self.is_visible(LicensePageLocators.SAVE_LICENSE_CHANGE).click()
        # Для загрузки данных
        time.sleep(1)
        after_rename_from_block: str = self.check_result_names_after_rename(
            self.get_titles_items_after_rename(itm_for_rename),
            self.TITLE_FOR_RENAME_FROM_BLOCK
        )
        return [after_rename_from_context, after_rename_from_block]

    @staticmethod
    def check_result_names_after_rename(titles_list: list[str], expected_title: str) -> str:
        for title in titles_list:
            if title != expected_title:
                return "Names don't match"
        return expected_title

    def get_titles_items_after_rename(self, itm_for_get_title: tuple[str, str]) -> list[str]:
        return [
            self.is_visible(itm_for_get_title).text.splitlines()[0],
            self.is_visible(LicensePageLocators.RENAME_INPUT).get_attribute('value'),
            self.is_visible(LicensePageLocators.LICENSE_CONTENT_TITLE).text.split()[-1]
        ]

    def delete_category(self) -> list[int] | str:
        self.is_visible(CommonLocators.SEARCH_INPUT).send_keys(self.TITLE_FOR_RENAME_FROM_BLOCK)
        return self.delete_item(LicensePageLocators.CATEGORY_ITEM, LicensePageLocators.CATEGORY_ITEM)

    def delete_category_type(self) -> list[int] | str:
        return self.delete_item(LicensePageLocators.LAST_ITEM_TREE, LicensePageLocators.ROOT_LIST)

    def delete_license(self) -> list[int] | str:
        return self.delete_item(LicensePageLocators.LAST_ITEM_TREE, LicensePageLocators.ROOT_LIST)

    def delete_item(self, itm_for_remove: tuple, itms_list: tuple) -> list[int] | str:
        list_len: list[int] = [len(self.are_visible(itms_list))]
        # Ошибка при клике по контекстному меню;
        time.sleep(1)
        ActionChains(self.driver).context_click(self.is_visible(itm_for_remove)).perform()
        self.is_visible(LicensePageLocators.CONTEXT_LAST_ITEM).click()
        # Чтобы не было ошибок при клике на кнопку;
        time.sleep(1)
        self.is_visible(LicensePageLocators.CONFIRM_BUTTON).click()
        # Чтобы дождаться загрузки списка;
        time.sleep(1)
        try:
            list_len.append(len(self.are_visible(itms_list)))
            return list_len
        except TimeoutException:
            return self.NOT_FOUND_MESSAGE
