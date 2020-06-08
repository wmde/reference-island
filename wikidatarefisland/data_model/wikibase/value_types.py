from dateutil.parser import isoparse


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
            return self == str(other)

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
            return self == str(other)

        return self.value.lower().strip() == other.lower().strip()


class DateTimeValue:
    """Represent Wikibase date and time values."""
    def __init__(self, statement):
        """Instantiates a datetime.

        Arguments:
            statement {dict} -- A statement dictionary.
                See: https://github.com/wmde/reference-island#statement-dict
        """
        self.type = statement["datatype"]
        self.sign = statement["value"]["time"][0]
        self.value = statement["value"]["time"][1:]
        self.precision = int(statement["value"]["precision"])

    def __eq__(self, other):
        if not isinstance(other, str):
            return self == str(other)

        has_sign = other.startswith(('+', '-'))
        compare_sign = other[0] if has_sign else '+'
        compare_string = other[1:] if has_sign else other

        try:
            compare = isoparse(compare_string)
        except ValueError:
            return False

        if self.sign != compare_sign:
            return False

        # 9 - Year Precision
        if self.precision == 9:
            date = isoparse(self.value[:4])
            return date.year == compare.year

        try:
            date = isoparse(self.value)
        except ValueError:
            # Some Wikibase dates are not valid: https://phabricator.wikimedia.org/T85296
            return False
        return date.year == compare.year \
            and date.month == compare.month \
            and date.day == compare.day


class GeoValue:
    """Represent Wikibase geogaraphical values"""
    def __init__(self, statement):
        """Instantiates a geo value according to it's datatype

        Arguments:
            statement {dict} -- A statement dict.
                See: https://github.com/wmde/reference-island#statement-dict
        """
        self.type = statement["datatype"]
        self.value = statement["value"]

    def __eq__(self, other):
        if isinstance(other, dict):
            # TODO: Make it schema.org-agnostic
            if 'http://schema.org/latitude' in other:
                other['latitude'] = other['http://schema.org/latitude'][0]
            if 'http://schema.org/longitude' in other:
                other['longitude'] = other['http://schema.org/longitude'][0]
        if(self.type != 'globe-coordinate'
           or 'latitude' not in other
           or 'longitude' not in other):
            return self.value == other

        return (self.value["latitude"] == float(other["latitude"])
                and self.value["longitude"] == float(other["longitude"]))
