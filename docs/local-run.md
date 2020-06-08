# Local Run and Development

This documentation is aimed at developers wishing to run the Reference Island Data Pipeline on a small scale with their local machines or continue the development of the data pipeline.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*


- [Prerequisites & Setup](#prerequisites--setup)
- [Running the Data Pipeline](#running-the-data-pipeline)
  - [Getting some sample data](#getting-some-sample-data)
  - [Running the full pipeline](#running-the-full-pipeline)
  - [Running parts of the pipeline individually](#running-parts-of-the-pipeline-individually)
- [Testing & Development](#testing--development)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Prerequisites & Setup

The Reference Island Data Pipeline is a python package designed to extract potential references from the internet. As such, please make sure that the system in which you are running this on has Python 3.7+ installed or [setup with a pyenv](https://www.freecodecamp.org/news/manage-multiple-python-versions-and-virtual-environments-venv-pyenv-pyvenv-a29fb00c296f/).

1. Clone this repository to your machine:

    ```bash
    git clone https://github.com/wmde/reference-island.git
    ```

2. Create a python virtual environment **in** the repository root:

    ```bash
    python3 -m venv venv
    ```

    This has the advantage of keeping the dependencies of this project separate from your system.

3. Activate the virtual environment:

    ```bash
    source venv/bin/activate
    ```

4. Install this package and it's dependencies into the python virtual environment:

    ```bash
    pip3 install .
    ```

## Running the Data Pipeline

In order to run the Reference Island Data Pipeline, you will need to obtain a small set of Wikibase item dump, in the same format as a [Wikidata JSON dumps](https://www.wikidata.org/wiki/Wikidata:Database_download#JSON_dumps_(recommended)). 

_**Important:** It is **not** recommended to run the entire pipeline on a developer laptop for large scale dumps. If you would like to run the pipeline on a large part of Wikidata, see the [production run documentation](production-run.md)._

### Getting some sample data

In case you don't have a small dataset to run the data pipeline on, you can follow the steps below to obtain a small sample of the Wikidata Dumps (See [Wikidata dumps directory](https://dumps.wikimedia.org/other/wikibase/wikidatawiki/) for a list of most recent entity dumps). 

1. Start downloading the latest dump:

   ```bash
   wget https://dumps.wikimedia.org/other/wikibase/wikidatawiki/latest-all.json.gz
   ```

2. After retrieving a some data, press <kbd>Ctrl</kbd> + <kbd>C</kbd> to stop the download.

3. Write the downloaded data into a `json` file:

   ```bash
   zcat latest-all.json.gz > dumps.json
   ```

   _**Note:** You might see errors since there will probably be a partial chunk that is missing from the file. This isn't a problem however, as the pipeline will ignore the corrupt chunk._

### Running the full pipeline

As each step of the Reference Island Data Pipeline is encoded as a command in a [`Makefile`](../Makefile), running the whole pipeline is fairly simple:

```bash
DUMP_PATH=<path-to-dump-file> make
```

_**Note:** Make sure to set the `DUMP_PATH`  environment variable to the path of the dump on **your** machine. See [instructions for obtaining data](#getting-some-sample-data) above._

### Running parts of the pipeline individually

To run only individual parts of the data pipeline, add a name for the result file as an argument to the `make` command. See the following for more information regarding each step of the pipeline:

*  [Data Pipeline Reference](pipeline.md) provides more information on each of the pipeline stages
*  [Pipeline Result Schema Reference](result.md) provides more information on the results of each step.

The commands for each sequential step are as follows:

1. `make data/whitelisted_ext_idefs.json` runs [SS 1: External Resource Whitelister](pipeline.md#ss-1-external-resource-whitelister)
2. `DUMP_PATH=<path-to-dump-file> make data/extracted_unreferenced_statements.jsonl` runs [Pipe 1: Item Extractor](pipeline.md#pipe-1-item-extractor)
3. `make data/schema_org_context.jsonld` runs [SS 2: Schema.org JSON-LD context fetcher](pipeline.md#ss-2-schemaorg-json-ld-context-fetcher)
4. `make data/scraped_data.jsonl` runs [Pipe 2: Scraper](pipeline.md#pipe-2-scraper)
5. `make data/matched_references.jsonl` runs [Pipe 3: Value Matcher](pipeline.md#pipe-3-value-matcher)
6. `make data/matched_item_references.jsonl` runs [Pipe 4: Statistical Matcher](pipeline.md#pipe-4-statistical-matcher)

Additionally, running `make data/references.jsonl` runs and merges Pipe 3 and Pipe 4.

## Testing & Development

The Data Pipeline python package includes handy tools for local development. To use these tools:

1. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

2. Install the Development dependencies and tests

   ```bash
   pip3 install .
   pip3 install -e .[tests]
   ```

After setting up you may run the following commands (in the repository root):

* Run linter:

  ```bash
  flake8 .
  ```

* Run unit and integration tests:

  ```bash
  pytest
  ```

* Leave the virtual environment:

  ```bash
  deactivate
  ```

