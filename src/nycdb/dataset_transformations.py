"""
Each function in this file is the name of a table or dataset.
"""
import logging
import itertools

from .transform import with_bbl, to_csv, stream_files_from_zip, extract_csv_from_zip, skip_fields, iso_dates_to_text
from .transform import hpd_registrations_address_cleanup, hpd_contacts_address_cleanup
from .datasets import datasets
from .annual_sales import AnnualSales
from .dof_421a import iter_421a
from .utility import merge

def ecb_violations(dataset):
    return with_bbl(to_csv(dataset.files[0].dest), borough='boro')


def dob_violations(dataset):
    return with_bbl(to_csv(dataset.files[0].dest), borough='boro')


def dof_exemption_classification_codes(dataset):
    return to_csv(dataset.files[0].dest)


def dof_exemptions(dataset):
    return with_bbl(to_csv(dataset.files[1].dest), borough='boro')

def dof_property_valuation_and_assessments(dataset):
    return with_bbl(to_csv(dataset.files[0].dest), borough='boro')

def _pluto(dataset):
    """
    Handles importing of all pluto versions,
    optionally allowing for skipped fields in some versions.
    It assumes there is only one schema for each pluto dataset.
    """
    extension = 'txt' if dataset.name == 'pluto_10v1' else 'csv'

    if dataset.name == 'pluto_latest':
        pluto_generator = to_csv(dataset.files[0].dest, header_replacements={
            "taxblock": "block",
            "taxlot": "lot",
            "cd": "communityboard",
            "ct2010": "censustract2010",
            "council": "councildistrict",
            "zipcode": "postcode",
        })
    else:
        pluto_generator = to_csv(stream_files_from_zip(dataset.files[0].dest, extension=extension))

    pluto_fields_to_skip = dataset.schemas[0].get('skip')

    if pluto_fields_to_skip:
        pluto_generator = skip_fields(pluto_generator, [s.lower() for s in pluto_fields_to_skip])

    for line in pluto_generator:
        if line['borough'] is None or line['block'] is None or line['lot'] is None:
          logging.info("skipping pluto row without bbl: {}".format(line))
        else:
          yield line


# Creates a function for each pluto version
# same as doing def pluto_15v1() ... def pluto_16v2 ... etc
for pluto_version in filter(lambda x: x[0:5] == 'pluto', datasets().keys()):
    exec(f'''
def {pluto_version}(dataset):
    return _pluto(dataset)
''')


def hpd_complaints_and_problems(dataset):
    return to_csv(dataset.files[0].dest)


def dob_complaints(dataset):
    return to_csv(dataset.files[0].dest)


def hpd_violations(dataset):
    return to_csv(dataset.files[0].dest, header_replacements={'boro': 'borough', 'zip': 'postcode'})


def hpd_registrations(dataset):
    return hpd_registrations_address_cleanup(to_csv(dataset.files[0].dest))


def hpd_contacts(dataset):
    return hpd_contacts_address_cleanup(to_csv(dataset.files[1].dest))


def dof_sales(dataset):
    return with_bbl(to_csv(dataset.files[0].dest, header_replacements={'buildingclassattimeof': 'buildingclassattimeofsale'}))


def dobjobs(dataset):
    header_replacements = {
        'gislatitude': 'latitude',
        'gislongitude': 'longitude',
        'giscouncildistrict': 'councildistrict',
        'giscensustract': 'censustract',
        'gisntaname': 'nta',
    }
    return with_bbl(to_csv(dataset.files[0].dest, header_replacements=header_replacements))


def dob_now_jobs(dataset):
    header_replacements = {
        'city': 'applicantcity',
        'state': 'applicantstate',
        'zip': 'applicantzip',
        'standpipe': 'standpipeworktype',
        'antenna': 'antennaworktype',
        'sign': 'signworktype',
        'curbcut': 'curbcutworktype',
        'fence': 'fenceworktype',
        'scaffold': 'scaffoldworktype',
        'shed': 'shedworktype',
    }
    return with_bbl(skip_fields(to_csv(dataset.files[1].dest, header_replacements=header_replacements), [s.lower() for s in dataset.schemas[1]['skip']]))

