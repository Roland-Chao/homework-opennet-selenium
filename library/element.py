from selenium.webdriver.common.by import By

class Element:
    def __init__(self, name: str, locator: tuple = None, by: By = None, selector: str = None):
        self.name = name

        # Support both formats: locator tuple or by+selector
        if locator is not None:
            self.locator = locator
            self.by = locator[0]
            self.selector = locator[1]
        elif by is not None and selector is not None:
            self.by = by
            self.selector = selector
            self.locator = (by, selector)
        else:
            raise ValueError("Must provide either 'locator' tuple or both 'by' and 'selector'")

    def __str__(self):
        return f"Element: <{self.name}> Location: <{self.by}: {self.selector}>"