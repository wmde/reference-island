try:
    from simplejson import JSONDecodeError
except ImportError:
    from json import JSONDecodeError
import requests


class SchemaContextDownloader:
    @staticmethod
    def download(useragent):
        headers = {
            'Accept': 'application/ld+json, application/json',
            'user-agent': useragent
        }
        try:
            result = requests.get('https://schema.org/', headers=headers)
            context = result.json()
        except JSONDecodeError:
            context = requests.get(
                'https://schema.org/docs/jsonldcontext.jsonld',
                headers=headers
                ).json()
        return context
