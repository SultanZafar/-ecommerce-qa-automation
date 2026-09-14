from playwright.sync_api import Page

class BasePage:
    def __init__(self,page: Page):
        self.page = page

    def goto(self, url: str):
        self.page.goto(url)

    def click(self,locator: str):
        self.page.click(locator)

    def fill(self, locator: str, text: str):
        self.page.fill(locator, text)

    def get_text(self, locator: str)-> str:
        return self.page.inner_text(locator)