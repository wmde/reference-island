class QuantityValue:
    """Represent Wikibase Quantity Values."""
    def __init__(self, statement):
        """Instantiates a quantity value.

        Arguments:
            statement {dict} -- A statement dictionary.
                See: https://github.com/wmde/reference-island#statement-dict
        """
        self.type = statement["datatype"]
        self.value = statement["value"]["amount"]

    def __eq__(self, other):
        if not isinstance(other, str):
            return self == other

        return self.value == other


class TextValue:
    """Represent Wikibase text Values."""
    def __init__(self, statement):
        """Instantiates a text value according to it's datatype.

        Arguments:
            statement {dict} -- A statement dictionary.
                See: https://github.com/wmde/reference-island#statement-dict
        """
        self.type = statement["datatype"]
        self.value = statement["value"]["text"] \
            if self.type == "monolingualtext" \
            else statement["value"]

    def __eq__(self, other):
        if not isinstance(other, str):
            return self == other

        return self.value.lower().strip() == other.lower().strip()
