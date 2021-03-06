import json
import logging
import requests

logger = logging.getLogger(__name__)


class ConnectorException(Exception):
    def __init__(self, message, description, code, entity=None):
        self.code = code
        self.message = message
        self.description = description
        self.entity = entity
        super().__init__(message)


class Connector:

    def __init__(self, headers=None, verify_ssl=True):
        self.headers = headers
        self.verify_ssl = verify_ssl

    def _handle_response(self, response, object_name, url):
        if response.status_code == 400:
            raise ConnectorException(response.content, response.text, 400)
        if response.status_code == 422:
            raise ConnectorException(f'Error:  {response.json()}', response.text, 422)
        if response.status_code == 401:
            raise ConnectorException(f'Unauthorized operation over {object_name}', response.text, 401)
        if response.status_code == 404:
            raise ConnectorException(f'Not found error trying to access to {url}', response.text, 404)
        if response.status_code not in [200, 201]:
            raise ConnectorException(f'Fail operation to {url}', response.text, response.status_code,)
        if isinstance(response.json, dict):
            return response.json
        return json.loads(response.content)

    def get(self, url, object_name='this objects'):
        logger.debug('Getting url %s' % (url))
        if self.headers:
            response = requests.get(url, headers=self.headers, verify=self.verify_ssl)
        else:
            response = requests.get(url)
        return self._handle_response(response, object_name, url)

    def post(self, url, data, object_name='this objects'):
        logger.debug('Creating %s to %s' % (object_name, url))
        if self.headers:
            response = requests.post(url, json=data, headers=self.headers, verify=self.verify_ssl)
        else:
            response = requests.post(url, json=data, verify=self.verify_ssl)
        return self._handle_response(response, object_name, url)

    def put(self, url, data, object_name):
        logger.debug('Updating %s to %s' % (object_name, url))
        if self.headers:
            response = requests.put(url, json=data, headers=self.headers, verify=self.verify_ssl)
        else:
            response = requests.put(url, json=data, verify=self.verify_ssl)
        return self._handle_response(response, object_name, url)

    def delete(self, url, object_name):
        logger.debug('Deleting %s from %s' % (object_name, url))
        if self.headers:
            response = requests.delete(url, headers=self.headers, verify=self.verify_ssl)
        else:
            response = requests.delete(url, verify=self.verify_ssl)
        return self._handle_response(response, object_name, url)
