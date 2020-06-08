# Running the Data Pipeline
This documentation is for developers wishing to run the pipeline in a large scale. It concisely describes how to analyse **all of Wikidata** in order to obtain potential reference matches.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

  - [Prerequisites](#prerequisites)
- [Steps to run](#steps-to-run)
  - [1. Setup Cloud VPS Virtual Machine](#1-setup-cloud-vps-virtual-machine)
  - [2. Run Side Service 1: External Resource Whitelister](#2-run-side-service-1-external-resource-whitelister)
  - [3. Run Pipe 1: Item Extractor](#3-run-pipe-1-item-extractor)
    - [Setup](#setup)
    - [Run](#run)
  - [4. Run the rest of the pipeline](#4-run-the-rest-of-the-pipeline)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Prerequisites

Running the Reference Island data pipeline on a large scale Wikidata dump is a process that requires multiple machines and a length of time. It is **not** recommended to run the entire pipeline on a developer laptop for large scale dumps because:

- Wikidata dumps are pretty large: ≈100s of GB uncompressed.
- Processing time for the entire pipeline is relatively long: According to the latest estimation, >40 days.

As a more robust solution, the development team recommends to run most of the pipeline on a Virtual Machine on [WMF's Cloud VPS](https://wikitech.wikimedia.org/wiki/Portal:Cloud_VPS) with the exception of [Pipe 1: Item Extractor](pipeline.md#pipe-1-item-extractor).

For Pipe 1 to read the complete dumps it is advisable to run on a machine in the [WMF Analytics cluster](https://wikitech.wikimedia.org/wiki/Analytics/Systems/Cluster). This is recommended because the machines in the Analytics cluster have the complete dumps available on fast storage.

The following documentation assumes that you:
- Have [set-up a Cloud VPS VM](https://wikitech.wikimedia.org/wiki/Help:Cloud_VPS_Instances)

    _**Note**: the Wikidata team has a Cloud VPS project called `wikidata-dev` for miscellaneous work_

- Have [permissions to access to the Analytics Cluster](https://wikitech.wikimedia.org/wiki/Analytics/Data_access)

# Steps to run

## 1. Setup Cloud VPS Virtual Machine

Clone the repository to your ***Cloud VPS VM***, and run the following command **in** the root of the repository folder: 

1. Create a python virtual environment **in** the repository root:

   ```bash
   python3 -m venv venv
   ```

   This has the advantage of keeping dependencies from this project separate from your system.

2. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

3. Install this package and it's dependencies into the python virtual environment:

   ```bash
   pip3 install .
   ```

   

## 2. Run [Side Service 1: External Resource Whitelister](pipeline.md#ss-1-external-resource-whitelister)

_**Important:** Do not run this step on an Analytics Cluster Machine, as it makes calls to third party websites._

On the ***Cloud VPS VM*** run the following:

```bash
make data/whitelisted_ext_idefs.json
```

## 3. Run [Pipe 1: Item Extractor](pipeline.md#pipe-1-item-extractor)

This step should be run on a machine in the ***Analytics cluster***. The initial development team ran it on `stat1005`.

### Setup
1. [Setup the HTTP Proxy](https://wikitech.wikimedia.org/wiki/HTTP_proxy) so that you can access the internet.
1. Clone this repository into a machine in the analytics cluster.
1. Create a python virtualenv in the repository root:

    ```bash
    virtualenv -p python3 venv
    ```
1. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```
1. Install this package and it's dependencies into the python virtual environment:

   ```bash
   pip install .
   ```

### Run

1. Copy across your generated `whitelisted_ext_idefs.json` to the `data` folder in this repository.

2. Run the following:

    ```bash
    DUMP_PATH=<path-to-dump-file> make data/extracted_unreferenced_statements.jsonl
    ```
    
    _**Note:** Make sure to set the `DUMP_PATH` to the path of the dump on that machine. It is recommended to use the `gz` dump due to the quicker decompression time. On `stat1005` the path to the dump is: `/mnt/data/xmldatadumps/public/wikidatawiki/entities/latest-all.json.gz`_

## 4. Run the rest of the pipeline
_**Important:** Do not run this step on an Analytics Cluster Machine, as it makes calls to third party websites._

Back on the ***Cloud VPS VM*** . follow the steps below:

1. Copy `extracted_unreferenced_statements.jsonl` from the ***Analytics cluster*** machine to to the `data` folder in this repository.

2. Run the following:

   ```bash
   make
   ```

This should trigger all the remaining jobs and the resultant data in `data/references.jsonl` is now ready for further
manual processing by you or to be [loaded into the Wikidata game](./wikidata-game.md#updating-the-game-data).

For more information on the Schema of the result data in `data/references.jsonl`, see [Pipeline Result Schema Reference](result.md).