def rentstab(dataset):
    return to_csv(dataset.files[0].dest)


def rentstab_v2(dataset):
    return to_csv(dataset.files[0].dest)


def rentstab_summary(dataset):
    return to_csv(dataset.files[0].dest)


# NYC Open Data's query.csv export names some ACRIS columns differently
# from the display names that the table columns are based on.
ACRIS_HEADER_REPLACEMENTS = {
    'real_property_master': {
        'recordedborough': 'borough',
        'documentdate': 'docdate',
        'documentamt': 'docamount',
        'recordeddatetime': 'recordedfiled',
        'reelyr': 'reelyear',
        'reelpg': 'reelpage',
        'percenttrans': 'pcttransferred',
    },
    'real_property_remarks': {'sequencenumber': 'remarklinenbr', 'remarktext': 'remarktextline'},
    'personal_property_legals': {'addrunit': 'unit'},
    'personal_property_master': {
        'recordedborough': 'borough',
        'documentamt': 'docamount',
        'recordeddatetime': 'recordedfiled',
        'ucccollateral': 'collateral',
        'fedtaxserialnbr': 'slid',
        'fedtaxassessmentdate': 'assessmentdate',
        'rpttlnbr': 'rptt',
        'reelyr': 'reelyear',
        'reelpg': 'reelpage',
        'filenbr': 'filenumber',
    },
    'personal_property_references': {
        'crfn': 'referencebycrfn',
        'docidref': 'referencebydocid',
        'filenbr': 'referencebyfilenbr',
    },
    'personal_property_remarks': {'sequencenumber': 'remarklinenbr', 'remarktext': 'remarktextline'},
}


def acris(dataset, schema):
    dest_file = next(filter(lambda f: schema['table_name'] in f.dest, dataset.files))
    _to_csv = to_csv(dest_file.dest, header_replacements=ACRIS_HEADER_REPLACEMENTS.get(schema['table_name'], {}))
    if 'skip' in schema:
        return skip_fields(_to_csv, [s.lower() for s in schema['skip']])
    else:
        return _to_csv


def oath_hearings(dataset):
    return with_bbl(to_csv(dataset.files[0].dest),
                    borough='violationlocationborough',
                    block='violationlocationblockno',
                    lot='violationlocationlotno')


def pad_adr(dataset):
    pad_generator = with_bbl(to_csv(extract_csv_from_zip(
        dataset.files[0].dest, 'bobaadr.txt')), borough='boro')

    pad_fields_to_skip = dataset.schemas[0].get('skip')

    return skip_fields(pad_generator, [s.lower() for s in pad_fields_to_skip])


def j51_exemptions(dataset):
    return with_bbl(to_csv(dataset.files[0].dest, header_replacements={'b': 'boroughcode', 'e': 'easement'}), borough='boroughcode')


def marshal_evictions(dataset, schema):
    dest_file = next(filter(lambda f: schema['table_name'] in f.dest, dataset.files))
    _to_csv = to_csv(dest_file.dest)
    if 'skip' in schema:
        return skip_fields(_to_csv, [s.lower() for s in schema['skip']])
    else:
        return _to_csv

def nycha_bbls_18(dataset):
    return  with_bbl(to_csv(dataset.files[0].dest))

def nycha_bbls_24(dataset):
    return  with_bbl(to_csv(dataset.files[1].dest))


def hpd_litigations(dataset):
    return to_csv(dataset.files[0].dest, header_replacements={'boroid': 'boro', 'casejudgement': 'openjudgement'})


def hpd_vacateorders(dataset):
    header_replacements = {
        'boroshortname': 'borough',
        'housenumber': 'number',
        'streetname': 'street',
        'actualrescinddate': 'rescinddate',
        'postoce': 'postcode',
    }
    return to_csv(dataset.files[0].dest, header_replacements=header_replacements)


