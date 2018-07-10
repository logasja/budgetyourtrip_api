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
        self.assertEqual(category.sumtype, '1')

    def test_get_categories(self):
        categories = self._api.categories()
        self.assertEqual(len(categories), 18)
        self.assertEqual(categories[15].name, 'Charitable Donations')

    

if __name__ == '__main__':
    api_test = unittest.TestLoader().loadTestsFromTestCase(TestAPIGeneral)
    unittest.TextTestRunner(verbosity=1).run(api_test)