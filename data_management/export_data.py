"""
Module that exports the Garmin .fit files to csv files.
Merits to Max Candocia
Tutorial: https://maxcandocia.com/article/2017/Sep/22/converting-garmin-fit-to-csv/

Required:
- fitparse => pip install fitparse
- Garmin .fit files stored in a given directory
    => Use data_management.import_data.py to get the .fit files from your Garmin account

- config.yml => yaml file with the required parameters:

    exportData:
        input_dir: "<path where Garmin .fit files are stored"
        export_dir: "<path where to store the converted .csv files"
        timezone: "<timezone>" #check pytz.timezone documentation
        export_fields: ["timestamp", "distance", "altitude", "speed", "heart_rate", "cadence"]
           # Required field: "timestamp"
           # Optional fields: ["position_lat", "position_long", "distance", "altitude", "speed", "vertical_oscillation",
           #  "stance_time_percent", "stance_time", "vertical_ratio", "stance_time_balance", "step_length", "unknown_87",
           #  "heart_rate", "cadence", "temperature", "activity_type", "fractional_cadence"]

"""

import csv
import os
import fitparse
import pytz
import yaml


# --------------------------------------------------------------------------
#                        SETUP
# --------------------------------------------------------------------------
#Get the right path to the config.yml and open it
input_dir = os.getcwd()
(new_path, NULL) = input_dir.rsplit("/", 1)
with open(new_path + "/config.yml") as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)

#Get all config parameters
input_dir = cfg['exportData']['input_dir']
export_dir = cfg['exportData']['export_dir']
export_fields = cfg['exportData']['export_fields']
UTC = pytz.UTC
CST = pytz.timezone(cfg['exportData']['timezone'])


# --------------------------------------------------------------------------
#                        MAIN
# --------------------------------------------------------------------------

def main():
    # Parse fit file path or directory
    if input_dir[-4:].lower() == '.fit':
        _temp = input_dir.rpartition('/')
        directory = _temp[0] + _temp[1]
        files = [_temp[2]]
    else:
        directory = input_dir
        files = os.listdir(input_dir)

    fit_files = [file for file in files if file[-4:].lower() == '.fit']
    for file in fit_files:
        new_filename = export_dir  + file[:-4] + '.csv'
        if os.path.exists(new_filename):
            print('%s already exists. skipping.' % new_filename)
            continue

        filePath = directory + file
        fitfile = fitparse.FitFile(filePath,
                                   data_processor=fitparse.StandardUnitsDataProcessor())

        print('converting %s' % file)

        # Wite fit data into csvs
        write_fitfile_to_csv(fitfile, new_filename)
    print('finished conversions')


# --------------------------------------------------------------------------
#                        OTHER FUNCTIONS
# --------------------------------------------------------------------------

def write_fitfile_to_csv(fitfile, output_file):
    """
    Function to write the imported fit files into csvs
    Input:
    :param fitfile:
    :param output_file:
    Output:
    csv file with all "export_fields" from fit object
    Return:
    """

    messages = fitfile.messages
    data = []
    for m in messages:
        skip = False
        if not hasattr(m, 'fields'):
            continue
        fields = m.fields
        # check for important data types
        mdata = {}
        time_stamp_exists = False
        for field in fields:
            if field.name in export_fields:
                if field.name == 'timestamp':
                    mdata[field.name] = UTC.localize(field.value).astimezone(CST)
                    time_stamp_exists = True
                else:
                    mdata[field.name] = field.value
        # if user forgot to introduce "timestamp", we force it
        if time_stamp_exists == False:
            mdata['timestamp'] = UTC.localize(field.value).astimezone(CST)

    # write to csv
    with open(output_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(export_fields)
        for entry in data:
            writer.writerow([str(entry.get(k, '')) for k in export_fields])
    print('wrote %s' % output_file)


if __name__ == '__main__':
    main()