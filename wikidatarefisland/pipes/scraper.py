import concurrent.futures
from time import gmtime, strftime

import extruct
import requests
from w3lib.html import get_base_url

from .abstract_pipe import AbstractPipe


class ScraperPipe(AbstractPipe):
    def __init__(self, config, schemaorg_normalizer, schemaorg_mapper):
        """

        :type config: wikidatarefisland.Config
        :type schemaorg_mapper: wikidatarefisland.services.SchemaorgPropertyMapper
        """
        self.config = config
        self.schemaorg_normalizer = schemaorg_normalizer
        self.schemaorg_mapper = schemaorg_mapper

    def flow(self, item):
        resource_urls = {i['url']: i['referenceMetadata'] for i in item['resourceUrls']}
        schemaorg_mapping = {
            i['url']: i['property'] for i in self.schemaorg_mapper.get_mapping()}
        statement_pids = [i['pid'] for i in item['statements']]
        properties_to_check = filter(lambda t: t in schemaorg_mapping.values(), statement_pids)
        if not properties_to_check:
            # Bail out if we can't find any property that have schema.org equivalent
            return

        extracted_data = {}
        workers = int(self.config.get('parallel_workers'))
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
            future_to_url = {
                executor.submit(self._check_external_identifier, i): i for i in resource_urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except KeyboardInterrupt:
                raise
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
            else:
                extracted_data[url] = data

        return self._match_extracted_data(extracted_data, resource_urls,
                                          schemaorg_mapping, item)

    def _check_external_identifier(self, url):
        session = requests.Session()
        session.headers.update({'User-Agent': self.config.get('user_agent')})
        r = session.get(url, timeout=30)
        base_url = get_base_url(r.text, r.url)
        data = extruct.extract(r.text, base_url=base_url, uniform=True)
        return {'data': self.schemaorg_normalizer.normalize_from_extruct(data),
                'timestamp': strftime("%Y-%m-%d %H:%M:%S", gmtime())}

    def _match_extracted_data(self, extracted_data, resourceUrls, mapping, item):
        final_data = []
        for url in extracted_data:
            final_data += self._get_data_per_url(url, extracted_data[url],
                                                 resourceUrls, mapping, item)
        return final_data

    def _get_data_per_url(self, url, data, resourceUrls, mapping, item):
        final_data = []
        resourceUrls[url]['dateRetrieved'] = data['timestamp']
        for datum in data['data']:
            for schema_property in datum:
                if schema_property not in mapping:
                    continue
                pid = mapping[schema_property]
                for statement in item['statements']:
                    if statement['pid'] != pid:
                        continue

                    formatted = self._format_result(
                        statement,
                        item['itemId'],
                        resourceUrls[url],
                        datum[schema_property])
                    final_data.append(formatted)
        return final_data

    def _format_result(self, statement, item_id, metadata, extracted_data):
        return {
            'statement': statement,
            'itemId': item_id,
            'reference': {
                'referenceMetadata': metadata,
                'extractedData': extracted_data
            }
        }
