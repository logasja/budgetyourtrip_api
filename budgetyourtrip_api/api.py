"""Module containing the interface to the API.

Currently access:
    Category

"""

import posixpath
from functools import wraps

from cache_requests import Session
import requests
from budgetyourtrip_api import models, config

class Api(object):
    """Main class of the API.

    Create an instance of this to access the api.

    """

    def __init__(self, key = config.API_KEY):
        """Create an api object.

        Args:
            api_key (str, optional): api key to use.
                If one is not supplied, a default one will be generated and used.

        """
        self.__session = Session()
        self.__session.headers['X-API-KEY'] = key

    def __get_data(self, url, params=None):
        """Get the data at the given URL, using supplied parameters.

        Args:
            url (str):                  The URL to retrieve data from.
            params (dict, optional):    Key-value pairs to include when making the request.

        Returns:
            json:                       The JSON response.

        """
        response = self.__session.get(url, params=params)
        # Check status code
        if response.status_code == 401:
            response.raise_for_status()
        elif response.status_code == 404:
            # Api item doesn't exist
            return None
        elif response.status_code != requests.codes.ok:
            response.raise_for_status()
        try:
            return response.json()['data']
        except ValueError:
            # Parsing json response failed
            pass

    def __build_response(self, path, model_class):
        """Retrieve data from given path and load it into an object of given model class.

        Args:
            path (str):             Path of API to send request to.
            model_class (type):     The type of object to build using the response from the API.

        Returns:
            object:                 Instance of the specified model class.

        """
        data = self.__get_data(posixpath.join(config.END_POINT, path))
        if not data:
            return None
        return model_class(data, self)

    def __get_multiple(self, path, model_class):
        """Retrieve from API endpoint that returns a list of items.

        Args:
            model (type):   The type of object to build using the response from the API.
            path (str):     The path of API to send request to.

        Returns:
            list:           A list containing items of type model_class.

        """
        url = posixpath.join(config.END_POINT, path)
        data = self.__get_data(url)
        if not data:
            return None
        items = []
        for json_item in data:
            item = model_class(json_item, self)
            items.append(item)
        return items

    def category(self, id):
        """Get a category by id.

        Args:
            id (int):       Unique identifier of a category.

        Returns:
            object:         Category object with all fields.

        """
        return self.__build_response('categories/{0}'.format(id), models.Category)

    def categories(self):
        """Get a list of categories by id.

        Returns:
            list:           List of categories objects.
        """
        return self.__get_multiple('categories/', models.Category)

    def currency(self, currency_code):
        """Get a currency object by code.

        Returns:
            object:         Currency object.
        """
        return self.__build_response('currencies/{0}'.format(currency_code), models.Currency)

    def currencies(self):
        """Get a list of available currencies.

        Returns:
            list:           List of currency objects.
        """
        return self.__get_multiple('currencies/', models.Currency)

    def location(self, geonameid):
        """Get a location by geonameid.

        Returns:
            object:         Location object.
        """
        return self.__build_response('costs/locationinfo/{0}'.format(geonameid), models.Location)

    def locations_search(self, search_term):
        """Get a list of matching locations by search term.

        Returns:
            list:           List of location objects matching search term.
        """
        return self.__get_multiple('search/location/{0}'.format(search_term), models.Location)

    def country_info(self, country_code):
        """Get a country object with cost info by country code.

        Returns:
            object:         Country object.
        """
        return self.__build_response('costs/countryinfo/{0}'.format(country_code), models.Country)

    def country_search(self, search_term):
        """Get a list of countries that match the search term.

        Returns:
            list:           List of Countries.
        """
        return self.__get_multiple('search/country/{0}'.format(search_term), models.Country)

    def country_costs(self, country_code):
        """Get a list of the costs associated with a country.

        Returns:
            list:           List of Costs.
        """
        return self.__get_multiple('costs/country/{0}'.format(country_code), models.Cost)

    def location_costs(self, geonameid):
        """Get a list of costs associated with a location.

        Returns:
            list:           List of Costs.
        """
        return self.__get_multiple('costs/location/{0}'.format(geonameid), models.Cost)

    def convert_currency(self, amount, from_cur='usd', to_cur='eur'):
        """Convert the given amount from one currency to the other.

        Returns:
            float:          The monetary value of the amount given.
        """
        data = self.__get_data(posixpath.join(config.END_POINT, 
                               'currencies/convert/{0}/{1}/{2}'.format(from_cur, to_cur, amount)))
        if not data:
            return None
        return data['newAmount']
