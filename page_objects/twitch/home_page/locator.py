from library.element import Element
from selenium.webdriver.common.by import By

class HomePageLocator:
    def __init__(self, driver):
        self.driver = driver

    def footer_browse_link(self) -> Element:
        return Element(
            name="Footer - Browse Link",
            by=By.XPATH,
            selector='//a[contains(@class, "ScInteractableBase") and @href="/directory"]'
        )
