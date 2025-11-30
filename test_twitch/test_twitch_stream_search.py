import allure, pytest
from pathlib import Path
from library.page_utils import PageUtils
from page_objects.twitch import TwitchPages
from conftest import load_test_data

@pytest.mark.UI
@allure.parent_suite("Twitch WAP")
@allure.suite("Search Stream")
class TestTwitchSearch():
    DATA_DIR = Path(__file__).parent / "case_data"

    @pytest.mark.twitch
    @allure.sub_suite("Search Stream Success Test")
    @allure.title("Twitch search stream and select streamer by index")
    def test_twitch_search(self, driver):
        test_data = load_test_data(str(self.DATA_DIR / "twitch_search"))

        page_utils = PageUtils(driver)
        twitch = TwitchPages(driver)

        page_utils.goto_url(test_data["url"])

        twitch.home.click_footer_browse_link()
        
        twitch.search.wait_for_main_content_appear()

        twitch.search.search_stream(test_data["search_keyword"])

        twitch.search.check_search_result()

        page_utils.scroll_page(y=test_data["scroll"]["y"], count=test_data["scroll"]["count"])

        twitch.search.select_stream_by_index(test_data["stream_index"])

        twitch.search.handle_content_classification_gate()

        twitch.search.wait_for_video_player_appear_and_start_playing()
        
        with allure.step("Take screenshot"):
            allure.attach.file(
                page_utils.page_screenshot(save_path="allure-results/screenshot.png", full_page=True), 
                name="Screenshot", 
                attachment_type=allure.attachment_type.PNG
            )
