from library.page_utils import PageUtils
from library.allure import allure_attach_log
from library.validator import Validator
from page_objects.twitch.home_page.locator import HomePageLocator

class HomePageAction(PageUtils, HomePageLocator):
    def __init__(self, driver):
        PageUtils.__init__(self, driver)
        HomePageLocator.__init__(self, driver)
        self.validator = Validator()

    @allure_attach_log(log_name="Click Footer - Browse Link")
    def click_footer_browse_link(self):
        self.click_element(self.footer_browse_link(), timeout=0)
