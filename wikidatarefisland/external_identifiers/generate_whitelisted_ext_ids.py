import concurrent.futures

import requests


class GenerateWhitelistedExtIds():

    def __init__(self, wdqs_reader, storage, config, external_identifier_to_url_mapper,
                 no_checks=10, no_processes=10):
        """
        Implementation of Side-step 1

        :type wdqs_reader: wikidatarefisland.data_access.WdqsReader
        :type storage: wikidatarefisland.data_access.Storage
        :type config: wikidatarefisland.Config
        :type external_identifier_to_url_mapper:
            wikidatarefisland.data_access.ExternalIdentifierToUrlMapper
        """
        self.wdqs_reader = wdqs_reader
        self.storage = storage
        self.config = config
        self.no_checks = no_checks
        self.no_processes = no_processes
        self.external_identifier_to_url_mapper = external_identifier_to_url_mapper
        self.result_file_name = 'ext_ids_check_result.json'

    def check_cases(self, usecases, formatter_urls_for_id):
        total_number = 0
        good_responses = 0
        schema_org_responses = 0
        for case in usecases:
            total_number += 1
            value = case['value']['value']
            url = formatter_urls_for_id[0].replace('$1', value)
            try:
                r = requests.get(url, timeout=30)
            except KeyboardInterrupt:
                raise
            except:  # noqa: E722
                continue
            if r.status_code == 200:
                good_responses += 1

            # TODO: Proper check
            if 'http://schema.org' in r.text:
                schema_org_responses += 1
        return total_number, good_responses, schema_org_responses

    def check_external_identifier(self, pid, formatter_url):
        print('Checking {0}'.format(pid))
        usecases = self.wdqs_reader.get_usecases(pid, self.no_checks)
        return self.check_cases(usecases, formatter_url)

    def run(self):
        external_identifiers = self.wdqs_reader.get_all_external_identifiers()
        try:
            final_results = self.storage.get(self.result_file_name)
        except FileNotFoundError:
            final_results = {}

        pids = {}
        for i in external_identifiers:
            if i in final_results or i in self.config.get('blacklisted_properties'):
                continue
            formatter_url = self.external_identifier_to_url_mapper.get_formatter(i)
            if not formatter_url:
                print('{0} does not have a formatter'.format(i))
                continue
            pids[i] = formatter_url

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.no_processes) as executor:
            future_to_pid = {
                executor.submit(self.check_external_identifier, i, pids[i]): i for i in pids}
            for future in concurrent.futures.as_completed(future_to_pid):
                pid = future_to_pid[future]
                try:
                    data = future.result()
                except Exception as exc:
                    print('%r generated an exception: %s' % (pid, exc))
                    continue
                final_results[pid] = data
                self.storage.store(self.result_file_name, final_results)

        data = self.storage.get(self.result_file_name)
        schemas = []
        for i in data:
            if data[i][2] > int(self.no_checks / 2):
                schemas.append(i)

        return schemas
