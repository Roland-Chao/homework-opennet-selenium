from library.element import Element
from selenium.webdriver.common.by import By

class SearchPageLocator:
    def __init__(self, driver):
        self.driver = driver

    def search_input(self) -> Element:
        return Element(
            name="Search Input",
            by=By.XPATH,
            selector='//input[@type="search"]'
        )

    def page_main_content_wrapper(self) -> Element:
        return Element(
            name="Page Main Content Wrapper",
            by=By.XPATH,
            selector='//main[@id="page-main-content-wrapper"]'
        )

    def stream_list(self, index: int = None) -> Element:
        name = "Stream List"
        selector = '//h2[text()="Channels"]/ancestor::div/following-sibling::div//button'
        if index:
            name = f"Stream #{index}"

        return Element(
            name=name,
            by=By.XPATH,
            selector=selector
        )

    def search_result_warning_text(self) -> Element:
        return Element(
            name="Search Result Warning Text",
            by=By.XPATH,
            selector='//h2[text()="Please try a different keyword"]'
        )

    def video_player(self) -> Element:
        return Element(
            name="Video Player",
            by=By.XPATH,
            selector='//div[@data-a-target="video-player"]'
        )

    def content_classification_gate_overlay(self) -> Element:
        return Element(
            name="Content Classification Gate Overlay",
            by=By.XPATH,
            selector='//div[@data-a-target="content-classification-gate-overlay"]'
        )

    def content_classification_gate_button(self) -> Element:
        return Element(
            name="Content Classification Gate Button - Start Watching",
            by=By.XPATH,
            selector='//div[@data-a-target="tw-core-button-label-text" and text()="Start Watching"]'
        )
