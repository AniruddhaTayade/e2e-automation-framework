from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CartPage(BasePage):
    _TITLE = (By.CLASS_NAME, "title")
    _CART_ITEMS = (By.CLASS_NAME, "cart_item")
    _ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    _CONTINUE_SHOPPING = (By.ID, "continue-shopping")
    _CHECKOUT_BTN = (By.ID, "checkout")

    # Checkout step 1
    _FIRST_NAME = (By.ID, "first-name")
    _LAST_NAME = (By.ID, "last-name")
    _ZIP_CODE = (By.ID, "postal-code")
    _CONTINUE_BTN = (By.ID, "continue")

    # Checkout step 2
    _FINISH_BTN = (By.ID, "finish")
    _SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")

    # Checkout complete
    _COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def get_page_title(self) -> str:
        return self.get_text(self._TITLE)

    def get_cart_item_count(self) -> int:
        items = self.driver.find_elements(*self._CART_ITEMS)
        return len(items)

    def get_cart_item_names(self) -> list[str]:
        return [el.text for el in self.find_all(self._ITEM_NAMES)]

    def get_cart_item_prices(self) -> list[float]:
        return [float(el.text.replace("$", "")) for el in self.find_all(self._ITEM_PRICES)]

    def remove_item(self, item_name: str):
        safe_name = item_name.lower().replace(" ", "-").replace("(", "").replace(")", "")
        locator = (By.ID, f"remove-{safe_name}")
        self.click(locator)

    def continue_shopping(self):
        self.click(self._CONTINUE_SHOPPING)

    def proceed_to_checkout(self):
        self.click(self._CHECKOUT_BTN)
        self.wait.until(EC.url_contains("checkout-step-one"))

    def fill_checkout_info(self, first_name: str, last_name: str, zip_code: str):
        def _js_fill(element_id, value):
            el = self.driver.find_element(By.ID, element_id)
            self.driver.execute_script("arguments[0].focus()", el)
            self.driver.execute_script(
                "var nv=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;"
                "nv.call(arguments[0],arguments[1]);"
                "arguments[0].dispatchEvent(new Event('input',{bubbles:true}));"
                "arguments[0].dispatchEvent(new Event('change',{bubbles:true}));",
                el, value,
            )
            self.driver.execute_script("arguments[0].blur()", el)

        _js_fill("first-name", first_name)
        _js_fill("last-name", last_name)
        _js_fill("postal-code", zip_code)
        # SauceDemo is a React SPA — clicking the submit input in headless Chrome
        # doesn't reliably trigger navigation; dispatching a DOM submit event does.
        self.driver.execute_script(
            "document.querySelector('form').dispatchEvent(new Event('submit',{bubbles:true}))"
        )
        self.wait.until(EC.url_contains("checkout-step-two"))

    def get_order_total(self) -> str:
        return self.get_text(self._SUMMARY_TOTAL)

    def finish_order(self):
        btn = self.find_clickable(self._FINISH_BTN)
        self.driver.execute_script("arguments[0].click()", btn)
        self.wait.until(EC.url_contains("checkout-complete"))

    def get_completion_message(self) -> str:
        return self.get_text(self._COMPLETE_HEADER)
