from functools import reduce
from pyld import jsonld


class SchemaOrgNormalizer:

    @staticmethod
    def filterProps(prop_key):
        return "schema.org" in prop_key

    @staticmethod
    def filterScraped(scraped):
        filtered_keys = list(filter(SchemaOrgNormalizer.filterProps, scraped.keys()))
        return filtered_keys

    @staticmethod
    def normalizeMultipleExpanded(*args):
        # PROBLEM: This method inadvertently chucks away values hidden in @graph
        scrapedList = reduce(lambda acc, arg: acc + arg, args)
        filtered = list(filter(SchemaOrgNormalizer.filterScraped, scrapedList))
        return jsonld.flatten(filtered)
