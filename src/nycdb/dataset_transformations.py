from .transform import with_geo, with_bbl, to_csv, extract_csvs_from_zip, skip_fields
from .transform import hpd_registrations_address_cleanup, hpd_contacts_address_cleanup
from .dof_parser import parse_dof_file
from .datasets import datasets

def ecb_violations(dataset):
    return with_bbl(to_csv(dataset.files[0].dest), borough='boro')


def dob_violations(dataset):
    return with_bbl(to_csv(dataset.files[0].dest), borough='boro')


def _pluto(dataset):
    """
    Handles importing of all pluto versions,
    optionally allowing for skipped fields in some versions.
    It assumes there is only one schema for each pluto dataset.
    """
    pluto_generator = with_geo(to_csv(extract_csvs_from_zip(dataset.files[0].dest)))
    pluto_fields_to_skip = dataset.schemas[0].get('skip')

    if pluto_fields_to_skip:
        return skip_fields(pluto_generator, [s.lower() for s in pluto_fields_to_skip])

    return pluto_generator

# Creates a function for each pluto version
# same as doing def pluto_15v1() ... def pluto_16v2 ... etc
for pluto_version in filter(lambda x: x[0:5] == 'pluto', datasets().keys()):
    exec(f'''
def {pluto_version}(dataset):
    return _pluto(dataset)
''')

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

def j51_exemptions(dataset):
    return with_bbl(to_csv(dataset.files[0].dest), borough='boroughcode')


def marshal_evictions(dataset, schema):
    dest_file = next(filter(lambda f: schema['table_name'] in f.dest, dataset.files))
    _to_csv = to_csv(dest_file.dest)
    return _to_csv
