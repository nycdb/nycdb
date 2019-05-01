TABLES = {
    'pluto_15v1': {'pluto_15v1': 800000},
    'pluto_16v2': {'pluto_16v2': 800000},
    'pluto_17v1': {'pluto_17v1': 800000},
    'pluto_18v1': {'pluto_18v1': 800000},
    'pluto_18v2': {'pluto_18v2': 800000},
    'dobjobs': {'dobjobs': 1000000},
    'dob_violations': {'dob_violations': 2000000},
    'ecb_violations': {'ecb_violations': 1300000},
    'hpd_violations': {'hpd_violations': 4000000},
    'hpd_registrations': {
        'hpd_registrations': 150000,
        'hpd_contacts': 600000,
        'hpd_corporate_owners': 30000,
        'hpd_business_addresses': 130000,
        'hpd_registrations_grouped_by_bbl': 130000,
        'hpd_registrations_grouped_by_bbl_with_contacts': 130000
    },
    'dof_sales': {'dof_sales': 75000},
    'rentstab': {'rentstab': 45000},
    'rentstab_summary': {'rentstab_summary': 45000},
    'dob_complaints': {'dob_complaints': 1000000},
    'hpd_complaints': {
        'hpd_complaints': 1000000,
        'hpd_complaint_problems': 2000000
    },
    'acris': {
        'real_property_remarks': 1000000,
        'real_property_legals': 1000000,
        'real_property_master': 1000000,
        'real_property_parties': 1000000,
        'real_property_references': 1000000,
        'personal_property_legals': 1000000,
        'personal_property_master': 1000000,
        'personal_property_parties': 1000000,
        'personal_property_references': 1000000,
        'personal_property_remarks': 400000,
        'acris_country_codes': 250,
        'acris_document_control_codes': 123,
        'acris_property_type_codes': 46,
        'acris_ucc_collateral_codes': 8
    },
    'marshal_evictions': {
        'marshal_evictions_17': 17000,
        'marshal_evictions_18': 19000
    },
    'oath_hearings': {'oath_hearings': 10000000}
}


class colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def check_dataset(db, dataset):
    """ input: nycdb.Database, str """

    for table_name, min_row_count in TABLES[dataset].items():
        if db.table_exists(table_name):
            cnt = db.row_count(table_name)
            if cnt >= min_row_count:
                print(colors.GREEN + table_name + ' has ' + format(cnt, ',') + ' rows' + colors.ENDC)
            else:
                if cnt == 0:
                    print(colors.FAIL + table_name + ' has no rows!' + colors.ENDC)
                else:
                    has_rows = colors.FAIL + table_name + ' has ' + format(cnt, ',') + ' rows.' + colors.ENDC
                    expecting = colors.FAIL + 'Expecting at least ' + colors.BLUE + \
                        format(min_row_count, ',') + colors.ENDC + colors.FAIL + ' rows' + colors.ENDC
                    print(has_rows + expecting)
        else:
            print(colors.FAIL + table_name + ' is missing!' + colors.ENDC)
