# Pipeline Result Schema Reference

The following document describes the various data dump outputs of the Reference Island data pipeline process, and the structure of the data within.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [JSON and JSON-L dumps](#json-and-json-l-dumps)
  - [Allowed External Ids Dump](#allowed-external-ids-dump)
  - [Extracted Items Dump](#extracted-items-dump)
  - [Potential Matches Dump](#potential-matches-dump)
- [Lines](#lines)
  - [`ItemLine`](#itemline)
  - [`MatchLine`](#matchline)
- [Blobs](#blobs)
  - [`StatementBlob`](#statementblob)
    - [Potential Values](#potential-values)
  - [`ResourceBlob`](#resourceblob)
  - [`ReferenceBlob`](#referenceblob)
  - [`ReferenceMetaBlob`](#referencemetablob)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## JSON and JSON-L dumps

### Allowed External Ids Dump

This dump is the Result of [SS 1: External Resource Checker](pipeline.md#ss-1-external-resource-checker). It is a `json` file containing an array of Wikibase external id PID strings.

[Scrape #3 Allowed Resources Example](https://raw.githubusercontent.com/wmde/reference-hunting-data/master/allowed_ext_idefs.json?token=ABOZJNMEXT7OJRQDOAVWDUC63JNUQ).


### Extracted Items Dump

This dump is the result of [Pipe 1: Item Extractor](pipeline.md#pipe-1-item-extractor). It is a `jsonl` file where each line follows the [`ItemLine`](#itemline) schema. 

[Scrape #2 Item Dump Example](https://github.com/wmde/reference-hunting-data/raw/master/first_run/extracted_unreferenced_statements.jsonl.gz).

### Potential Matches Dump

This dump is the result of [Pipe 2: Scraper](pipeline.md#pipe-2-scraper), [Pipe 3: Value Matcher](pipeline.md#pipe-3-value-matcher) and [Pipe 4: Statistical Matcher](pipeline.md#pipe-4-statistical-matcher). It is a `jsonl` file where each line follows the [`MatchLine`](#matchline) schema.

[Scrape #2 Potential Match Example](https://raw.githubusercontent.com/wmde/reference-hunting-data/master/second_run/references.jsonl?token=ABOZJNJRCIEWGXBVW5G4HAS63JN5U).

## Lines

### `ItemLine`

A JSON object to represent a Wikibase item which contains unreferenced statements and [***allowed***](pipeline.md#ss-1-external-resource-checker) external source URLs. This information is extracted from a Wikidata data dump in [Pipe 1: Item Extractor](#pipe-1-item-extractor).

```js
{
     "itemId": String // Wikibase QID of the item 
     "statements": [ StatementBlob ] // An array of unreferenced statement claims
     "resourceUrls": [ ResourceBlob ] // An array of data describing resource URLs to scrape
}
```

For more information on the various sub-schema included in an `ItemLine` follow the links below:

* [`StatementBlob`](#statementblob)
* [`ResourceBlob`](#resourceblob)

### `MatchLine` 

JSON object representing a ***potential*** data match between an unreferenced Wikibase Statement claim and a piece of extracted data, as well as encoded information for generating a Wikibase reference.

```js
{
    "itemId": String, // Wikibase QID of the item which contains the statement claim
    "statement": StatementBlob, // The statement data to be matched
    "reference": ReferenceBlob // Data regarding the potential matched reference
}
```

For more information on the various sub-schema included in a `MatchLine` follow the links below:

* [`StatementBlob`](#statementblob)
* [`ReferenceBlob`](#referenceblob)

## Blobs

### `StatementBlob`

The `StatementBlob` schema describes an unreferenced Wikibase Statement claim, and it's value. 

```js
{
    "pid": String, // Wikibase PID of the property of the statement
    "datatype": String, // Wikibase data type see: https://www.wikidata.org/wiki/Special:ListDatatypes
    "value": Mixed // Data describing the matched value from a Wikibase
}
```

#### Potential Values

The `"value"` key in a statement can contain any of the value objects extracted from from a Wikibase JSON representation of an item. Same as the `"value"` key in [Wikibase JSON Response Data Value Documentation](https://gerrit.wikimedia.org/r/plugins/gitiles/mediawiki/extensions/Wikibase/+/master/docs/topics/json.md#data-values-json_datavalues). In the current implementation, supported values are for the following Wikibase data types:

* ##### `"string"` & `"url"`

	In these cases, `"value"` will be a `String` literal value containing the text or url to match e.g.: `"Ludwig Wittgenstein"` or `"http://www.example.com"`

	**Schema Example:**
	
	```js
	{
	    //...
	    "value": String
	}
	```

* ##### `"monolingualtext"`

	In this case the `"value"` is an object containing the text to match and the language it is written in. See list of [Wikidata data types](https://www.wikidata.org/wiki/Special:ListDatatypes) for more information.

	**Schema Example:**

    ```js
    {
        //...
        "value": {
            "text": String, // The text itself
            "language": String // The language code of the text
        }
    }
    ```

* ##### `"quantity"`

	The `"value"` for quantity will be an object containing various information regarding quantity values. See [quantity](https://gerrit.wikimedia.org/r/plugins/gitiles/mediawiki/extensions/Wikibase/+/master/docs/topics/json.md#quantity-json_datavalues_quantity) in Wikibase JSON Response Documentation.

	**Schema Example:**

    ```js
    {
        //...
        "value": {
            "amount": String, // A string representation of a number including the sign (+/-)
            "unit": String, // 1 for unitless quantities or URI to Wikibase item of unit e.g. "https://www.wikidata.org/wiki/Q11573" 
            "upperBound": String, // Optional string representation of a number to encode uncertainty
            "lowerBound": String, // Optional string representation of a number to encode uncertainty
        }
    }
    ```

* #####  `"globe-coordinate"`

	In this case the `"value"` is an object containing coordinate information. For more information see [globecoordinate](https://gerrit.wikimedia.org/r/plugins/gitiles/mediawiki/extensions/Wikibase/+/master/docs/topics/json.md#globecoordinate-json_datavalues_globe) in Wikibase JSON Response Documentation.

	**Schema Example:**

    ```js
    {
        //...
        "value": {
            "latitude": Number, // Floating point number 
            "longitude": Number, // Floating point number 
            "altitude": null, // Unused, always null
            "precision": Number, // Floating point or scientific notation number, null when information is not provided
            "globe": String // URI to Wikibase item of the globe these coordinates are on, e.g. "http://www.wikidata.org/entity/Q2" 
        }
    }
    ```

* ##### `"time"`

    Here the `"value"` will be an object containing date and time information. For more information, see [time](https://gerrit.wikimedia.org/r/plugins/gitiles/mediawiki/extensions/Wikibase/+/master/docs/topics/json.md#time-json_datavalues_time) in Wikibase JSON Response Documentation.

    **Schema Example:**

    ```js
    {
        //...
        "value": {
            "time": String, // A **near** ISO 8601 time representation
            "timezone": Number, // Unused, currently always 0 
            "before": Number, // Unused, currently always 0
            "after": Number, // Unused, currently always 0
            "precision": Number, // Integer between 0 - 14 representing the precision unit 
            "calendarmodel": String // URI to wikibase item of calendar model, e.g. "http://www.wikidata.org/entity/Q1985727"
        }
    }
    ```

* ##### `"wikibase-item"`

    For this data type `"value"` will be an object containing information about the item id. For more information, see [wikibase-entityid](https://gerrit.wikimedia.org/r/plugins/gitiles/mediawiki/extensions/Wikibase/+/master/docs/topics/json.md#wikibase_entityid-json_datavalues_entityid) in Wikibase JSON Response Documentation.

    **Schema Example**:

    ```js
    {
        //...
        "value": {
            "entity-type": String, // Will always be "item" in this case
            "id": String, // Wikibase QID
            "numeric-id": Number // Numeric representation of the above id
          }
    }
    ```
### `ResourceBlob`

A `ResourceBlob` schema describes a URL to scrape for data matches, as well as instructions on building a potential reference for that URL.

```js
{
    "url": String // The URL to scrape for data
    "referenceMetaData": ReferenceMetaBlob // Data for constructing a Wikibase reference, without the "dateRetrieved" key
}
```

For more information on the various sub-schema included in a `ResourceBlob` follow the links below:

* [`ReferenceMetaBlob`](#referencemetablob)

### `ReferenceBlob`

The `ReferenceBlob` schema describes data to support a potential reference, as well as the potential reference itself.

```js
{
    "extractedData": [ Mixed ] // An array of data extracted for this statement
    "referenceMetadata": ReferenceMetaBlob, // Data for constructing a Wikibase reference 
}
```

For more information on the various sub-schema included in a `ReferenceBlob` follow the links below:

* [`ReferenceMetaBlob`](#referencemetablob)

### `ReferenceMetaBlob`

A `ReferenceMetaBlob` is a schema which provides essential information for constructing a reference on a Wikibase project. The keys in this object schema are meant to be dynamic in order to support building references through the Wikibase api. 

```js
{
    "dateRetrieved": String // GMT date-time representation formatted as YYYY-MM-DD HH:MM:SS,
    /** 
    * A key value pair representing a "stated in" claim:
    * Key: Always "P248" in our case (Wikidata "stated in" PID)
    * Value: Wikibase QID for an item representing the reference source
    **/
    STATED_IN_PID: String,
    /** 
    * A key value pair representing an "external id" claim:
    * Key: Wikibase PID representing the external id for the reference source 
    * Value: The id value for the above external id
    **/
    EXTERNAL_ID_PID: String,
    /** 
    * A key value pair representing a "reference URL" claim:
    * Key: Always "P854" in our case (Wikidata "reference URL" PID)
    * Value: The url the data was extracted from
    **/
    REFERENCE_URL_PID: String
}
```