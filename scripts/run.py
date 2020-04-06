import argparse
import os

from wikidatarefisland import data_access, Config, external_identifiers


def main():
    parser = argparse.ArgumentParser(description='Run the pipes and/or side steps')
    parser.add_argument('--step', default=[], dest='steps', action='append', type=str,
                        help='Steps to run e.g. ss1 or pipe2, default: Run all')

    steps = parser.parse_args().steps
    if steps == []:
        steps = ['all']

    file_path = os.path.realpath(__file__)
    config = Config.newFromScriptPath(file_path)
    wdqs_reader = data_access.WdqsReader.newFromConfig(config)
    storage = data_access.Storage.newFromScript(file_path)

    if 'ss1' in steps or 'all' in steps:
        external_identifiers.GenerateWhitelistedExtIds(wdqs_reader, storage, config).run()


if __name__ == "__main__":
    main()
