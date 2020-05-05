from wikidatarefisland.data_model.wikibase import ValueMatchers
from wikidatarefisland.pipes import AbstractPipe


class ValueMatcherPipe(AbstractPipe):
    """A pipe segment to match potential references with statement data."""
    def __init__(self, matchers: ValueMatchers):
        """Instantiate the pipe

        Arguments:
            matchers {wikidatarefisland.data_model.ValueMatchers} --
                A static class with value matcher functions
        """
        self.matchers = matchers

    def flow(self, potential_match):
        """Applies transformations to data flow

        Arguments:
            potential_match {dict} -- A potential statement - reference match to examine.
                See: See: https://github.com/wmde/reference-island#statement-reference-blob

        Returns:
            List -- A list containing the input potential match if there's a match, empty otherwise.
        """
        filters = [
            self.matchers.match_text,
            self.matchers.match_quantity,
            self.matchers.match_geo,
            self.matchers.match_datetime
        ]

        if not any(match(potential_match) for match in filters):
            return []

        return [potential_match]
