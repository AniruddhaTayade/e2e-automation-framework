from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class InventoryPage(BasePage):
    _TITLE = (By.CLASS_NAME, "title")
    _ITEMS = (By.CLASS_NAME, "inventory_item")
    _ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    _SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    _CART_ICON = (By.CLASS_NAME, "shopping_cart_link")

    def get_page_title(self) -> str:
        return self.get_text(self._TITLE)

    def get_item_count(self) -> int:
        return len(self.find_all(self._ITEMS))

    def get_item_names(self) -> list[str]:
        return [el.text for el in self.find_all(self._ITEM_NAMES)]

    def get_item_prices(self) -> list[float]:
        return [float(el.text.replace("$", "")) for el in self.find_all(self._ITEM_PRICES)]

    def sort_by(self, option: str):
        """option values: 'az', 'za', 'lohi', 'hilo'"""
        select = Select(self.find(self._SORT_DROPDOWN))
        select.select_by_value(option)

    def add_item_to_cart(self, item_name: str):
        safe_name = item_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
        locator = (By.ID, f"add-to-cart-{safe_name}")
        self.click(locator)

    def remove_item_from_cart(self, item_name: str):
        safe_name = item_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
        locator = (By.ID, f"remove-{safe_name}")
        self.click(locator)

    def get_cart_badge_count(self) -> int:
        if not self.is_displayed(self._CART_BADGE):
            return 0
        return int(self.get_text(self._CART_BADGE))

    def go_to_cart(self):
        self.click(self._CART_ICON)
