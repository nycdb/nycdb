TABLES = {
    'pluto_15v1': {'pluto_15v1': 800_000},
    'pluto_16v2': {'pluto_16v2': 800_000},
    'pluto_17v1': {'pluto_17v1': 800_000},
    'pluto_18v1': {'pluto_18v1': 800_000},
    'pluto_18v2': {'pluto_18v2': 800_000},
    'dobjobs': {'dobjobs': 1_000_000},
    'dob_violations': {'dob_violations': 2_000_000},
    'ecb_violations': {'ecb_violations': 1_300_000},
    'hpd_violations': {'hpd_violations': 4_000_000},
    'hpd_registrations': {
        'hpd_registrations': 150_000,
        'hpd_contacts': 600_000,
        'hpd_corporate_owners': 30_000,
        'hpd_business_addresses': 130_000,
        'hpd_registrations_grouped_by_bbl': 130_000,
        'hpd_registrations_grouped_by_bbl_with_contacts': 130_000
    },
    'dof_sales': {'dof_sales': 75_000},
    'rentstab': {'rentstab': 45_000},
    'rentstab_summary': {'rentstab_summary': 45_000},
    'dob_complaints': {'dob_complaints': 1_000_000},
    'hpd_complaints': {
        'hpd_complaints': 1_000_000,
        'hpd_complaint_problems': 2_000_000
    },
    'pad': {'pad_adr': 1000000},
    'acris': {
        'real_property_remarks': 1_000_000,
        'real_property_legals': 1_000_000,
        'real_property_master': 1_000_000,
        'real_property_parties': 1_000_000,
        'real_property_references': 1_000_000,
        'personal_property_legals': 1_000_000,
        'personal_property_master': 1_000_000,
        'personal_property_parties': 1_000_000,
        'personal_property_references': 1_000_000,
        'personal_property_remarks': 400_000,
        'acris_country_codes': 250,
        'acris_document_control_codes': 123,
        'acris_property_type_codes': 46,
        'acris_ucc_collateral_codes': 8
    },
    'marshal_evictions': {
        'marshal_evictions_17': 17_000,
        'marshal_evictions_18': 19_000
    },
    'oath_hearings': {'oath_hearings': 10_000_000}
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
