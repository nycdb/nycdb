from .transform import with_geo, with_bbl, to_csv, extract_csvs_from_zip, skip_fields
from .transform import hpd_registrations_address_cleanup, hpd_contacts_address_cleanup
from .dof_parser import parse_dof_file


def pluto_16v2(dataset):
    return with_geo(to_csv(extract_csvs_from_zip(dataset.files[0].dest)))


def pluto_17v1(dataset):
    return with_geo(to_csv(extract_csvs_from_zip(dataset.files[0].dest)))


def pluto_18v1(dataset):
    return with_geo(to_csv(extract_csvs_from_zip(dataset.files[0].dest)))


def hpd_complaints(dataset):
    return with_bbl(to_csv(dataset.files[0].dest))


def hpd_complaint_problems(dataset):
    return to_csv(dataset.files[1].dest)


def dob_complaints(dataset):
    return to_csv(dataset.files[0].dest)


def hpd_violations(dataset):
    return to_csv(dataset.files[0].dest)


def hpd_registrations(dataset):
    return hpd_registrations_address_cleanup(to_csv(dataset.files[0].dest))


def hpd_contacts(dataset):
    return hpd_contacts_address_cleanup(to_csv(dataset.files[1].dest))


def dof_sales(dataset):
    for f in dataset.files:
        for row in with_bbl(parse_dof_file(f.dest)):
            yield row


def dobjobs(dataset):
    return with_bbl(to_csv(dataset.files[0].dest))


def rentstab(dataset):
    return to_csv(dataset.files[0].dest)


def acris(dataset, schema):
    dest_file = next(filter(lambda f: schema['table_name'] in f.dest, dataset.files))
    _to_csv = to_csv(dest_file.dest)
    if 'skip' in schema:
        return skip_fields(_to_csv, [s.lower() for s in schema['skip']])
    else:
        return _to_csv
