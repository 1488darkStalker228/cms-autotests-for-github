import pytest
from src.base_classes.common_methods import CommonMethods
from src.pages.playlists_page import PlaylistsListPage, PlaylistsDownloadPage, PlaylistsComparePage, \
    PlaylistsLicensesPage


@pytest.mark.usefixtures('setup', 'authorization')
class TestPlaylists:
    # Playlists_list_page
    def test_create_playlist(self):
        playlists_list_page = PlaylistsListPage(self.driver, 'https://cms-test.cubicservice.ru/playlists/list')
        playlists_list_page.open()
        result_from_create_modal, result_from_edit_modal = playlists_list_page.create_playlist()
        assert result_from_create_modal == result_from_edit_modal, 'Data does not match'
        assert result_from_edit_modal[0:6] == playlists_list_page.get_text_playlist_item(), 'Data does not match'

    def test_edit_playlist(self):
        playlists_list_page = PlaylistsListPage(self.driver, 'https://cms-test.cubicservice.ru/playlists/list')
        playlists_list_page.open()
        data_for_edit, result_after_edit = playlists_list_page.edit_playlist()
        assert data_for_edit == result_after_edit, 'Data does not match'
        assert result_after_edit[0:6] == playlists_list_page.get_text_playlist_item(), 'Data does not match'

    def test_delete_playlist(self):
        playlists_list_page = PlaylistsListPage(self.driver, 'https://cms-test.cubicservice.ru/playlists/list')
        playlists_list_page.open()
        counter_before = CommonMethods(self.driver).get_counter_items()
        title_from_table_item, title_from_details = playlists_list_page.delete_playlist()
        counter_after = CommonMethods(self.driver).get_counter_items()
        assert title_from_table_item == title_from_details, 'Title no match'
        assert counter_before > counter_after, 'Deletion error'

    def test_download_playlist(self):
        playlists_list_page = PlaylistsListPage(self.driver, 'https://cms-test.cubicservice.ru/playlists/list')
        playlists_list_page.open()
        title_from_download, title_from_playlists = playlists_list_page.download_playlist()
        assert title_from_download == title_from_playlists, 'Download error'

    def test_add_remove_track(self):
        playlists_list_page = PlaylistsListPage(self.driver, 'https://cms-test.cubicservice.ru/playlists/list')
        playlists_list_page.open()
        add_counters, del_counters, add_counters_with_active, del_counters_with_active \
            = playlists_list_page.add_remove_track()
        assert add_counters[0] == add_counters[1], \
            'The number of selected tracks does not match the counter'
        assert del_counters[0] == del_counters[1], \
            'The number of selected tracks does not match the counter'
        assert add_counters_with_active[0] == add_counters_with_active[1], \
            'The number of selected tracks does not match the counter'
        assert del_counters_with_active[0] == del_counters_with_active[1], \
            'The number of selected tracks does not match the counter'

    def test_search_track(self):
        playlists_list_page = PlaylistsListPage(self.driver, 'https://cms-test.cubicservice.ru/playlists/list')
        playlists_list_page.open()

        tl_list_before_search, tl_search_input_after_clear, tl_list_after_clear_search_input \
            = playlists_list_page.check_state_track_lists_table()

        pl_list_before_search, pl_search_input_after_clear, pl_list_after_clear_search_input \
            = playlists_list_page.check_state_playlist_table()

        tl_search_request, tl_result = playlists_list_page.search_tracks_in_track_list()
        pl_search_request, pl_result = playlists_list_page.search_tracks_in_playlist()

        assert tl_list_before_search == tl_list_after_clear_search_input, 'Incorrect result'
        assert tl_search_input_after_clear == '', 'Clear error'
        assert tl_search_request.lower() in tl_result.lower(), 'Incorrect search result'

        assert pl_list_before_search == pl_list_after_clear_search_input, 'Incorrect result'
        assert pl_search_input_after_clear == '', 'Clear error'
        assert pl_search_request.lower() in pl_result.lower(), 'Incorrect search result'

    def test_search_playlists_in_selected_modal(self):
        playlists_list_page = PlaylistsListPage(self.driver, 'https://cms-test.cubicservice.ru/playlists/list')
        playlists_list_page.open()
        list_before_search, search_input_after_clear, list_after_clear_search_input \
            = playlists_list_page.check_state_selected_modal_table()
        search_request, result = playlists_list_page.search_playlists_in_selected_modal()
        assert list_before_search == list_after_clear_search_input, 'Incorrect result'
        assert search_input_after_clear == '', 'Clear error'
        assert search_request.lower() in result.lower(), 'Incorrect search result'

    def test_import_tracks_from_other_playlists(self):
        playlists_list_page = PlaylistsListPage(self.driver, 'https://cms-test.cubicservice.ru/playlists/list')
        playlists_list_page.open()
        counter_currents_items, counter_after_import = playlists_list_page.import_tracks_from_other_playlists()
        assert counter_currents_items == counter_after_import, 'Incorrect import result'

    # Playlists_download_page
    def test_delete_playlists_from_download(self):
        playlists_download_page = PlaylistsDownloadPage(self.driver,
                                                        'https://cms-test.cubicservice.ru/playlists/download')
        playlists_download_page.open()
        counter_before = CommonMethods(self.driver).get_counter_items()
        selected_items_amount, delete_icon_counter = playlists_download_page.delete_playlists()
        counter_after = CommonMethods(self.driver).get_counter_items()
        assert selected_items_amount == delete_icon_counter, 'The quantity does not match the counter'
        assert counter_before > counter_after, 'Deletion error'

    def test_search_playlists_download(self):
        playlists_download_page = PlaylistsDownloadPage(self.driver,
                                                        'https://cms-test.cubicservice.ru/playlists/download')
        playlists_download_page.open()
        list_before_search, search_input_after_clear, list_after_clear_search_input \
            = playlists_download_page.check_state_playlists_table()
        search_request, result = playlists_download_page.search_playlist()
        assert list_before_search == list_after_clear_search_input, 'Incorrect result'
        assert search_input_after_clear == ''
        assert search_request.lower() in result.lower(), 'Incorrect search result'

    # Playlists_compare_page
    def test_compare_button(self):
        playlists_compare_page = PlaylistsComparePage(self.driver, 'https://cms-test.cubicservice.ru/playlists/compare')
        playlists_compare_page.open()
        button_status, counter_button = playlists_compare_page.check_status_and_counter_compare_button()
        assert button_status == ['true', 'true', None, None, 'true'], 'Incorrect status of the button'
        assert counter_button == ['0', '1', '2', '10', '11'], 'Incorrect counter of the button'

    def test_compare_playlists(self):
        playlists_compare_page = PlaylistsComparePage(self.driver, 'https://cms-test.cubicservice.ru/playlists/compare')
        playlists_compare_page.open()
        amount_of_shared_tracks = playlists_compare_page.compare_playlists()
        assert amount_of_shared_tracks == 3, 'Amount of shared tracks no match'

    # licenses_page
    def test_search_in_license_tree(self):
        playlists_license_page = PlaylistsLicensesPage(self.driver,
                                                       'https://cms-test.cubicservice.ru/playlists/licenses')
        playlists_license_page.open()
        list_before_search, search_input_after_clear, list_after_clear_search_input = \
            playlists_license_page.check_state_license_tree()
        search_request, result = playlists_license_page.search_in_license_tree()
        assert list_before_search == list_after_clear_search_input, 'Incorrect result'
        assert search_input_after_clear == ''
        assert search_request.lower() in result.lower(), 'Incorrect search result'

    def test_create_licenses_and_categories(self):
        playlists_license_page = PlaylistsLicensesPage(self.driver,
                                                       'https://cms-test.cubicservice.ru/playlists/licenses')
        playlists_license_page.open()
        assert playlists_license_page.create_license() == playlists_license_page.ITEM_TITLE, 'Create license error'
        assert playlists_license_page.create_category_type() == playlists_license_page.ITEM_TITLE, \
            'Create category type error'
        assert playlists_license_page.create_category() == playlists_license_page.ITEM_TITLE, 'Create category error'

    def test_change_display_type(self):
        playlists_license_page = PlaylistsLicensesPage(self.driver,
                                                       'https://cms-test.cubicservice.ru/playlists/licenses')
        playlists_license_page.open()
        license_result = playlists_license_page.change_display_type_in_license()
        playlists_license_page.go_to_down_item_in_tree()
        category_type_result = playlists_license_page.change_display_type_in_category_tree()
        playlists_license_page.go_to_down_item_in_tree()
        category_result = playlists_license_page.change_display_type_in_category_tree()
        assert 'Failed change display type' not in license_result
        assert 'Failed change display type' not in category_type_result
        assert 'Failed change display type' not in category_result

    def test_edit_category_fields(self):
        playlist_licence_page = PlaylistsLicensesPage(self.driver,
                                                      'https://cms-test.cubicservice.ru/playlists/licenses')
        playlist_licence_page.open()
        fields_values, fields_values_after_refresh = playlist_licence_page.edit_category_fields()
        assert fields_values == fields_values_after_refresh
        assert playlist_licence_page.check_promotion_period() == playlist_licence_page.ICON_FOUND_MESSAGE

    def test_search_playlist_in_cat_page(self):
        playlist_licence_page = PlaylistsLicensesPage(self.driver,
                                                      'https://cms-test.cubicservice.ru/playlists/licenses')
        playlist_licence_page.open()
        list_before_search, search_input_after_clear, list_after_clear_search_input \
            = playlist_licence_page.check_state_cat_page_table()
        search_request, result = playlist_licence_page.search_playlists_in_category_page()
        assert list_before_search == list_after_clear_search_input, 'Incorrect result'
        assert search_input_after_clear == ''
        assert search_request.lower() in result.lower(), 'Incorrect search result'

    def test_rename_licenses_and_categories(self):
        playlists_license_page = PlaylistsLicensesPage(self.driver,
                                                       'https://cms-test.cubicservice.ru/playlists/licenses')
        playlists_license_page.open()
        lic_after_rename_from_context, lic_after_rename_from_block = playlists_license_page.rename_license()
        cat_tp_after_rename_from_context, cat_tp_after_rename_from_block = playlists_license_page.rename_category_type()
        cat_after_rename_from_context, cat_after_rename_from_block = playlists_license_page.rename_category()
        assert lic_after_rename_from_context == playlists_license_page.TITLE_FOR_RENAME_FROM_CONTEXT, 'Rename error'
        assert lic_after_rename_from_block == playlists_license_page.TITLE_FOR_RENAME_FROM_BLOCK, 'Rename error'
        assert cat_tp_after_rename_from_context == playlists_license_page.TITLE_FOR_RENAME_FROM_CONTEXT, 'Rename error'
        assert cat_tp_after_rename_from_block == playlists_license_page.TITLE_FOR_RENAME_FROM_BLOCK, 'Rename error'
        assert cat_after_rename_from_context == playlists_license_page.TITLE_FOR_RENAME_FROM_CONTEXT, 'Rename error'
        assert cat_after_rename_from_block == playlists_license_page.TITLE_FOR_RENAME_FROM_BLOCK, 'Rename error'

    def test_delete_licenses_and_categories(self):
        playlists_license_page = PlaylistsLicensesPage(self.driver,
                                                       'https://cms-test.cubicservice.ru/playlists/licenses')
        playlists_license_page.open()
        delete_category = playlists_license_page.delete_category()
        list_len_before, list_len_after = playlists_license_page.delete_category_type()
        delete_license = playlists_license_page.delete_license()
        assert delete_category == playlists_license_page.NOT_FOUND_MESSAGE
        assert list_len_before > list_len_after
        assert delete_license == playlists_license_page.NOT_FOUND_MESSAGE

