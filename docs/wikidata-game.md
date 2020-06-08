# Reference Hunt Wikidata Game

This document describes various aspects of the Reference Hunt Wikidata Game: from updating the game's data to deploying new versions.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Background](#background)
  - [Distributed Game Requirements](#distributed-game-requirements)
  - [Game API Hosting](#game-api-hosting)
- [Updating The Game Data](#updating-the-game-data)
- [Development workflow](#development-workflow)
  - [Installing docker](#installing-docker)
  - [Installing composer dependencies](#installing-composer-dependencies)
  - [Running a copy of the game locally](#running-a-copy-of-the-game-locally)
  - [Running phpunit](#running-phpunit)
- [Automatic Deployment](#automatic-deployment)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Background

The development team for the Reference Island data pipeline implemented a [Wikidata Distributed Game](https://tools.wmflabs.org/wikidata-game/distributed/) to measure the quality of the pipeline, and add references to Wikidata.

For more information about the Wikidata Distributed Game and the Reference Hunt implementation, see the following:
- [Wikidata Distributed Game API documentation](https://bitbucket.org/magnusmanske/wikidata-game/src/master/public_html/distributed/?at=master)
- [Reference Hunt Distributed Game](https://tools.wmflabs.org/wikidata-game/distributed/#game=73)
- [Reference Treasure Hunt - Game Stats](https://tools.wmflabs.org/wd-ref-island/stats.php) (Live)

### Distributed Game Requirements

The Distributed Game platform requires developers to expose an api which provides:
* Serves "tiles" that can then be shown to users.
* Receives sent feedback about user actions. e.g. accepted or rejected tiles
* Provides a small summary for inclusion on the main page of the game (logo, description etc.)

### Game API Hosting

The API must be accessible by the Distributed Game platform over http(s). The development team chose to host the
Reference Hunt game API on [ToolForge](https://gerrit.wikimedia.org/r/admin/projects).

For more information about ToolForge and the specific tool see:
- [ToolForge Documentation](https://wikitech.wikimedia.org/wiki/Help:Toolforge)
- [wd-ref-island Tool Admin Panel](https://tools.wmflabs.org/admin/tool/wd-ref-island)

_**Note**: In order to gain access to the Game API and ToolForge tool, please get in touch with one of the maintainers listed  in the tool's admin panel_

## Updating The Game Data
The Reference Hunt Game API reads potential matches from a mysql database hosted on ToolForge. For an overview of the database schema
please see: [`wikidata_game/game.sql`](../wikidata_game/game.sql).

In order to obtain the potential matches and update the game database, make sure you are listed as a tool maintainer on ToolForge, and follow the steps below:

1. Run the Reference Island [Data Pipeline](pipeline.md) (see: [Production Pipeline Documentation](production-run.md)).

2. Log into the tool's [ToolForge Account](https://wikitech.wikimedia.org/wiki/Portal:Toolforge/Tool_Accounts). 

4. Upload the potential matches dump (the file called `references.jsonl`) to a path under the tool's home directory. 

5. Run the following command ***from the tool's home directory*** to populate the game's database:

   ```bash
   REFS_PATH="<path to references.jsonl>" php -f populator/populator.php
   ```

   _**Note:** don't forget to replace `<path to references.jsonl>` with the actual path to the potential matches dump file._

## Development workflow

Scripts for the game are found in the `wikidata_game` sub-folder of this repository.

### Installing docker
The Reference Hunt Game API includes an easy to use docker-compose environment for local development. To use
this environment install docker and docker-compose by following the
[docker-compose installation guide](https://docs.docker.com/compose/install/).

### Installing composer dependencies

To install the project's dependencies, run the following command **_in_** the `wikidata_game` directory:

```bash
docker run -it --rm --user $(id -u):$(id -g) -v ~/.composer:/tmp -v $(pwd):/app docker.io/composer install`
```

### Running a copy of the game locally
To start a local copy of the game API run:
```bash
docker-compose up
```
The game API will be available at `http://localhost:8100/api.php`

For more details see: [`docker-compose.yml`](../docker-compose.yml)

### Running phpunit

To run the phpunit tests locally, run the following command from the `wikidata_game` directory:

```bash
docker run -it --rm --user $(id -u):$(id -g) -v ~/.composer:/tmp -v $(pwd):/app docker.io/composer run-script test
```

## Automatic Deployment

The Reference Hunt Game API was set up manually on ToolForge. It includes GitHub Hook scripts to:

*  Keep the Game API updated when new commits are made to the master branch of this repository. 
* Provide a staging environment to verify unmerged branches of the API.

To automatically ***stage*** and ***deploy*** versions of the Game API, follow the steps below:

1. Ensure your branch name is prefixed with `game-`. Otherwise, automatic deployment and staging will not work.
2. Create a WIP pull request to this repository. This will create a staged version of the Game API from your branch.
3. To preview your changes go to `https://tools.wmflabs.org/wd-ref-island/test.php?branch=<your branch name>`.
4. Once your pull request is merged, the game will be automatically deployed to https://tools.wmflabs.org/wikidata-game/distributed/#game=73.
