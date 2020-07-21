# Data Pipeline Reference

The following document aims to describe the flow of data in the Reference Island pipeline, as well as provide relevant code touch points and concepts covered in this code base.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Glossary](#glossary)
- [Data Pumps](#data-pumps)
  - [Dump Reader Pump](#dump-reader-pump)
  - [Simple Pump](#simple-pump)
  - [Observer Pump](#observer-pump)
- [Pipeline Segments](#pipeline-segments)
  - [Pipe 1: Item Extractor](#pipe-1-item-extractor)
  - [Pipe 2: Scraper](#pipe-2-scraper)
  - [Pipe 3: Value Matcher](#pipe-3-value-matcher)
  - [Pipe 4: Statistical Matcher](#pipe-4-statistical-matcher)
- [Side Services](#side-services)
  - [SS 1: External Resource Checker](#ss-1-external-resource-checker)
  - [SS 2: Schema.org JSON-LD context fetcher](#ss-2-schemaorg-json-ld-context-fetcher)
- [Noteworthy Utility Classes](#noteworthy-utility-classes)
  - [Wikidata External Id URL Formatter](#wikidata-external-id-url-formatter)
  - [Schema.org Data Normalizer](#schemaorg-data-normalizer)
  - [Wikidata - Schema.org Property Mapper](#wikidata---schemaorg-property-mapper)
  - [Wikibase Value Matchers](#wikibase-value-matchers)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Glossary

The following terms will be used throughout this document, their meanings are as follows:

**Pump**: Represents a class that "flows" data into a pipeline segment, and is responsible for reading and writing the results of each segment to and from the disk.

**Pipe #:** Represents a sequential segment in the main data pipeline, which processes Wikidata item serializations into a formatted list of potential references. 

**SS #:** Represents a "side service", to provide additional data to segments in the main pipeline, which will aid in making decisions or filter and format potential references.

## Data Pumps

### Dump Reader Pump

[[Code]](../wikidatarefisland/pumps/pump.py#L25-L49)

The dump reader pump is designed to read Wikidata dumps in various formats (`json`, `gz`, `bz`). It flows each Wikidata Item into a passed pipe class and writes the results into a specified file in `jsonl` format.  

### Simple Pump

[[Code]](../wikidatarefisland/pumps/pump.py#L14-L22)

The simple pump is designed to read `jsonl` files, and flow each line into a passed pipe class. It then writes the results of the pipe into a specified file in `jsonl` format.

### Observer Pump

[[Code]](../wikidatarefisland/pumps/pump.py#L52-L59)

The observer pump is designed as a read only pipeline. It reads files in `jsonl` format and flows each line into a specified pipe class.

## Pipeline Segments

### Pipe 1: Item Extractor

[[Code]](../wikidatarefisland/pipes/item_extractor_pipe.py), [[Makefile Command]](../Makefile#L9-L11): `make data/extracted_unreferenced_statements.jsonl`

This pipe segment is designed to filter out and formats Wikibase Items according to specified criteria. In order to pass this pipe segment, the Item must:

* Not be an instance of a [***ignored class***](../config/default.yml#L1-L9).
* Have at least one [***unreferenced***](../config/default.yml#L108-L110) statement of a [***non skipped property***](../config/default.yml#L11-L76).
* Have at least one External Id linking to a ***allowed*** external resource (see: [SS 1: External Resource Checker](#ss-1-external-resource-checker)).

It takes in a de-serialized [Wikibase Item](https://gerrit.wikimedia.org/r/plugins/gitiles/mediawiki/extensions/Wikibase/+/master/docs/topics/json.md#json) dump as an input and returns an array with a single [`ItemLine`](result.md#itemline) or an empty array if the item does not match the criteria.

### Pipe 2: Scraper

[[Code]](../wikidatarefisland/pipes/scraper.py), [[Makefile Command]](../Makefile#L14-L17): `make data/scraped_data.jsonl`

The scraper pipe makes calls to external resource URLs to retrieve Schema.org data in various formats (microdata, json-ld, rdfa). It [normalizes](#schemaorg-data-normalizer) this data and pairs statements with potential extracted data matches according to a Schema.org <-> Wikidata [mapping](#wikidata---schemaorg-property-mapper) maintained on Wikidata by the community.

This pipe takes in a single [`ItemLine`](result.md#itemline) and returns an array with 0 or more [`MatchLine`](result.md#matchline)s, depending whether any potential matches were found.

### Pipe 3: Value Matcher

[[Code]](../wikidatarefisland/pipes/value_matcher_pipe.py), [[Makefile Command]](../Makefile#L18-L20): `make data/matched_references.jsonl`

The value matcher pipe tries to make [exact matches](#wikibase-value-matchers) between the statement data and the extracted data for that statement.

This pipe takes in a single [`MatchLine`](result.md#matchline), and returns an array with that line if a match exists or an empty array if it did not find a match.

### Pipe 4: Statistical Matcher

[[Code: Statistical Analysis]](../wikidatarefisland/pipes/item_statistical_analysis_pipe.py), [[Code: Item Matching]](../wikidatarefisland/pipes/item_mapping_matcher_pipe.py), [[Makefile Command]](../Makefile#L21-L23): `make data/matched_item_references.jsonl`

This pipeline segment consists of two pipe steps in order to match extracted data and statement values that refer to a Wikibase Item: 

- The first step reads and updates an internal statistic record about the frequency of matches between a piece of extracted data and a Wikibase QID utilizing settings for a [minimum frequency](../config/default.yml#L128-L129) and maximum amount of [allowed noise](../config/default.yml#L131-L132).
-  The second step of this segment relies on the data gathered above to match Wikibase Items to their ***probable matches***.

This segment iterates over the data dump twice, where each pipe takes in a single [`MatchLine`](result.md#matchline), and returns an array with that line if a match exists, or an empty array if it doesn't.

## Side Services

### SS 1: External Resource Checker

[[Code]](../wikidatarefisland/external_identifiers/generate_allowed_ext_ids.py), [[Makefile Command]](../Makefile#L7-L8): `make data/allowed_ext_idefs.json`

This service produces a list of External Identifier resource which are viable candidates for data extraction. It test-scrapes a sample of 10 use cases from each non [***ignored external identifier***](../config/default.yml#L78-L106), obtained through the [Wikidata Query Service](https://query.wikidata.org/), to determine whether the resource of that identifier contains enough viable data to scrape. It then collects all identifiers representing viable resources and writes their Wikibase Property IDs to a JSON array.

###  SS 2: Schema.org JSON-LD context fetcher

[[Code]](../wikidatarefisland/data_access/schema_context_downloader.py), [[Makefile Command]](../Makefile#L12-L13): `make data/schema_org_context.jsonld`

This service downloads the Schema.org JSON-LD context to prevent multiple calls to http://schema.org during scraping.

Until 2020-05-19 it was possible for PyLD to automatically obtain it through content-negotiation of schema.org but this broke. To mitigate this, the side-stream has a backup method to get the context from the schema.org docs.

## Noteworthy Utility Classes

### Wikidata External Id URL Formatter

[[Code]](../wikidatarefisland/services/external_identifier_formatter.py)

This service takes in a string representation of an external id property and attempts to output a formatted URL for an external resource utilizing the [Wikidata Query Service](https://query.wikidata.org/). In addition, the URL Formatter generates a reference metadata object according to the retrieved formatted URL. See [`ResourceBlob`](result.md#resourceblob) for the output, if no formatter is found the service returns `false`.

### Schema.org Data Normalizer

[[Code]](../wikidatarefisland/data_model/schemaorg_normalizer.py)

This service takes in an object containing raw scraped data in `json-ld` format (For example, the results of the following scraping library: https://github.com/scrapinghub/extruct with the [`uniform` option set to true](https://github.com/scrapinghub/extruct#uniform)).

The output of this service will be a list of objects representing a Schema.org type with the following structure: 

```js
[
    {
        "http://schema.org/name": [ "Ludwig Wittgenstein" ],
        "http://schema.org/sameAs": [ "http://viaf.org/viaf/24609378" ],
        "http://schema.org/birthPlace": [{
          "http://schema.org/name": [ "Vienna" ],
          "http://schema.org/geo": [{
            "http://schema.org/geo/latitude": ["48.20849"],
            "http://schema.org/geo/longitude": ["16.37208"]
          }]
        }]
    },
    //...
]
```

### Wikidata - Schema.org Property Mapper

[[Code]](../wikidatarefisland/services/schemaorg_property_mapper.py)

A service to retrieve the most recent state of mappings between Wikidata Properties and Schema.org properties using the [Wikidata Query Service](https://query.wikidata.org/).

Outputs a list of objects representing a mapping, where each object has the following structure:

* `property`: String representing a property on Wikidata.
* `url`: A Schema.org property URL

Example:

```js
[
    {
        "property": "P1476",
        "url": "http://schema.org/name"
    },
    //...
]
```

### Wikibase Value Matchers

[[Code]](../wikidatarefisland/data_model/wikibase/value_matchers.py)

This static class exposes methods to match between specified Wikibase (Wikidata) values and extracted data in a single [`MatchLine`](result.md#matchline). It relies on Wikibase [ValueType](../wikidatarefisland/data_model/wikibase/value_types.py) classes with a custom equivalence method to perform the matching and returns a boolean to determine whether a match exists in the data passed in.