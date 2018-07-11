"""Module containing the models used for the API.abs

The classes can be used independently of API.abs

"""

import os
from functools import wraps

import requests

def api_method(func):
    """Decorate methods needing access to api

    Thid decorator ensures that methods that need to make a call to the
    api are only run if access to the api is available.
    If access to it is not available, ''NotImplementedError'' will be raised.
    """
    @wraps(func)
    def api_call(*args, **kwargs):
        if args[0]._api:
            return func(*args, **kwargs)
        else:
            raise NotImplementedError
    return api_call

# Base class
class ApiObject(object):
    def __init__(self):
        pass

    def _build(self, model_json):
        """Assemble an object from a JSON representation.

        Uses ``self.attrs`` to pull values from ``model_json`` and create object attributes.

        Args:
            model_json: JSON representation of an API resource.

        Raises:
            KeyError: if the key from ``self.attrs`` is not a key in ``model_json``

        """
        for key, value in self.attrs.items():
            try:
                # TODO use setattr(self, key, value) instead?
                self.__dict__.update({key: ApiObject._get_from_dict(model_json, value)})
            except KeyError:
                self.__dict__.update({key: None})
        
    @staticmethod
    def _get_from_dict(data_dict, map_list):
        """Retrieve the value corresponding to ``map_list`` in ``data_dict``.

        If ``map_list`` is a string, it is used directly as a key of ``data_dict``.
        If ``map_list`` is a list or tuple, each item in it is used recusively as a key.

        Args:
            data_dict (dict): The dictionary to retrieve value from.
            map_list (list, tuple or str): The key(s) to use in data_dict.

        Returns:
            The value corresponding to the given key(s).

        """
        if isinstance(map_list, (list, tuple)):
            for k in map_list:
                data_dict = data_dict[k]
        else:
            data_dict = data_dict[map_list]
        return data_dict

    def __eq__(self, other):
        """Define equality of two API objects as having the same type and attributes."""
        return (type(self) == type(other) and
                dict((k, self.__dict__[k]) for k in self.attrs.keys()) ==
                dict((k, other.__dict__[k]) for k in other.attrs.keys()))

    def __repr__(self):
        """Nicer printing of API objects."""
        return str(dict((k, self.__dict__[k]) for k in self.attrs.keys()))


# Travel costs categories
class Category(ApiObject):
    """Class representing a Category.

    Attributes:
        id_ (int):          Unique Identifier of the category.
        name (str):         The name of the category.
        description (str):  Description of the category.
    """

    def __init__(self, category_json, api=None):
        """Take in a JSON representation of a category and convert it into Categories Object.

        Args:
            category_json (json):       JSON representation of a category resource.
            api (object, optional):     Object that implements the API
                                        (see :class:`~budgetyourtrip_api.api.budgetyourtrip_api`).
                                        This will be used to make calls to the API when needed.
        """
        super(Category, self).__init__()
        self._api = api
        self.attrs = {
            "id_"           : "category_id",
            "name"          : "name",
            "description"   : "description"
        }
        self._build(category_json)

class Country(ApiObject):
    """ Class representing a Country.

    Attributes:
        id_ (str):          Unique country code identifier.
        name (str):         Name of the country.
        currency (str):     Currency code.
        negotiate (int):    The usual amount for which tourists need to negotiate for prices.
        canonical_url (str):URL on the budgetyourtrip website.
        costs (list):       All of the :class:`Costs <Cost>` of the country.
    """

    def __init__(self, country_json, api=None):
        """Take in a JSON representation of a country and make a Country Object.

        Args:
            country_json (json):        JSON representation of a show resource.
            api (object, optional):     Object that implements the API.
                                        (see :class:`~budgetyourtrip_api.budgetyourtrip_api`).
                                        This will be used to make calls to API when needed.
        """
        super(Country, self).__init__()
        self._api = api
        self.attrs = {
            "id_"           : "country_code",
            "name"          : "name",
            "canonical_url" : "url",
            "negotiate"     : "negotiate",
            "currency"      : "currency_code"
        }
        if country_json['info']:
            self.costs = []
            self._build(country_json['info'])
            for cost_json in country_json['costs']:
                self.costs.append(Cost(cost_json))
        else:
            self.costs = None
            self._build(country_json)


class Cost(ApiObject):
    """ Class representing a cost.

    Attributes:
        id_ (int):              Unique cost identifier.
        budget (float):         The cost for budget travel.
        midrange (float):       The cost for midrange travel.
        luxury (float):         The cost for luxury travel.
        country_code (str):     Unique country code identifier.
    """

    def __init__(self, cost_json, api=None):
        """Take in a JSON representation of a cost and make a Cost Object.

        Args:
            cost_json (json):           JSON representation of a show resource.
            api (object, optional):     Object that implements the API.
                                        (see :class:`~budgetyourtrip_api.budgetyourtrip_api`).
                                        This will be used to make calls to the API when needed.
        """
        super(Cost, self).__init__()
        self._api = api
        self.attrs = {
            "id_"           : "category_id",
            "budget"        : "value_budget",
            "midrange"      : "value_midrange",
            "luxury"        : "value_luxury",
            "country_id"    : "country_code"
        }
        self._build(cost_json)


class Currency(ApiObject):
    """ Class representing a currency.

    Attributes:
        id_ (str):              Currency code.
        name (str):             Currency name.
        symbol (str):           Currency symbol.
    """
    def __init__(self, currency_json, api=None):
        """take in a JSON representation of a currency and make a Currency object.

        Args:
            currency_json (json):       JSON representation of a currency.
            api (object, optional):     Object that implements the API
                                        (see :class:`~budgetyourtrip_api.budgetyourtrip_api`).
                                        This will be used to make calls to the API when needed.
        """
        super(Currency, self).__init__()
        self._api = api
        self.attrs = {
            "id_"           : "currency_code",
            "name"          : "currency",
            "symbol"        : "symbol"
        }
        self._build(currency_json)


class Location(ApiObject):
    """ Class representing a location.

    Attributes:
        id_ (int):              Geoname ID.
        name (str):             Location name.
        latitute (float):       Latitude.
        longitude (float):      Longitude.
        feature_class (str):    
        feature_code (str):     
        country_code (str):     
        country_name (str):     
        admin1_code (str):      
        negotiate (int):        How much the traveler needs to negotiate for prices.
        currency_code (str):    Currency code of location.
        currency (str):         Full currency string.
    """

    def __init__(self, location_json, api=None):
        """Take in a JSON representation of a cost and make a Cost Object.

        Args:
            location_json (json):       JSON representation of a show resource.
            api (object, optional):     Object that implements the API.
                                        (see :class:`~budgetyourtrip_api.budgetyourtrip_api`).
                                        This will be used to make calls to the API when needed.
        """
        super(Location, self).__init__()
        self._api = api
        self.attrs = {
            "id_"           : "geonameid",
            "name"          : "name",
            "latitude"      : "latitude",
            "longitude"     : "longitude",
            "feature_class" : "feature_class",
            "feature_code"  : "feature_code",
            "country_code"  : "country_code",
            "country_name"  : "country_name",
            "admin1_code"   : "admin1_code",
            "negotiate"     : "negotiate",
            "currency_code" : "currency_code",
            "currency"      : "currency"
        }
        self._build(location_json)