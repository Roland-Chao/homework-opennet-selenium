from selenium import webdriver

def get_chrome_options(device: str = "desktop") -> webdriver.ChromeOptions:
    options = webdriver.ChromeOptions()

    # Common arguments
    options.add_argument('--start-maximized')
    options.add_argument('--autoplay-policy=no-user-gesture-required')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=IsolateOrigins,site-per-process')
    options.add_argument('--enable-features=NetworkService,NetworkServiceInProcess')
    options.add_argument('--ignore-certificate-errors')

    if device.lower() == "mobile":
        user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/132.0 Mobile/15E148 Safari/605.1.15'
        options.add_argument(f'user-agent={user_agent}')

        options.add_argument('--window-size=390,844')  # iPhone 15 size
    else:
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.7444.176 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')

    # Experimental options
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Preferences
    prefs = {
        'profile.default_content_setting_values': {
          'notifications': 2,        # Block notifications
          'geolocation': 2,          # Block geolocation requests
          'media_stream': 2,         # Block media stream (camera/microphone) requests
          'automatic_downloads': 1,  # Allow automatic downloads
        },
        'intl.accept_languages': 'en-US'  # English (US)
    }
    options.add_experimental_option('prefs', prefs)

    return options
