"""
Each function in this file is the name of a table or dataset.
"""
import logging
import itertools

from .transform import with_bbl, to_csv, stream_files_from_zip, extract_csv_from_zip, skip_fields
from .transform import hpd_registrations_address_cleanup, hpd_contacts_address_cleanup
from .datasets import datasets
from .annual_sales import AnnualSales
from .dof_421a import iter_421a

def ecb_violations(dataset):
    return with_bbl(to_csv(dataset.files[0].dest), borough='boro')


def dob_violations(dataset):
    return with_bbl(to_csv(dataset.files[0].dest), borough='boro')


def dof_exemption_classification_codes(dataset):
    return to_csv(dataset.files[0].dest)


def dof_exemptions(dataset):
    return with_bbl(to_csv(dataset.files[1].dest), borough='boro')


def _pluto(dataset):
    """
    Handles importing of all pluto versions,
    optionally allowing for skipped fields in some versions.
    It assumes there is only one schema for each pluto dataset.
    """
    extension = 'txt' if dataset.name == 'pluto_10v1' else 'csv'

    if dataset.name == 'pluto_latest':
        pluto_generator = to_csv(dataset.files[0].dest)
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


def hpd_complaints(dataset):
    return with_bbl(to_csv(dataset.files[1].dest))


def hpd_complaint_problems(dataset):
    return to_csv(dataset.files[2].dest)


def dob_complaints(dataset):
    return to_csv(dataset.files[0].dest)


def hpd_violations(dataset):
    return to_csv(dataset.files[0].dest)


def hpd_registrations(dataset):
    return hpd_registrations_address_cleanup(to_csv(dataset.files[0].dest))


def hpd_contacts(dataset):
    return hpd_contacts_address_cleanup(to_csv(dataset.files[1].dest))


def dof_sales(dataset):
    return with_bbl(to_csv(dataset.files[0].dest))


def dobjobs(dataset):
    return with_bbl(to_csv(dataset.files[0].dest))


def dob_now_jobs(dataset):
    return with_bbl(skip_fields(to_csv(dataset.files[1].dest), [s.lower() for s in dataset.schemas[1]['skip']]))

def rentstab(dataset):
    return to_csv(dataset.files[0].dest)


def rentstab_v2(dataset):
    return to_csv(dataset.files[0].dest)


def rentstab_summary(dataset):
    return to_csv(dataset.files[0].dest)


def acris(dataset, schema):
    dest_file = next(filter(lambda f: schema['table_name'] in f.dest, dataset.files))
    _to_csv = to_csv(dest_file.dest)
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
    return with_bbl(to_csv(dataset.files[0].dest), borough='boroughcode')


def marshal_evictions(dataset, schema):
    dest_file = next(filter(lambda f: schema['table_name'] in f.dest, dataset.files))
    _to_csv = to_csv(dest_file.dest)
    if 'skip' in schema:
        return skip_fields(_to_csv, [s.lower() for s in schema['skip']])
    else:
        return _to_csv


def nycha_bbls(dataset, schema):
    dest_file = next(filter(lambda f: schema['table_name'] in f.dest, dataset.files))
    _to_csv_with_bbl = with_bbl(to_csv(dest_file.dest))
    return _to_csv_with_bbl


def hpd_litigations(dataset):
    return to_csv(dataset.files[0].dest)


def hpd_vacateorders(dataset):
    return to_csv(dataset.files[0].dest)


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
    return skip_fields(to_csv(dataset.files[0].dest), [s.lower() for s in dataset.dataset['schema']['skip']]);


def hpd_affordable_building(dataset):
    return to_csv(dataset.files[0].dest)


def hpd_affordable_project(dataset):
    return to_csv(dataset.files[1].dest)


def hpd_conh(dataset):
    return to_csv(dataset.files[0].dest)


def dcp_housingdb(dataset):
    return to_csv(extract_csv_from_zip(dataset.files[0].dest, "HousingDB_post2010.csv"))


def dob_vacate_orders(dataset):
    return with_bbl(to_csv(dataset.files[0].dest), borough='boroughname')


def dof_tax_lien_sale_list(dataset):
    return with_bbl(to_csv(dataset.files[0].dest))


def dob_certificate_occupancy(dataset):
    return with_bbl(skip_fields(to_csv(dataset.files[0].dest), [s.lower() for s in dataset.dataset['schema']['skip']]))


def hpd_hwo_charges(dataset):
    return to_csv(dataset.files[0].dest)


def hpd_omo_invoices(dataset):
    return to_csv(dataset.files[0].dest)


def hpd_omo_charges(dataset):
    return to_csv(dataset.files[1].dest)
