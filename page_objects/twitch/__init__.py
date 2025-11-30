from .home_page.action import HomePageAction
from .search_page.action import SearchPageAction


class TwitchPages:
    def __init__(self, driver):
        self.home = HomePageAction(driver)
        self.search = SearchPageAction(driver)
