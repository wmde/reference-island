
## Glossary

The following terms will be used throughout this document, their meanings are as follows:

**Pipe <#>:** Represents a sequential step in the main data pipeline, which processes Wikidata item serializations into a formatted list of potential references. 

**SS<#>:** Represents a "side service", to provide additional data to steps in the main pipeline, which will aid in making decisions or filter and format potential references.

## General Agreements

* The output formats for each step in the pipeline is to be formatted and encoded in `jsonl` with the exception of [Pipe 5](#pipe-5).

## Pipe 1: Find unreferenced statements and URLs for a given list of Wikidata items<a name="pipe-1"></a>

This step will take in the following inputs, and will output the data expected in [Pipe 2](#pipe-2).

* `whitelistedExtIds`: List of strings representing whitelisted Wikidata external id properties, same as output of [SS1](#ss-1).

* `items`: List of Wikidata item serializations, as described in the [Wikibase Data Model documentation](https://www.mediawiki.org/wiki/Wikibase/DataModel/JSON)

A python implementation of this pipe can be found as `ItemExtractorPipe` in `item_extractor_pipe.py`

### Getting some initial data
Obtaining a small sample to test this pipe with locally can be a challenge. The python implementation was designed to
work either complete or partial parts of the JSON dumps of Wikidata. See: https://dumps.wikimedia.org/other/wikibase/wikidatawiki/

A very rough dump can be obtained by doing the following:
`wget https://dumps.wikimedia.org/other/wikibase/wikidatawiki/latest-all.json.gz`
and hitting Ctrl-C after bit of data has transferred

Then writing this to a json file:
`zcat latest-all.json.gz > dumps.json`

You might see errors since there will probably be a partial chunk that is missing but this isn't a
problem with the python implementation since the partially corrupt last line will just be ignored.

## Pipe 2: Scrape given URLs for potential matches between  unreferenced statements and structured data<a name="pipe-2"></a>

This step will take in the following inputs and will output the data expected in [Pipe 3](#pipe-3).

* `items`:  List of objects to represent Wikidata Items with the following keys:

  * `itemId`: The Wikidata id of the item being examined

  * `resourceUrls`: List of objects describing external resources to scrape, and reference meta data to be added to references.

    * `url`: String representing the url to scrape
    * `referenceMetadata`: Data to append to the potential references matched at the end of this stage with optional reference keys. 

    ***Note***: An example for this property can be found in the output provided by [SS4](#ss-4).
    
  * `statements`: List of unreferenced statements where each individual statement has the following structure: <a name="statement-blob"></a>
    
    * `pid`: The property id of the statement

    * `value`: The data value of the statement / Item id of the Wikidata item value.

    * `datatype`: The string describing the type of data held in value.

    <a name="statement-dict"></a>Template:
    ```json
    {
      "pid": [String],
      "datatype": [String],
      "value": {valueBlob}
    }
    ```

    See [Wikibase JSON response documentation](https://gerrit.wikimedia.org/r/plugins/gitiles/mediawiki/extensions/Wikibase/+/master/docs/topics/json.md#Snaks-json_snaks) for the `datavalue -> value` key.

    An example for the valueBlob:
    ```json
    {
      "entity-type": "item",
      "numeric-id": 350,
      "id": "Q350"
    }
    ```

    Complete Statement Example:
    ```json
    [
        {
            "pid": "P321", 
            "datatype": "wikibase-item",
            "value": {
              "numeric-id": 214917,
              "id": "Q214917"
            },
        },
        {
            "pid": "P777",
            "datatype": "time",
            "value": {
              "time": "+2013-12-07T00:00:00Z",
              "timezone": 0,
              "before": 0,
              "after": 0,
              "precision": 11,
              "calendarmodel": "http://www.wikidata.org/entity/Q1985727"
            }
        }
    ]
    ...
    ```

## Pipe 3: Filter extracted values by plain text matching<a name="pipe-3"></a>

This step will take the output of Pipe 2 as it's primary input. It will also take the output of SS2 as an input.

One row of this file relates to one unreferenced statement and one potential reference, mutliple references for the same statemnet will be repeated in multiple lines. It contains the `itemId` the statement was on as well as all the extracted structured data that relates to this statement and `referenceMetadata` referring to where that data came from.

The format of the template of one row of Pipe 2 is as follows:
```json
{
  "statement": {statementBlob},
  "itemId": [itemId],
  "reference": {
    referenceMetadata: referenceBlob,
    extractedData: [ [value] ]
    }
}
```
For details about the statement format see that in [Pipe 2](#statement-blob)

### `referenceBlob` format
Note this corresponds to the format of the referenceMetadata seen in [SS4](#ss-4) with the new requirement of a  key value pair co-responding to  the date retrieved.
```json
{
  *[statedInPropId]: [externalIdItem],
  *[externalIdProp]: [externalIdVal],
  *[referenceUrl]: [String],
  [dateRetrieved]: [String]
}
```

## Pipe 5: Format potential references into Quickstatements format<a name="pipe-5"></a>

### <a name="statement-reference-blob"></a>Input format
```json
{ 
    "itemId": [itemId],
    "statement": { statementBlob }, 
    "reference": referenceBlob,
}
```

## SS1: Find good external Id Properties<a name="ss-1"></a>

A service to whitelist external id properties based on a predefined blacklist, and the amount of Schema.org definitions found in a sample external resource.

This service takes in a list of  manually blacklisted external ids, and retrieves a list of currently available external ids from Wikidata.

The output for this service is a listed of string representation of whitelisted external ids. For example:  

  ```json
  ["P1234", "P1233", ...]
  ```

## SS2: Fetch current mappings between Wikidata Properties and Schema.org Properties<a name="ss-2"></a>

A service to retrieve the most recent state of mappings between Wikidata Properties and Schema.org properties.

Outputs a list of objects representing a mapping. Each object has the following structure:

* `property`: String representing a property on Wikidata.
* `url`: A Schema.org property URL

Example:

```json
[
    {
        "property": "P1476",
        "url": "http://schema.org/name"
    },
    ...
]
```



## SS3 (Utility Class): Normalize data from various scraped raw formats<a name="ss-3"></a>

This service takes in an object containing raw scraped data in `json-ld` format (For example, the results of the following scraping library: https://github.com/scrapinghub/extruct with the [`uniform` option set to true](https://github.com/scrapinghub/extruct#uniform)).

The output of this service will be a list of objects representing a Schema.org type with the following structure: 

```json
[
    {
        "http://schema.org/name": [ "Ludwig Wittgenstein" ],
        "http://schema.org/sameAs": [ "http://viaf.org/viaf/24609378" ],
        "http://schema.org/birthPlace": {
          "http://schema.org/name": [ "Vienna" ],
          "http://schema.org/geo": {
            "http://schema.org/geo/latitude": "48.20849",
            "http://schema.org/geo/longitude": "16.37208"
          }
        }
    },
    ...
]
```

## SS4: Map External ID Properties and Values to URL and reference metadata<a name="ss-4"></a>

This service takes in a string representation of an external id property and attempts to output a formatted URL  for an external resource, as well as reference metadata according to the Wikidata mapping. If non is found it will return `false`.

The output format is an object with the following properties:

* `url`: The formatted URL of an external resource

* `referenceMetadata`: An object representing meta data for a potential reference, with the following key-value pairs:

  | Key                              | Value                                     |
  | -------------------------------- | ----------------------------------------- |
  | "P248" ("stated in" Property id) | Wikidata item representing an external id |
  | Passed in external id property   | Passed in external id value               |

  Example (WorldCat Identities record for Ludwig Wittgenstein, with Wikidata property mapping):

   ```json
  {
      "url": "https://www.worldcat.org/identities/lccn-n79032058/",
      "referenceMetadata": {
          "P248": "Q76630151",
          "P7859": "lccn-n79032058"
      }
  }
   ```

  # SS5: Download schema.org json-ld context
 This services downloads the schame.org json-ld context. Until 2020-05-19 it was possible for pyld to automatically
 obtain it through content-negotiation of `http://schema.org` but this broke.

 This side-service has a backup method to get the context from the schema.org docs