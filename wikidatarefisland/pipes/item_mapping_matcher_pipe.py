from wikidatarefisland.pipes import AbstractPipe


class ItemMappingMatcherPipe(AbstractPipe):
    """Pipe to match potential references with statement data on item values using a mapping."""

    def __init__(self, mapping, allowed_external_identifiers):
        """
        :type mapping: dict See ItemStatisticalAnalysisPipe.get_mapping()
        :type allowed_external_identifiers: list of allowed external identifiers
            like ['P1', 'P3', ...]
        """
        self.mapping = mapping
        self.allowed_external_identifiers = allowed_external_identifiers

    def flow(self, potential_match):
        """Apply transformations to data flow

        Arguments:
            potential_match {dict} -- A potential statement - reference match to examine.
                See: See: https://github.com/wmde/reference-island#statement-reference-blob

        Returns:
            List -- A list containing the input potential match if there's a match, empty otherwise.
        """
        if potential_match['statement']['datatype'] != 'wikibase-item':
            return []
        item_id = potential_match['statement']['value']['numeric-id']
        ext_id_property = None
        for pid in potential_match['reference']['referenceMetadata']:
            if pid not in self.allowed_external_identifiers:
                continue
            ext_id_property = pid
            break
        if not ext_id_property:
            return []
        extracted_data = potential_match['reference']['extractedData']
        for value in extracted_data:
            value = str(value)
            if not value:
                continue
            pid = potential_match['statement']['pid']
            if pid not in self.mapping[ext_id_property]:
                return []
            if item_id == self.mapping[ext_id_property][pid].get(str(value)):
                return [potential_match]
        return []
