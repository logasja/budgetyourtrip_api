"""Module containing the interface to the API.

Currently access:
    Category

"""

import posixpath
from functools import wraps

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
        self.__session = requests.Session()
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
            json_data = response.json()
            # print(json_data)
            return json_data['data']
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

    def category(self, id):
        """Get a category by id.

        Args:
            id (int):       Unique identifier of a category.

        Returns:
            object:         Category object with all fields.

        """
        return self.__build_response('categories/{0}'.format(id), models.Category)