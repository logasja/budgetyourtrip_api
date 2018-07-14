import unittest
import context
from budgetyourtrip_api.api import Api
from unittest import mock

class TestAPIGeneral(unittest.TestCase):
    def setUp(self):
        self._api = Api()

    def test_get_category(self):
        category = self._api.category(1)
        self.assertEqual(category.name, "Accommodation")
        self.assertEqual(category.description, "From camping to luxury hotels, costs are for one person and assume double occupancy.")

    def test_get_categories(self):
        categories = self._api.categories()
        self.assertEqual(len(categories), 18)
        self.assertEqual(categories[15].name, 'Charitable Donations')

    def test_get_currency(self):
        currency = self._api.currency('AUD')
        self.assertEqual(currency.name, "Dollar (Australia) ")
        self.assertEqual(currency.symbol, "AU$")

    def test_get_currencies(self):
        currencies = self._api.currencies()
        self.assertIsNotNone(currencies)

    def test_get_location(self):
        location = self._api.location(4167147)
        self.assertEqual(location.name, "Orlando")
        self.assertEqual(location.currency_code, "USD")
        self.assertEqual(location.country_code, "US")

    def test_get_locations(self):
        locations = self._api.locations_search("Georgia")
        self.assertGreater(len(locations), 0)

    def test_get_country(self):
        country = self._api.country_info('US')
        self.assertIsNotNone(country)
        self.assertEqual(country.id_, "US")
        self.assertEqual(country.name, "United States of America")
        self.assertEqual(country.currency, "USD")
        self.assertGreater(len(country.costs), 0)

    def test_search_country(self):
        countries = self._api.country_search("United")
        self.assertIsNotNone(countries)
        self.assertGreater(len(countries), 0)
        self.assertGreater(len(countries[0].costs), 0)

    def test_currency_convert(self):
        usd = self._api.convert_currency(15)
        self.assertIsNotNone(usd)
        self.assertIsInstance(usd, float)

if __name__ == '__main__':
    api_test = unittest.TestLoader().loadTestsFromTestCase(TestAPIGeneral)
    unittest.TextTestRunner(verbosity=1).run(api_test)