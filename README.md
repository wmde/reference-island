# Wikidata Reference Island
![reference_island_logo](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Treasure_map.png/120px-Treasure_map.png)
## Installation and Running Tests
We can create a python virtual environment.
This has the advantage of keeping dependencies from this project separate from your system.

Create a venv in a folder `./venv`
`python3 -m venv venv`

Active the virtual environment:
`source venv/bin/active`

Install this library and test dependencies:
`pip3 install .`
`pip3 install -e .[tests]`

Run linter:
`flake8 .`

Run tests:
`pytest`

To leave the virtual environment:
`deactivate`

## Running the pipeline
To run the whole pipeline end to end, put the dump on data/dump.json and then run:

`make`

### Running each part of the pipeline
For each part of the pipeline, add name of the file as argument to make (for more information on pipes and side services see `docs/api.md`):
 - `make data/whitelisted_ext_idefs.json` runs SS1
 - `make data/extracted_unreferenced_statements.jsonl` runs pipe1
 - `make data/scraped_data.jsonl` runs pipe2
 - `make data/matched_references.jsonl` runs pipe3
 - `make data/matched_item_references.jsonl` runs pipe4
 - `make` or `make data/references.jsonl` runs and merges pipe3 and pipe4
