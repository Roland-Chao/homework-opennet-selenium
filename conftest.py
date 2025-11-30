import pytest, allure, base64
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from library.page_utils import PageUtils
from library.file_handler import FileHandler
from config.browser_config import get_chrome_options

# Load environment variables from .env file
load_dotenv()

def pytest_addoption(parser):
    parser.addoption(
        "--device-type",
        action="store",
        default="mobile",
        choices=["mobile", "desktop"],
        help="Device type for browser emulation: mobile or desktop (default: mobile)"
    )
    parser.addoption(
        "--page-load-timeout",
        action="store",
        type=int,
        default=60,
        help="Page load timeout in seconds (default: 60)"
    )

def load_test_data(file_path):
    return FileHandler().read_json_file(file_path)

@pytest.fixture(scope="function")
def driver(request):
    device = request.config.getoption("--device-type")

    if not hasattr(request.node, 'screenshot_path_list'):
        request.node.screenshot_path_list = []

    file_handler = FileHandler()

    # Setup Chrome driver with options
    chrome_options = get_chrome_options(device=device)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Set page load timeout from pytest options
    driver.set_page_load_timeout(request.config.getoption("--page-load-timeout"))

    page_utils = PageUtils(driver)
    yield driver

    # Screenshot capture
    with allure.step("Capture browser screenshots"):
        try:
            window_handles = driver.window_handles
            with allure.step(f"Found {len(window_handles)} window(s)"):
                for i, handle in enumerate(window_handles):
                    try:
                        with allure.step(f"Capture screenshot for window #{i + 1}"):
                            screenshot_path = f"allure-results/{request.node.name}_{i}.png"

                            # Switch to window by handle (not index) to avoid stale references
                            driver.switch_to.window(handle)

                            # Verify window is still valid before screenshot
                            if driver.current_url:
                                page_utils.page_screenshot(
                                    save_path=screenshot_path,
                                    full_page=True
                                )
                                request.node.screenshot_path_list.append(screenshot_path)
                    except Exception as e:
                        print(f"Failed to capture screenshot for window #{i + 1}: {e}")
        except Exception as e:
            print(f"Failed to get window handles: {e}")

    driver.quit()

    # Write screenshot information to Allure report
    if request.node.screenshot_path_list:
        with allure.step("Write screenshot information to Allure"):
            description = f"""<body><h3>Test Screenshots</h3>"""
            for index, screenshot_path in enumerate(request.node.screenshot_path_list, start=1):
                png = file_handler.find_file_path(screenshot_path)
                with open(png, "rb") as img_file:
                    img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
                description += f"""<img src="data:image/png;base64,{img_base64}" alt="Browser screenshot #{index}"\
                    style="width: 100%; max-width: 1200px; height: auto; object-fit: contain; margin-bottom: 20px; cursor: pointer;"
                    onclick="window.open(this.src, '_blank');">"""
            description += """</body>"""
            allure.dynamic.description_html(description)
