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
        sumtype (int):      Type of sum done on this category.
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
        self.attr = {
            "id_"           : "category_id",
            "name"          : "name",
            "description"   : "description",
            "sumtype"       : "sumtype"
        }
        self._build(category_json)

class Country(ApiObject):
    """ Class representing a Country.

    Attributes:
        