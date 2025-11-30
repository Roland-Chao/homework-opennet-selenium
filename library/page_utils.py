import allure
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from library.logger import HandleLog
from library.element import Element
from library.exception import *


def page_utils_exception(error_message_template):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)

            except TimeoutException:
                format_kwargs = {**kwargs, 'self': self}
                timeout_seconds = self.element_wait_time
                error_msg = error_message_template.format(**format_kwargs)
                raise PageUtilsTimeoutException(f"{error_msg}, timeout after {timeout_seconds} seconds")

            except CustomException:
                raise

            except Exception as e:
                raise CustomException(
                    f"[{func.__name__}] Execution error:\n"
                    f"    Method: {func.__name__}\n"
                    f"    Arguments: {kwargs}\n"
                    f"    Error: {str(e)}"
                )

        return wrapper
    return decorator

class PageUtils:
    DEFAULT_TIMEOUT = int(os.getenv('ELEMENT_TIMEOUT', '10'))

    def __init__(self, driver: webdriver.Remote, element_wait_time: int = None, poll_frequency: float = 0.5):
        self.host = '[PageUtils]'
        self.driver = driver
        self.element_wait_time = element_wait_time or self.DEFAULT_TIMEOUT
        self.poll_frequency = poll_frequency
        self.browser_wait = WebDriverWait(driver, timeout=self.element_wait_time, poll_frequency=poll_frequency)
        self.action_chains = ActionChains(self.driver)
        self.log = HandleLog()

    def _get_wait(self, timeout: int = None) -> WebDriverWait:
        wait_time = timeout if timeout else self.element_wait_time
        return WebDriverWait(self.driver, timeout=wait_time, poll_frequency=self.poll_frequency)

    def _log_duration(self, start_time: datetime, action: str, element_name: str = None):
        end_time = datetime.now()
        duration = end_time - start_time
        formatted_duration = "{:.2f}".format(duration.total_seconds())

        if element_name:
            self.log.info_log(f"{self.host} {action}: <{element_name}>, duration: {formatted_duration}s")
        else:
            self.log.info_log(f"{self.host} {action}, duration: {formatted_duration}s")

    @page_utils_exception(error_message_template="{self.host} Navigate to URL failed")
    def goto_url(self, url: str, is_wait_for_load: bool = False):
        start_time = datetime.now()

        with allure.step(f"Navigate to {url}"):
            self.driver.get(url)

            if is_wait_for_load:
                self.wait_for_fully_loaded()

            self._log_duration(start_time, f"Navigate to {url}")

    @page_utils_exception(error_message_template="{self.host} Get current URL failed")
    def get_current_url(self) -> str:
        current_url = self.driver.current_url
        self.log.info_log(f"{self.host} Get current URL: {current_url}")
        return current_url

    @page_utils_exception(error_message_template="{self.host} Wait for URL timeout")
    def wait_for_url(self, expected_url: str, timeout: int = None):
        start_time = datetime.now()
        wait = self._get_wait(timeout)

        wait.until(EC.url_to_be(expected_url))
        self._log_duration(start_time, f"Wait for URL: {expected_url}")

    @page_utils_exception(error_message_template="{self.host} Wait for page load timeout")
    def wait_for_fully_loaded(self, timeout: int = None):
        wait = self._get_wait(timeout)
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        self.log.info_log(f"{self.host} Page fully loaded")

    @page_utils_exception(error_message_template="{self.host} Element not found: {element}")
    def find_element_visible(self, element: Element, timeout: int = None):
        start_time = datetime.now()
        wait = self._get_wait(timeout)

        web_element = wait.until(
            EC.visibility_of_element_located((element.by, element.selector)),
            message=f"{self.host} Element not found: {element}"
        )
        self._log_duration(start_time, "Find element", element.name)
        return web_element

    @page_utils_exception(error_message_template="{self.host} Elements not found: {element}")
    def find_elements_visible(self, element: Element, timeout: int = None):
        start_time = datetime.now()
        wait = self._get_wait(timeout)

        web_elements = wait.until(
            EC.visibility_of_all_elements_located((element.by, element.selector)),
            message=f"{self.host} Elements not found: {element}"
        )
        end_time = datetime.now()
        duration = end_time - start_time
        formatted_duration = "{:.2f}".format(duration.total_seconds())

        self.log.info_log(f"{self.host} Find all elements: <{element.name}>, count: {len(web_elements)}, duration: {formatted_duration}s")
        return web_elements

    @page_utils_exception(error_message_template="{self.host} Clickable element not found: {element}")
    def find_clickable_element(self, element: Element, timeout: int = None):
        start_time = datetime.now()
        wait = self._get_wait(timeout)

        web_element = wait.until(
            EC.element_to_be_clickable((element.by, element.selector)),
            message=f"{self.host} Clickable element not found: {element}"
        )
        self._log_duration(start_time, "Find clickable element", element.name)
        return web_element

    @page_utils_exception(error_message_template="{self.host} Element not located: {element}")
    def find_element_located(self, element: Element, timeout: int = None):
        start_time = datetime.now()
        wait = self._get_wait(timeout)

        web_element = wait.until(
            EC.presence_of_element_located((element.by, element.selector)),
            message=f"{self.host} Element not located: {element}"
        )
        self._log_duration(start_time, "Locate element", element.name)
        return web_element

    @page_utils_exception(error_message_template="{self.host} Element not visible: {element}")
    def check_element_visible(self, element: Element, timeout: int = 5):
        try:
            self.find_element_visible(element, timeout=timeout)
            self.log.info_log(f"{self.host} Element <{element.name}> is visible")
            return True

        except Exception:
            self.log.info_log(f"{self.host} Element <{element.name}> is not visible")
            return False

    @page_utils_exception(error_message_template="{self.host} Element still visible: {element}")
    def wait_for_element_invisible(self, element: Element, timeout: int = None):
        start_time = datetime.now()
        wait = self._get_wait(timeout)

        is_invisible = wait.until(
            EC.invisibility_of_element_located((element.by, element.selector)),
            message=f"{self.host} Element still visible: {element}"
        )
        self._log_duration(start_time, f"Wait for element invisible: {element.name}")
        return is_invisible

    @page_utils_exception(error_message_template="{self.host} Click element failed: {element}")
    def click_button(self, element: Element, retries: int = 3, delay: int = 1, should_roll: bool = True, timeout: int = None):
        attempt = 0

        while attempt < retries:
            try:
                web_element = self.find_clickable_element(element, timeout)

                if should_roll:
                    self.roll_to_element(web_element, element.name)

                try:
                    web_element.click()
                    self.log.info_log(f"{self.host} Click element: <{element.name}> success")
                    return

                except ElementClickInterceptedException:
                    # Fallback to JavaScript click
                    self.log.info_log(f"{self.host} Standard click failed, trying JavaScript click...")
                    self.driver.execute_script("arguments[0].click();", web_element)
                    self.log.info_log(f"{self.host} Click element: <{element.name}> success (JavaScript)")
                    return

            except Exception as e:
                attempt += 1
                self.log.error_log(f"{self.host} Click element: <{element.name}> failed, attempt: {attempt}/{retries}")

                if attempt >= retries:
                    error_message = f"{self.host} Click element: {element} failed after {retries} attempts"
                    self.log.error_log(error_message)
                    raise CustomException(error_message)

                time.sleep(delay)

    @page_utils_exception(error_message_template="{self.host} Click element failed: {element}")
    def click_element(self, element: Element, is_wait_for_load: bool = False, timeout: int = None):
        self.click_button(element, retries=1, should_roll=True, timeout=timeout)

        if is_wait_for_load:
            self.wait_for_fully_loaded()

    @page_utils_exception(error_message_template="{self.host} Element not visible, skip clicking: {element}")
    def click_if_visible(self, element: Element, timeout: int = 5) -> bool:
        try:
            if self.check_element_visible(element, timeout):
                self.click_element(element, timeout=timeout)
                return True
            return False

        except Exception:
            self.log.info_log(f"{self.host} Element <{element.name}> not visible, skip clicking")
            return False

    @page_utils_exception(error_message_template="{self.host} Input to element failed: {element}")
    def input_value_to_element(self, element: Element, value: str, is_clear: bool = True,
                              need_enter: bool = False, is_wait_for_load: bool = False, timeout: int = None):
        self.log.info_log(f"{self.host} Input text: {value} to: {element.name}")

        web_element = self.find_clickable_element(element, timeout)
        self.roll_to_element(web_element, element.name)

        if is_clear:
            self.log.info_log(f"{self.host} Clear element: {element.name}")
            web_element.clear()
            time.sleep(0.5)

        web_element.send_keys(str(value))

        if need_enter:
            web_element.send_keys(Keys.RETURN)

        if is_wait_for_load:
            self.wait_for_fully_loaded()

        self.log.info_log(f"{self.host} Input to <{element.name}> success")

    @page_utils_exception(error_message_template="{self.host} Send key to element failed: {element}")
    def send_key_to_element(self, element: Element, key: str = "Enter", is_wait_for_load: bool = False):
        key_mapping = {
            "Enter": Keys.RETURN,
            "Tab": Keys.TAB,
            "Escape": Keys.ESCAPE,
            "ArrowDown": Keys.ARROW_DOWN,
            "ArrowUp": Keys.ARROW_UP,
        }

        self.log.info_log(f"{self.host} Send key: {key} to element: {element.name}")
        web_element = self.find_element_located(element)

        selenium_key = key_mapping.get(key, key)
        web_element.send_keys(selenium_key)

        if is_wait_for_load:
            self.wait_for_fully_loaded()

    @page_utils_exception(error_message_template="{self.host} Get element text failed: {element}")
    def get_element_text(self, element: Element, timeout: int = None) -> str:
        web_element = self.find_element_visible(element, timeout)
        text = web_element.text
        self.log.info_log(f"{self.host} Get element <{element.name}> text: {text}")
        return text

    @page_utils_exception(error_message_template="{self.host} Get all elements text failed: {element}")
    def get_all_elements_text(self, element: Element, is_clean: bool = False, timeout: int = None) -> list:
        web_elements = self.find_elements_visible(element, timeout)
        text_list = [elem.text for elem in web_elements]

        if is_clean:
            text_list = [text.replace('\n', ' ').strip() for text in text_list]

        self.log.info_log(f"{self.host} Get all elements <{element.name}> text, count: {len(text_list)}")
        return text_list

    @page_utils_exception(error_message_template="{self.host} Get elements count failed: {element}")
    def get_elements_count(self, element: Element, timeout: int = None) -> int:
        web_elements = self.find_elements_visible(element, timeout)
        count = len(web_elements)
        self.log.info_log(f"{self.host} Get elements <{element.name}> count: {count}")
        return count

    @page_utils_exception(error_message_template="{self.host} Get element attribute failed: {element}")
    def get_element_attribute_value(self, element: Element, attribute: str, timeout: int = None):
        web_element = self.find_element_visible(element, timeout)
        value = web_element.get_attribute(attribute)
        self.log.info_log(f"{self.host} Get element <{element.name}> attribute: {attribute} = {value}")
        return value

    @page_utils_exception(error_message_template="{self.host} Get element input value failed: {element}")
    def get_element_input_value(self, element: Element, timeout: int = None):
        return self.get_element_attribute_value(element, "value", timeout)

    @page_utils_exception(error_message_template="{self.host} Check element state failed: {element}")
    def check_element_state(self, element: Element, state: str = "visible", timeout: int = None) -> bool:
        valid_states = ["visible", "invisible", "clickable", "enabled", "disabled"]

        if state not in valid_states:
            raise ValueError(f"Invalid state: {state}. Valid states: {', '.join(valid_states)}")

        self.log.info_log(f"{self.host} Check element <{element.name}> state: {state}")

        try:
            wait = self._get_wait(timeout)

            if state == "visible":
                wait.until(EC.visibility_of_element_located((element.by, element.selector)))
                return True

            elif state == "invisible":
                wait.until(EC.invisibility_of_element_located((element.by, element.selector)))
                return True

            elif state == "clickable":
                wait.until(EC.element_to_be_clickable((element.by, element.selector)))
                return True

            elif state in ["enabled", "disabled"]:
                web_element = self.find_element_located(element, timeout)
                is_enabled = web_element.is_enabled()
                return is_enabled if state == "enabled" else not is_enabled

        except TimeoutException:
            self.log.info_log(f"{self.host} Element <{element.name}> state check failed: {state}")
            return False

    @page_utils_exception(error_message_template="{self.host} Wait for element state timeout: {element}")
    def wait_for_element_state(self, element: Element, state: str, timeout: int = None):
        if not self.check_element_state(element, state, timeout):
            error_message = f"{self.host} Wait for element {element.name} state: {state} timeout"
            self.log.error_log(error_message)
            raise CustomException(error_message)

    @page_utils_exception(error_message_template="{self.host} Scroll to element failed")
    def roll_to_element(self, element, element_name: str = None, block_position: str = "center"):
        if isinstance(element, Element):
            web_element = self.find_element_visible(element)
            name = element.name
        else:
            web_element = element
            name = element_name or "element"

        self.log.info_log(f"{self.host} Scroll to element: <{name}>, position: {block_position}")
        self.driver.execute_script(f"arguments[0].scrollIntoView({{block: '{block_position}', behavior: 'smooth'}});", web_element)
        time.sleep(0.5)

    @page_utils_exception(error_message_template="{self.host} Scroll page failed")
    def scroll_page(self, x: int = 0, y: int = 0, count: int = 1, wait_timeout: int = 2):
        for i in range(count):
            self.driver.execute_script(f"window.scrollBy({x}, {y})")
            self.log.info_log(f"{self.host} Scroll page ({x}, {y}) - {i+1}/{count}")

            if wait_timeout > 0:
                time.sleep(wait_timeout)

            # Check if reached bottom after waiting
            if i < count - 1:  # Only check if not last iteration
                old_scroll_y = self.driver.execute_script("return window.pageYOffset")
                self.driver.execute_script(f"window.scrollBy(0, 1)")  # Try scroll 1px
                time.sleep(0.1)
                new_scroll_y = self.driver.execute_script("return window.pageYOffset")

                if new_scroll_y == old_scroll_y:
                    self.log.info_log(f"{self.host} Reached bottom, stop scrolling (Total {i+1})")
                    break
                else:
                    # Scroll back if not at bottom
                    self.driver.execute_script(f"window.scrollBy(0, -1)")

    @page_utils_exception(error_message_template="{self.host} Move to element failed: {element}")
    def move_to_element(self, element: Element):
        self.log.info_log(f"{self.host} Move mouse to element: <{element.name}>")
        web_element = self.find_clickable_element(element)
        self.action_chains.move_to_element(web_element).perform()

    @page_utils_exception(error_message_template="{self.host} Move to element and click failed: {element}")
    def move_to_element_and_click(self, element: Element):
        self.log.info_log(f"{self.host} Move to element and click: <{element.name}>")
        web_element = self.find_element_located(element)
        self.action_chains.move_to_element(web_element).click().perform()

    @page_utils_exception(error_message_template="{self.host} Switch window failed")
    def switch_window(self, index: int = -1, is_wait_for_load: bool = True):
        self.log.info_log(f"{self.host} Switch to window index: {index}")
        all_windows = self.driver.window_handles
        self.driver.switch_to.window(all_windows[index])

        if is_wait_for_load:
            self.wait_for_fully_loaded()

        self.log.info_log(f"{self.host} Switched to window: {self.get_current_url()}")

    @page_utils_exception(error_message_template="{self.host} Get window count failed")
    def get_page_count(self) -> int:
        count = len(self.driver.window_handles)
        self.log.info_log(f"{self.host} Window count: {count}")
        return count

    @page_utils_exception(error_message_template="{self.host} Close window failed")
    def close_current_window(self):
        self.log.info_log(f"{self.host} Close current window")
        self.driver.close()

    @page_utils_exception(error_message_template="{self.host} Wait for condition failed")
    def wait_for_condition(self, condition_func, timeout: int = None, message: str = ""):
        start_time = datetime.now()
        wait = self._get_wait(timeout)

        result = wait.until(condition_func, message=message or f"{self.host} Custom condition not met")

        self._log_duration(start_time, "Wait for condition", message)
        return result

    @page_utils_exception(error_message_template="{self.host} Screenshot failed")
    def page_screenshot(self, save_path: str, full_page: bool = False):
        if full_page:
            original_size = self.driver.get_window_size()
            required_width = self.driver.execute_script('return document.body.scrollWidth')
            required_height = self.driver.execute_script('return document.body.scrollHeight')
            self.driver.set_window_size(required_width, required_height)
            self.driver.save_screenshot(save_path)
            self.driver.set_window_size(original_size['width'], original_size['height'])
        else:
            self.driver.save_screenshot(save_path)
            
        self.log.info_log(f"{self.host} Screenshot saved: {save_path}")
        return save_path
        
