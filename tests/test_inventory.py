import pytest
from pages.inventory_page import InventoryPage


class TestInventory:
    def test_inventory_displays_six_products(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        assert inventory.get_item_count() == 6

    def test_inventory_page_title_is_products(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        assert inventory.get_page_title() == "Products"

    def test_sort_az_orders_names_ascending(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.sort_by("az")
        names = inventory.get_item_names()
        assert names == sorted(names)

    def test_sort_za_orders_names_descending(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.sort_by("za")
        names = inventory.get_item_names()
        assert names == sorted(names, reverse=True)

    def test_sort_lohi_orders_prices_ascending(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.sort_by("lohi")
        prices = inventory.get_item_prices()
        assert prices == sorted(prices)

    def test_sort_hilo_orders_prices_descending(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.sort_by("hilo")
        prices = inventory.get_item_prices()
        assert prices == sorted(prices, reverse=True)

    def test_add_single_item_updates_cart_badge(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_item_to_cart("Sauce Labs Backpack")
        assert inventory.get_cart_badge_count() == 1

    def test_add_multiple_items_updates_cart_badge(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_item_to_cart("Sauce Labs Backpack")
        inventory.add_item_to_cart("Sauce Labs Bike Light")
        assert inventory.get_cart_badge_count() == 2

    def test_remove_item_decrements_cart_badge(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_item_to_cart("Sauce Labs Backpack")
        inventory.add_item_to_cart("Sauce Labs Bike Light")
        inventory.remove_item_from_cart("Sauce Labs Backpack")
        assert inventory.get_cart_badge_count() == 1

    def test_no_cart_badge_when_cart_empty(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        assert inventory.get_cart_badge_count() == 0
