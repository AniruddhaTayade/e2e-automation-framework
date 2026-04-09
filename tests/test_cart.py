import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


class TestCart:
    def test_cart_shows_added_item(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_item_to_cart("Sauce Labs Backpack")
        inventory.go_to_cart()

        cart = CartPage(logged_in_driver)
        assert cart.get_page_title() == "Your Cart"
        assert cart.get_cart_item_count() == 1
        assert "Sauce Labs Backpack" in cart.get_cart_item_names()

    def test_cart_shows_correct_item_price(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_item_to_cart("Sauce Labs Backpack")
        inventory.go_to_cart()

        cart = CartPage(logged_in_driver)
        prices = cart.get_cart_item_prices()
        assert len(prices) == 1
        assert prices[0] == 29.99

    def test_cart_shows_multiple_items(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_item_to_cart("Sauce Labs Backpack")
        inventory.add_item_to_cart("Sauce Labs Bike Light")
        inventory.go_to_cart()

        cart = CartPage(logged_in_driver)
        assert cart.get_cart_item_count() == 2

    def test_remove_item_from_cart(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_item_to_cart("Sauce Labs Backpack")
        inventory.add_item_to_cart("Sauce Labs Bike Light")
        inventory.go_to_cart()

        cart = CartPage(logged_in_driver)
        cart.remove_item("Sauce Labs Backpack")
        assert cart.get_cart_item_count() == 1
        assert "Sauce Labs Bike Light" in cart.get_cart_item_names()

    def test_continue_shopping_returns_to_inventory(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.go_to_cart()

        cart = CartPage(logged_in_driver)
        cart.continue_shopping()
        assert "inventory" in logged_in_driver.current_url

    def test_full_checkout_flow_completes_order(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_item_to_cart("Sauce Labs Backpack")
        inventory.add_item_to_cart("Sauce Labs Bike Light")
        inventory.go_to_cart()

        cart = CartPage(logged_in_driver)
        cart.proceed_to_checkout()
        cart.fill_checkout_info("Jane", "Doe", "94043")  # waits for step-two internally

        total = cart.get_order_total()
        assert "$" in total

        cart.finish_order()  # waits for checkout-complete internally

        msg = cart.get_completion_message()
        assert "Thank you" in msg

    def test_checkout_url_progression(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_item_to_cart("Sauce Labs Backpack")
        inventory.go_to_cart()

        cart = CartPage(logged_in_driver)
        assert "cart" in logged_in_driver.current_url

        cart.proceed_to_checkout()
        assert "checkout-step-one" in logged_in_driver.current_url

        cart.fill_checkout_info("Jane", "Doe", "94043")
        assert "checkout-step-two" in logged_in_driver.current_url

        cart.finish_order()
        assert "checkout-complete" in logged_in_driver.current_url