def oca(dataset, schema):
    dest_file = next(filter(lambda f: schema['table_name'] in f.dest, dataset.files))
    _to_csv = to_csv(dest_file.dest)
    return _to_csv


def mci_applications(dataset):
    return skip_fields(to_csv(dataset.files[0].dest), [s.lower() for s in dataset.dataset['schema']['skip']])


def dof_annual_sales(dataset):
    return itertools.chain(*[with_bbl(AnnualSales(f.dest)) for f in dataset.files])


def dof_421a(dataset):
    return itertools.chain(*[with_bbl(iter_421a(f.dest)) for f in dataset.files])


def speculation_watch_list(dataset):
    headers_to_replace = {
        "censustract2020from2023": "censustract2020",
        "neighborhoodtabulationareanta2020from2023": "nta2020",
        "censustract": "censustract2020",
        "nta": "nta2020",
        "geocodedcolumn": "location1",
    }
    fields_to_skip = [s.lower() for s in dataset.dataset["schema"]["skip"]]
    return skip_fields(
        to_csv(dataset.files[0].dest, header_replacements=headers_to_replace),
        fields_to_skip,
    )


def hpd_affordable_building(dataset):
    header_replacements = {
        'housenumber': 'number',
        'streetname': 'street',
        'neighborhoodtabulationarea': 'ntaneighborhoodtabulationarea',
        'extendedaffordabilitystatus': 'extendedaffordabilityonly',
    }
    return to_csv(dataset.files[0].dest, header_replacements=header_replacements)


def hpd_affordable_project(dataset):
    header_replacements = {
        'extendedaffordabilitystatus': 'extendedaffordabilityonly',
        'verylowincome': 'verylowincomeunits',
        'moderateincome': 'moderateincomeunits',
        'middleincome': 'middleincomeunits',
        'other': 'otherincomeunits',
    }
    return to_csv(dataset.files[1].dest, header_replacements=header_replacements)


def hpd_conh(dataset):
    header_replacements = {
        "neighborhoodtabulationareanta2020": "nta",
        "aeporder": "dischargedaep",
        "zipcode": "postcode",
        "censustract": "censustract2020",
        "ntaneighborhoodtabulation": "nta",
    }
    return to_csv(dataset.files[0].dest, header_replacements=header_replacements)


def dcp_housingdb(dataset):
    return to_csv(extract_csv_from_zip(dataset.files[0].dest, "HousingDB_post2010_inactive_included.csv"))


def dob_vacate_orders(dataset):
    return with_bbl(to_csv(dataset.files[0].dest), borough='boroughname')


def dof_tax_lien_sale_list(dataset):
    return with_bbl(iso_dates_to_text(to_csv(dataset.files[0].dest), ['month'], '%m/%Y'))


def dob_certificate_occupancy(dataset):
    fields_to_skip = [s.lower() for s in dataset.schemas[0].get('skip')]
    return with_bbl(skip_fields(to_csv(dataset.files[0].dest, header_replacements={'housenumber': 'number', 'streetname': 'street'}), fields_to_skip))

def dob_foil_certificate_occupancy(dataset):
    header_replacements = {
        "apjobnumber": "jobnumber",
        "jjobtype": "jobtype",
        "apaissuedate": "issuedate",
        "jbinnumber": "bin",
        "jhousenumber": "housenumber",
        "jstreetname": "streetname",
        "jblock": "block",
        "jlot": "lot",
        "jzip5": "zip5",
        "jprdwellingunits": "prdwellingunits",
        "jexdwellingunits": "exdwellingunits",
        "apaapplicationstatus": "applicationstatus",
        "apafilingstatus": "filingstatus",
        "apitemnumber": "itemnumber",
        "apaissuetype": "issuetype",
        "jactivestatus": "activestatus",
        "jjobdocumentnumber": "jobdocumentnumber"
    }
    fields_to_skip = [s.lower() for s in dataset.schemas[1].get('skip')]
    return skip_fields(to_csv(dataset.files[1].dest, header_replacements=header_replacements), fields_to_skip)

