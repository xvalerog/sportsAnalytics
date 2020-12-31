
"""
Module that imports the data from your Garmin device to a given folder of your computer
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

from garminexport.incremental_backup import incremental_backup
from garminexport.logging_config import LOG_LEVELS
import yaml
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

#Get the right path to the config.yml and open it
path = os.getcwd()
(new_path, NULL) = path.rsplit("/", 1)
with open(new_path + "/config.yml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)


def main():

    logging.root.setLevel(LOG_LEVELS[cfg['importData']['log_level']])

    try:
        incremental_backup(username=cfg['general']['user_name'],
                       password=cfg['general']['password'],
                       backup_dir=cfg['importData']['backup_dir'],
                       export_formats=cfg['importData']['format'],
                       ignore_errors=cfg['importData']['ignore_errors'],
                       max_retries=cfg['importData']['max_retries'])



    except Exception as e:
        log.error("failed with exception: {}".format(e))


main()