"""
Script that imports the data from your Garmin device to a given folder of your computer
Required:
garminexport  => pip install garminexport
config.yml => yaml file with the required parameters:

    general:
        user_name: "<Garmin account email>"
        password: "<Garmin account password>"

    importData:
        backup_dir: "<path where to store the imported Garmin data"
        format: ["json_summary","json_details", "gpx", "tcx", "fit"] #choose as many as desired, but always as a list
        ignore_errors: False #default
        max_retries: 7 #detault
        log_level: "INFO" #DEBUG, INFO, WARNING, ERROR

"""

import argparse
from garminexport.incremental_backup import incremental_backup
from garminexport.logging_config import LOG_LEVELS
import yaml
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments.

    :return: Namespace object holding parsed arguments as attributes.
    This object may be directly used by sportsAnalytics/import_Garmin_data.
    """
    parser = argparse.ArgumentParser(
        prog="import_garmin_data",
        description=(
            "Imports raw data from your Garmin device according to the parameters"
            "specified in the config.yml file"
            "Import is done from a given Garmin Connect account."
            "Only activities not yet stored in the backup directory will "
            "be imported."))
    # positional args
    parser.add_argument(
        "--config", metavar="<config>", type=str, help="Config file in yml format")
    # optional args
    parser.add_argument(
        "--password", type=str, help="Account password.")

    return parser.parse_args()


def main():
    args = parse_args()

    with open(args.config) as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)

    if args.password is not None:
        cfg['general']['password'] = args.password
        #print("password by CLI")
    #else:
     #   print(cfg['general']['password'])

    logging.root.setLevel(LOG_LEVELS[cfg['importData']['log_level']])

    try:
        incremental_backup(username=cfg['general']['user_name'],
                           password=cfg['general']['password'],
                           backup_dir=cfg['importData']['backup_dir'],
                           export_formats=cfg['importData']['format'],
                           ignore_errors=cfg['importData']['ignore_errors'],
                           max_retries=cfg['importData']['max_retries'])
        print("process done")

    except Exception as e:
        log.error("failed with exception: {}".format(e))

if __name__ == '__main__':
    main()