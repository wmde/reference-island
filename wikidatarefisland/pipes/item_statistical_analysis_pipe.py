from _collections import defaultdict

from wikidatarefisland.pipes import AbstractPipe


class ItemStatisticalAnalysisPipe(AbstractPipe):
    """Pipe to analyze and build a mapping of item qids to values given in the scraped data."""

    def __init__(self, whitelisted_external_identifiers, minimum_repetitions, maximum_noise):
        """Instantiate the pipe

        :type whitelisted_external_identifiers: list of whitelisted external identifiers
            like ['P1', 'P3', ...]
        :type minimum_repetitions: int minimum number of receptions to consider two values the same
            The higher the number, the higher precision and the lower recall will be
        """
        self.whitelisted_external_identifiers = whitelisted_external_identifiers
        self.minimum_repetitions = minimum_repetitions
        self.maximum_noise = maximum_noise
        self.statistics = defaultdict(dict)

    def flow(self, potential_match):
        """
        Observe and take notes of items passing by

        This pipe doesn't produce any match on its own
        but it only builds mapping of most used items and their values in the scraped data.
        For example if a website uses "(Germany)" as the value of nationality of a person
        and we have "Q183" as that value and it gets repeated more than N times,
        we consider these two values to be the same.

        :param potential_match: a line of output of pipe2
        """
        if potential_match['statement']['datatype'] != 'wikibase-item':
            return [potential_match]
        item_id = potential_match['statement']['value']['numeric-id']
        ext_id_property = None
        # TODO: Pass the pid in the scraper so we can use it directly here
        for pid in potential_match['reference']['referenceMetadata']:
            if pid not in self.whitelisted_external_identifiers:
                continue
            ext_id_property = pid
            break
        if not ext_id_property:
            return [potential_match]
        extracted_data = potential_match['reference']['extractedData']
        for value in extracted_data:
            value = str(value)
            if not value:
                continue
            pid = potential_match['statement']['pid']
            if pid not in self.statistics[ext_id_property]:
                self.statistics[ext_id_property][pid] = defaultdict(list)
            self.statistics[ext_id_property][pid][str(value)].append(item_id)
        return [potential_match]

    def get_mapping(self):
        """

        :return: A dictionary of mapping of ext_id_property -> pid -> "value given by the ext id"
            to numeric id of the item equivalent to it.
            For example if external identifier "P1" provides "(Germany)" for
            nationality property ("P27") and the value in Wikidata is Q183. The mapping will be:
            mapping['P1']['P27']['(Germany)'] = 183
        """
        final_result = defaultdict(dict)
        for ext_id_property in self.statistics:
            for pid in self.statistics[ext_id_property]:
                final_result[ext_id_property][pid] = self._analyze_property(ext_id_property, pid)

        return final_result

    def _analyze_property(self, ext_id_property, pid):
        per_pid_result = {}
        for value in self.statistics[ext_id_property][pid]:
            items = self.statistics[ext_id_property][pid][value]
            if len(items) > self.minimum_repetitions:
                preferred_value = self.get_preferred_item_with_noise(items)
                if preferred_value:
                    per_pid_result[value] = preferred_value

        return per_pid_result

    def get_preferred_item_with_noise(self, items):
        """
        :type items: list
        """
        # Everything is the same, bail out.
        if len(set(items)) == 1:
            return items[0]
        for case in list(set(items)):
            if (items.count(case) / len(items)) > (1 - self.maximum_noise):
                return case
        return None
