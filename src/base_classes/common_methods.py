import random
import time
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.remote.webelement import WebElement
from src.base_classes.selenium_base import SeleniumBase
from src.locators.common.common_locators import CommonLocators


class CommonMethods(SeleniumBase):
    NOT_FOUND_MESSAGE: str = 'Items not found'
    EMPTY_VALUE: str = 'Empty value'

    def search(self, search_inp: tuple, items: tuple, amount_for_cut: int, title_position: int = 1) -> list[str] | str:
        search_inp: WebElement = self.is_visible(search_inp)
        items_titles: list[str] | str = self.splitlines_items(items, title_position)
        result: list[str] = []

        if self.NOT_FOUND_MESSAGE not in items_titles:
            random_item_title: str = items_titles[random.randint(0, len(items_titles) - 1)]
            if amount_for_cut > 0:
                if random_item_title[-1] == ' ':
                    search_inp.send_keys(random_item_title[0:amount_for_cut - 1])
                else:
                    search_inp.send_keys(random_item_title[0:amount_for_cut])
            else:
                search_inp.send_keys(random_item_title)
            # Не успевают подгружаться данные;
            time.sleep(2)
            result_item_title: str = self.splitlines_items(items, title_position)[0]

            if search_inp.get_attribute('value') is not None:
                result.append(search_inp.get_attribute('value'))
            else:
                result.append(search_inp.text)
            result.append(result_item_title)
            return result
        else:
            return [self.EMPTY_VALUE, self.NOT_FOUND_MESSAGE]

    def splitlines_items(self, items: tuple, title_position: int) -> list[str] | str:
        try:
            result: list[str] = []
            for item in self.are_present(items):
                item_splitlines: list[str] = item.text.splitlines()
                if len(item_splitlines) > 0:
                    result.append(item_splitlines[title_position])
            return result
        except TimeoutException:
            return self.NOT_FOUND_MESSAGE

    def get_counter_items(self) -> int:
        # Чтобы информация в элементе успела обновиться;
        time.sleep(1)
        return int(self.is_present(CommonLocators.ITEMS_COUNTER).text[3:7])

    def check_table_state_after_search(self, search_inp: tuple, items_list: tuple,
                                       index: int = 0) -> list[list[str] | str]:
        result: list[list[str] | str] = []

        init_state: list[str] = self.splitlines_items(items_list, index)
        result.append(init_state)
        search_input: WebElement = self.is_visible(search_inp)
        search_input.send_keys('some_text')
        # Для подгрузки данных;
        time.sleep(1)
        # Данную обработку можно будет убрать, если во всех поисковых инпутах добавятся крестики очистки инпута;
        try:
            clear_search_input = self.is_present(CommonLocators.CLEAR_SEARCH_INPUT)
            clear_search_input.click()
        except TimeoutException:
            search_input.send_keys(Keys.CONTROL + 'a')
            search_input.send_keys(Keys.DELETE)

        if search_input.get_attribute('value') is not None:
            result.append(search_input.get_attribute('value'))
        else:
            result.append(search_input.text)
        # Для подгрузки данных;
        time.sleep(1)
        state_after_clear_search_inp: list[str] = self.splitlines_items(items_list, index)
        result.append(state_after_clear_search_inp)
        return result
















