#!/usr/bin/env python

import os.path
import sys
import logging

from clean_utils import *
from utils import *

mkdir_p(BASE_DIR)

logging.basicConfig(format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
        datefmt='%H:%M:%S',
        stream=sys.stdout,
        level=logging.INFO)
log = logging.getLogger(__name__)


###################
# CSV import config

description = "311_complaints"

table_name = "call_311"

dtype_dict = {
        'Unique Key':'int64',
        'Created Date':'object',
        'Closed Date':'object',
        'Agency':'object',
        'Agency Name':'object',
        'Complaint Type':'object',
        'Descriptor':'object',
        'Location Type':'object',
        'Incident Zip':'object',
        'Incident Address':'object',
        'Street Name':'object',
        'Cross Street 1':'object',
        'Cross Street 2':'object',
        'Intersection Street 1':'object',
        'Intersection Street 2':'object',
        'Address Type':'object',
        'City':'object',
        'Landmark':'object',
        'Facility Type':'object',
        'Status':'object',
        'Due Date':'object',
        'Resolution Description':'object',
        'Resolution Action Updated Date':'object',
        'Community Board':'object',
        'Borough':'object',
        'X Coordinate (State Plane)':'float64',
        'Y Coordinate (State Plane)':'float64',
        'Park Facility Name':'object',
        'Park Borough':'object',
        'School Name':'object',
        'School Number':'object',
        'School Region':'object',
        'School Code':'object',
        'School Phone Number':'object',
        'School Address':'object',
        'School City':'object',
        'School State':'object',
        'School Zip':'object',
        'School Not Found':'object',
        'School or Citywide Complaint':'object',
        'Vehicle Type':'object',
        'Taxi Company Borough':'object',
        'Taxi Pick Up Location':'object',
        'Bridge Highway Name':'object',
        'Bridge Highway Direction':'object',
        'Road Ramp':'object',
        'Bridge Highway Segment':'object',
        'Garage Lot Name':'object',
        'Ferry Direction':'object',
        'Ferry Terminal Name':'object',
        'Latitude':'float64',
        'Longitude':'float64',
        'Location':'object'
}

keep_cols = [
    "Unique Key",
    "Created Date",
    "Closed Date",
    "Agency",
    "Complaint Type",
    "Descriptor",
    "Incident Zip",
    "Incident Address",
    "Street Name",
    "Cross Street 1",
    "Cross Street 2",
    "Intersection Street 1",
    "Intersection Street 2",
    "City",
    "Status",
    "Due Date",
    "Resolution Description",
    "Resolution Action Updated Date",
    "Borough",
    "Latitude",
    "Longitude",
    "Location"
]

truncate_columns = ['resolution_description']

date_time_columns = ['created_date','closed_date','due_date', 'resolution_action_updated_date']

datasets = {
    'complete': "https://nycopendata.socrata.com/api/views/erm2-nwe9/rows.csv?accessType=DOWNLOAD",
    # This is a view created by Chris Henry which filters by the complaint type
    #   indicated https://docs.google.com/spreadsheets/d/1hJIRu1Ku2pgaKfbFjXLEzN2jNH9rYmUtjpLZZHbfe80/edit
    # Additional views can be created at https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9/data
    'filtered': "https://data.cityofnewyork.us/api/views/7y5a-jzir/rows.csv?accessType=DOWNLOAD"
}

def main():
    extra_args = {
        '--dataset': {
            'default': 'filtered',
            'choices': ['complete','filtered'],
            'help': "Which 311 Socrata dataset."
        }
    }
    args = get_common_arguments('Import 311 complaints dataset.', extra_args=extra_args)

    if not args.SKIP_IMPORT:
        import_csv(args)

    sql_cleanup(args)


def import_csv(args):
    csv_dir = os.path.join(BASE_DIR, table_name)
    mkdir_p(csv_dir)

    csv_file = os.path.join(csv_dir, '311-full.csv')
    csv_url = datasets[args.dataset]

    if not os.path.isfile(csv_file) or args.BUST_DISK_CACHE:
        log.info("DL-ing 311 complaints")
        download_file(csv_url, csv_file)
    else:
        log.info("311 complaints exist, moving on...")

    pickle = os.path.join(csv_dir, 'split', '311-chunk-{}.pkl')
    csv_chunk_size = 250000

    hpd_csv2sql(description, args, csv_file, table_name, dtype_dict, truncate_columns,
            date_time_columns, keep_cols, pickle, csv_chunk_size=csv_chunk_size)


def sql_cleanup(args):
    log.info('SQL cleanup...')

    sql = clean_addresses(table_name, "incident_address") + \
        clean_boro(table_name, "borough", full_name_boro_replacements())

    run_sql(sql, args.TEST_MODE)


if __name__ == "__main__":
    main()