def dob_now_certificate_occupancy(dataset):
    fields_to_skip = [s.lower() for s in dataset.schemas[2].get('skip')]
    header_replacements = {
        'citycouncildistrict': 'councildistrict',
        'censustract2010': 'censustract',
        'ntaname': 'nta',
    }
    return skip_fields(to_csv(dataset.files[2].dest, header_replacements=header_replacements), fields_to_skip)


def hpd_hwo_charges(dataset):
    return to_csv(dataset.files[0].dest)


def hpd_omo_charges(dataset):
    return to_csv(dataset.files[1].dest)


def hpd_omo_invoices(dataset):
    return to_csv(dataset.files[2].dest)


def hpd_fee_charges(dataset):
    return to_csv(dataset.files[3].dest)


def dob_safety_violations(dataset):
    return with_bbl(to_csv(dataset.files[0].dest, header_replacements={'zip': 'postcode'}), borough='borough')


def dhs_daily_shelter_count(dataset):
    return to_csv(dataset.files[0].dest, header_replacements={'table': 'series_name'})


def dohmh_rodent_inspections(dataset):
    return with_bbl(
        skip_fields(
            to_csv(dataset.files[0].dest, header_replacements={'jobid': 'jobidcaseid'}),
            [s.lower() for s in dataset.dataset["schema"]["skip"]],
        ),
        borough="borocode",
    )


def hpd_aep(dataset):
    header_replacements = {
        'ofbcviolationsatstart': 'bcviolationsatstart',
        'boro': 'borough',
        'phn': 'number',
        'streetaddress': 'street',
    }
    return to_csv(dataset.files[0].dest, header_replacements=header_replacements)


def hpd_underlying_conditions(dataset):
    header_replacements = {
        'phn': 'numberphn',
        'streetname': 'street',
        'censustract': 'censustract2020',
        'nta': 'nta2020',
    }
    return iso_dates_to_text(to_csv(dataset.files[0].dest, header_replacements=header_replacements), ['orderissuedate'])

def hpd_ll44_buildings(dataset):
    return to_csv(dataset.files[0].dest, header_replacements={'boroid': 'borough', 'communityboardcb': 'communityboard'})

def hpd_ll44_projects(dataset):
    return to_csv(dataset.files[1].dest, header_replacements={'programname': 'programgroup'})

def hpd_ll44_tax_incentive(dataset):
    return to_csv(dataset.files[2].dest)


def fc_shd_building(dataset):
    return to_csv(dataset.files[0].dest)

def fc_shd_subsidy(dataset):
    return to_csv(dataset.files[1].dest)

def dos_active_corporations(dataset):
    header_replacements = {
        'chairmanname': 'ceoname',
        'chairmanaddress1': 'ceoaddress1',
        'chairmanaddress2': 'ceoaddress2',
        'chairmancity': 'ceocity',
        'chairmanstate': 'ceostate',
        'chairmanzip': 'ceozip',
    }
    return to_csv(dataset.files[0].dest, header_replacements=header_replacements)


def executed_evictions(dataset):
    header_replacements = {
        'evictionaptnum': 'evictionapartmentnumber',
        'residentialcommercialind': 'residentialcommercial',
        'evictionzip': 'evictionpostcode',
        'evictionpossession': 'evictionlegalpossession',
    }
    return to_csv(dataset.files[0].dest, header_replacements=header_replacements)


def hpd_jurisdiction(dataset):
    return with_bbl(to_csv(dataset.files[0].dest), borough='boroid')


def dof_property_charges_balance(dataset):
    for row in to_csv(dataset.files[0].dest):
        parid = row.get('parid') or ''
        yield merge(row, {'bbl': parid[:10]})
