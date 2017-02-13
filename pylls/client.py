#
#    Cachet API python client (python-pylls)
#
#    Copyright (C) 2017 Denis Pompilio (jawa) <denis.pompilio@gmail.com>
#
#    This file is part of python-pylls
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, see <http://www.gnu.org/licenses/>.

import json
import requests
import logging
from functools import partial


logger = logging.getLogger(__name__)


class CachetAPIClient(object):
    """Simple Cachet API client

    It implements common HTTP methods GET, POST, PUT and DELETE

    This client is using :mod:`requests` package. Please see
    http://docs.python-requests.org/ for more information.

    :param bool verify: Control SSL certificate validation
    :param int timeout: Request timeout in seconds
    :param str api_endpoint: Cachet API endpoint
    :param str api_token: Cachet API token
    """
    def __init__(self, api_endpoint, api_token=None, verify=None, timeout=None):
        """Initialization method"""
        self.verify = verify
        self.timeout = timeout

        self.api_endpoint = api_endpoint
        self.api_token = api_token

        self.request_headers = {
            'User-Agent': 'python-pylls',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        self.r_session = requests.Session()

        # Directly expose common HTTP methods
        self.get = partial(self.request, method='GET')
        self.post = partial(self.request, method='POST')
        self.put = partial(self.request, method='PUT')
        self.delete = partial(self.request, method='DELETE')

    def request(self, path, method, data=None, **kwargs):
        """Handle reauests to API

        :param str path: API endpoint's path to request
        :param str method: HTTP method to use
        :param obj data: Data to send (optional)

        Additional named argument may be passed and are directly transmitted
        to Session.request() call.

        :return: Parsed json response as :class:`dict`
        """
        if self.api_token:
            self.request_headers['X-Cachet-Token'] = self.api_token

        if not path.startswith('http://') and not path.startswith('https://'):
            url = "%s/%s" % (self.api_endpoint, path)
        else:
            url = path

        response = self.r_session.request(method, url,
                                          data=json.dumps(data),
                                          headers=self.request_headers,
                                          timeout=self.timeout,
                                          verify=self.verify,
                                          **kwargs)

        # If API returns an error, we simply raise and let caller handle it
        response.raise_for_status()

        return response.json()

    def paginate_request(self, path, method, data=None, **kwargs):
        """Handle Cachet request pagination

        :param str path: API endpoint's path to request
        :param str method: HTTP method to use
        :param obj data: Data to send (optional)

        Cachet pagination is handled and next pages requested on demand.

        Additional named argument may be passed and are directly transmitted
        to Session.request() call.

        :return: Response data items (:class:`Generator`)
        """
        next_page = path
        while next_page:
            response = self.request(next_page, method, data=data, **kwargs)

            if not isinstance(response.get('data'), list):
                next_page = None
                yield response['data']
            else:
                for entry in response['data']:
                    yield entry

                # Get next page if it exists
                try:
                    links = response['meta']['pagination']['links']
                    next_page = links.get('next_page')
                    print(links)
                except KeyError:
                    next_page = None


class CachetAPIEndPoint(object):
    """Cachet API endpoint

    :param CachetAPIClient api_client: Cachet API client object
    """
    def __init__(self, api_client):
        """Initialization method"""
        self.api_client = api_client
        self._get = api_client.get
        self._post = api_client.post
        self._put = api_client.put
        self._delete = api_client.delete
        self.paginate_get = partial(api_client.paginate_request, method='GET')

    def get(self, *args, **kwargs):
        """Unimplemented get method"""
        raise NotImplementedError("Operation not implemented")

    def create(self, *args, **kwargs):
        """Unimplemented create method"""
        raise NotImplementedError("Operation not implemented")

    def update(self, *args, **kwargs):
        """Unimplemented update method"""
        raise NotImplementedError("Operation not implemented")

    def delete(self, *args, **kwargs):
        """Unimplemented delete method"""
        raise NotImplementedError("Operation not implemented")
