import allure
import time
from library.page_utils import PageUtils
from library.allure import allure_attach_log
from page_objects.twitch.search_page.locator import SearchPageLocator
from library.validator import Validator
from library.exception import CustomException

class SearchPageAction(PageUtils, SearchPageLocator):
    def __init__(self, driver):
        PageUtils.__init__(self, driver)
        SearchPageLocator.__init__(self, driver)
        self.validator = Validator()
    
    @allure_attach_log(log_name="Search Stream")
    def search_stream(self, stream_name: str):
        with allure.step("Click search input"):
            self.click_element(self.search_input())

        with allure.step(f"Input search text: {stream_name}"):
            self.input_value_to_element(self.search_input(), stream_name, is_wait_for_load=True)

        with allure.step("Press Enter key"):
            self.send_key_to_element(self.search_input(), "Enter", is_wait_for_load=True)

    @allure_attach_log(log_name="Wait for Main Content Appear")
    def wait_for_main_content_appear(self):
        with allure.step("Wait for main content to appear"):
            self.validator.assert_is_equal(
                expected=True,
                actual=self.check_element_state(self.page_main_content_wrapper(), "visible")
            )

    @allure_attach_log(log_name="Check Search Result")
    def check_search_result(self):
        with allure.step("Check search result warning text"):
            result = self.check_element_state(self.search_result_warning_text(), "visible", timeout=3)

        if result:
            raise CustomException("No streams found")

    @allure_attach_log(log_name="Select Stream by Index")
    def select_stream_by_index(self, index: int):
        with allure.step("Get stream list count"):
            stream_count = self.get_elements_count(self.stream_list())

        if index > stream_count:
            raise CustomException(f"Stream #{index} does not exist, total {stream_count} streams")

        with allure.step(f"Select stream #{index}"):
            stream_elements = self.find_elements_visible(self.stream_list())

            if index <= len(stream_elements):
                target_element = stream_elements[index - 1]

                # Scroll to element and click
                self.roll_to_element(target_element, f"Stream #{index}")
                time.sleep(0.5)
                target_element.click()

    @allure_attach_log(log_name="Handle Content Classification Gate")
    def handle_content_classification_gate(self):
        with allure.step("Handle content classification gate if present"):
            self.click_if_visible(self.content_classification_gate_button(), timeout=5)

    @allure_attach_log(log_name="Wait for Video Player Appear")
    def wait_for_video_player_appear_and_start_playing(self):
        with allure.step("Wait for video player to appear"):
            self.wait_for_element_state(self.video_player(), "visible")

        with allure.step("Wait for video to start playing"):
            result =self.wait_for_condition(
                condition_func=lambda driver: driver.execute_script("""
                    const video_player = document.querySelector('video');
                    return video_player && video_player.currentTime > 0 && video_player.readyState >= 3;
                """),
                timeout=5,
                message="Video player ready"
            )
        
            self.validator.assert_is_equal(
                expected=True,
                actual=result,
                key="Video player ready"
            )