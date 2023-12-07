TABLES = {
    'pluto_10v1': {'pluto_10v1': 800_000},
    'pluto_15v1': {'pluto_15v1': 800_000},
    'pluto_16v2': {'pluto_16v2': 800_000},
    'pluto_17v1': {'pluto_17v1': 800_000},
    'pluto_18v1': {'pluto_18v1': 800_000},
    'pluto_18v2': {'pluto_18v2': 800_000},
    'pluto_19v1': {'pluto_19v1': 800_000},
    'pluto_19v2': {'pluto_19v2': 800_000},
    'pluto_20v8': {'pluto_20v8': 800_000},
    'pluto_21v3': {'pluto_21v3': 800_000},
    'pluto_22v1': {'pluto_22v1': 800_000},
    'pluto_23v1': {'pluto_23v1': 800_000},
    'pluto_latest': {'pluto_latest': 800_000},
    'dobjobs': {
        'dobjobs': 1_000_000,
        'dob_now_jobs': 380_000
    },
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
    'hpd_hwo_charges': {'hpd_hwo_charges': 88_000},
    'hpd_omo': {'hpd_omo_charges': 400_000, 'hpd_omo_invoices': 650_000},
    'dof_421a': {'dof_421a': 275_000},
    'dof_sales': {'dof_sales': 60_000},
    'dof_annual_sales': { 'dof_annual_sales': 900_000 },
    'dof_exemptions': {
        'dof_exemptions': 740_000,
        'dof_exemption_classification_codes': 175
    },
    'rentstab': {'rentstab': 45_000},
    'rentstab_v2': {'rentstab_v2': 40_000},
    'rentstab_summary': {'rentstab_summary': 45_000},
    'dob_complaints': {'dob_complaints': 1_000_000},
    'hpd_complaints': {
        'hpd_complaints_and_problems': 13_000_000,
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
        'marshal_evictions_18': 19_000,
        'marshal_evictions_19': 16_000,
        'marshal_evictions_all': 55_000,
    },
    'nycha_bbls': {
        'nycha_bbls_18': 5_500,
    },
    'oath_hearings': {'oath_hearings': 10_000_000},
    'hpd_vacateorders': {'hpd_vacateorders': 4_000},
    'hpd_litigations': {'hpd_litigations': 170_000},
    'j51_exemptions': {'j51_exemptions': 4_000_000},
    'mci_applications':{'mci_applications': 25_000},
    'oca': {
        'oca_index': 1_300_000,
        'oca_causes': 1_300_000,
        'oca_addresses': 1_300_000,
        'oca_parties': 3_400_000,
        'oca_events': 2_500_000,
        'oca_appearances': 2_500_000,
        'oca_appearance_outcomes': 2_500_000,
        'oca_motions': 700_000,
        'oca_decisions': 650_000,
        'oca_judgments': 600_000,
        'oca_warrants': 600_000,
        'oca_metadata': 1_300_000,
    },
    'hpd_affordable_production': {
        'hpd_affordable_building': 6_000,
        'hpd_affordable_project': 3_400
    },
    'hpd_conh': {'hpd_conh': 1_000},
    'dcp_housingdb': {'dcp_housingdb': 70_000},
    'speculation_watch_list': { 'speculation_watch_list': 500 },
    'dob_certificate_occupancy': {'dob_certificate_occupancy': 138_000}
}


class colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def check_dataset(db, dataset):
    """ input: nycdb.Database, str """

    exit_state = True

    for table_name, min_row_count in TABLES[dataset].items():
        if db.table_exists(table_name):
            cnt = db.row_count(table_name)
            if cnt >= min_row_count:
                print(colors.GREEN + table_name + ' has ' + format(cnt, ',') + ' rows' + colors.ENDC)
            else:
                exit_state = False
                if cnt == 0:
                    print(colors.FAIL + table_name + ' has no rows!' + colors.ENDC)
                else:
                    has_rows = colors.FAIL + table_name + ' has ' + format(cnt, ',') + ' rows.' + colors.ENDC
                    expecting = colors.FAIL + 'Expecting at least ' + colors.BLUE + \
                        format(min_row_count, ',') + colors.ENDC + colors.FAIL + ' rows' + colors.ENDC
                    print(has_rows + expecting)
        else:
            exit_state = False
            print(colors.FAIL + table_name + ' is missing!' + colors.ENDC)

    return exit_state
