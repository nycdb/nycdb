## Adding a new dataset

This can be tricky depending on the dataset - some might require you to write code to clean and format the data properly. Others might not.

This guide will cover adding a dataset from NYC Open Data.

### Step 1 - find the raw `.csv` download url

We need to find a URL that will trigger an automatic download of the dataset when we visit it.

For the DOB ECB Violations (the dataset we're adding in this example), when you visit the [NY Open Data page](https://data.cityofnewyork.us/Housing-Development/DOB-ECB-Violations/6bgk-3dad) for this dataset, the url you get is:

`https://data.cityofnewyork.us/Housing-Development/DOB-ECB-Violations/6bgk-3dad`


Make note of the last part of this path - `6bgk-3dad` - this is the dataset's ID code.


The raw `.csv` download link for this the entire dataset is `https://data.cityofnewyork.us/api/views/6bgk-3dad/rows.csv?accessType=DOWNLOAD`.

Note how the code `6bgk-3dad` was included after the part of the url that says `views`.

For any other NY Open Data dataset, you'll need to use the link above but replace the dataset ID code with the correct one.


### Step 2 - tell NYCDB how to manage the files


Make a new file in `src/nycdb/datasets` called `ecb_violations.yml` and paste the following into it:

```yml
---
files:
  -
    url: https://data.cityofnewyork.us/api/views/6bgk-3dad/rows.csv?accessType=DOWNLOAD
    dest: ecb_violations.csv
```

The name of the file without its `.yml` extension is the name that `nycdb` commands like `nycdb --download` and `nycdb --load` will look for. Since we've called the file `ecb_violations.yml`, it means you can run commands like `nycdb --download ecb_violations`.

`url:` is where you put the download link.

`dest:` is where you name the file when it's downloaded. Try to name it after the name of your dataset if possible--in our example, for instance, our dataset is named `ecb_violations` and our `dest` is `ecb_violations.csv`.  This isn't required, but it's a nice convention that makes it easier to know what dataset a CSV is for when looking through one's downloads.

`nycdb` will automatically handle the downloading and saving of this file from here.


### Step 3 - tell NYCDB how to parse / understand the data


For the next part, you'll need to tell NYCDB what all of the columns are and what do they contain - do they contain text, numbers, dates? etc.

***********
Here's a list of the column types you can use:

`text` - for text of any length

`char(1)` - for 1 character text

`char(10)` - for 10 character text... etc

`date` - for date fields

`integer` - for non-decimal numbers less than `2,147,483,647`

`smallint` - for non-decimal numbers less than `32,767`

`bigint` - for non-decimal numbers less than `9,223,372,036,854,775,807`

`numeric` - for decimal numbers

`boolean` - for true/false values

In addition to these types, any valid postgresql type can be used. If the type includes whitespace, be sure to surround it with quotation marks. For example, the [`oca_appearances.appearancedatetime` column](./nycdb/datasets/oca.yml) has type `'timestamp without time zone'`

**************


#### ** NOTE **

You might have found a table in the NY Open Data portal [like this for example](https://data.cityofnewyork.us/Housing-Development/DOB-ECB-Violations/6bgk-3dad) that lists out the columns in the dataset and their data type. Even if a column says "Text" there, if the column can be parsed as a `date`, then `nycdb` *might* be smart enough to know how to convert this "text" into a "date". If you check in the `typecast.py` file, you can see from the "date" method that NYCDB can parse dates in a variety of formats (like "20000131" and "12/31/2018 12:00:00 AM", for example).

It's also **essential** to note that nycdb converts all column names found in the CSV to conventional, valid SQL column names, and the fields listed in your new `yml` file must match those names. The field-to-column name matching is case-insensitive, but we prefer `CamelCase` field names for readability.

Some examples of how column names are transformed:

- Characters like ` `, `_`, `-`, and `+`, among others, are removed from the column names found in the CSV. For example, the `VIOLATION_NUMBER` column from the [DOB Violations data source](https://data.cityofnewyork.us/Housing-Development/DOB-Violations/3h2n-5cm9) is renamed to [`ViolationNumber` in dob_violations.yml](./nycdb/datasets/dob_violations.yml).
- The charater `%` is replaced with `pct`. For example, the `% TRANSFERRED` column from the [ACRIS - Real Property Master data source](https://data.cityofnewyork.us/City-Government/ACRIS-Real-Property-Master/bnx9-e6tj) is renamed to [`PCTTRANSFERRED` in acris.yml](./nycdb/datasets/acris.yml).
- Columns that begin with a number in the CSV are rearranged so the number comes last. For example, the `1-BR Units` column from the [Affordable Housing Production by Building data source](https://data.cityofnewyork.us/Housing-Development/Affordable-Housing-Production-by-Building/hg8x-zxpr) is renamed to [`BRUnits1` in hpd_affordable_production.yml](./nycdb/datasets/hpd_affordable_production.yml).
- All these transformations are implemented in [transform.py](./nycdb/transform.py).

For this example, we'll fill out the rest of the `ecb_violations.yml` configuration.

```yml
---
files:
  -
    url: https://data.cityofnewyork.us/api/views/6bgk-3dad/rows.csv?accessType=DOWNLOAD
    dest: ecb_violations.csv
schema:
  table_name: ecb_violations
  fields:
    IsnDobBisExtract: text
    EcbViolationNumber: text
    EcbViolationStatus: text
    DobViolationNumber: text
    bin: char(7)
    boro: char(1)
    block: char(5)
    lot: char(4)
    bbl: char(10)
    HearingDate: date
    HearingTime: text
    ServedDate: date
    IssueDate: date
    severity: text
    ViolationType: text
    RespondentName: text
    RespondentHouseNumber: text
    RespondentStreet: text
    RespondentCity: text
    RespondentZip: char(5)
    ViolationDescription: text
    PenalityImposed: numeric # Yes, they misspelled "penalty"
    AmountPaid: numeric
    BalanceDue: numeric
    InfractionCode1: text
    SectionLawDescription1: text
    InfractionCode2: text
    SectionLawDescription2: text
    InfractionCode3: text
    SectionLawDescription3: text
    InfractionCode4: text
    SectionLawDescription4: text
    InfractionCode5: text
    SectionLawDescription5: text
    InfractionCode6: text
    SectionLawDescription6: text
    InfractionCode7: text
    SectionLawDescription7: text
    InfractionCode8: text
    SectionLawDescription8: text
    InfractionCode9: text
    SectionLawDescription9: text
    InfractionCode10: text
    SectionLawDescription10: text
    AggravatedLevel: text
    HearingStatus: text
    CertificationStatus: text
```

#### ** NOTE **

If the dataset does not include a `BBL` column, but has `boro` (or `borough`), `block`, and `lot` columns, you can add a `bbl` column in manually and we'll add use `nycdb` construct the value in the next step:

```diff
     AggravatedLevel: text
     HearingStatus: text
     CertificationStatus: text
+    bbl: char(10)
```

### Step 4 - apply custom transformations to the data

Each dataset needs a method defined in `dataset_transformations.py` (which shares the same name as the dataset).

For datasets requiring no transformation, the simplest version of this method looks like this:

```
def ecb_violations(dataset):
    return to_csv(dataset.files[0].dest)
```

If your dataset needs some custom transformation, such as adding the `bbl`, you can add that behavior here:

```
def ecb_violations(dataset):
    return with_bbl(to_csv(dataset.files[0].dest), borough='boro')
```


### Step 5 (optional) - add indexes to the database to speed up search

You can add raw SQL commands to the `--load` process by adding a file named `ecb_violations.sql` into the `sql` directory.

It's always helpful to add indexes to help speed up search.

For `ecb_violations`, we can add a couple unique and non-unique indexes on fields that may be heavily queried.

```sql
CREATE INDEX ecb_violations_bbl_idx on ecb_violations (bbl);
CREATE INDEX ecb_violation_type_idx on ecb_violations (ViolationType);
CREATE INDEX ecb_violations_dob_violation_number_idx on ecb_violations (DobViolationNumber);
CREATE UNIQUE INDEX ecb_violations_isndobbisviol_idx on ecb_violations (EcbViolationNumber);
```

At the very least, when in doubt, you should at least try adding
and index on your dataset's `bbl` column, since it's a field that
people will frequently want to join on.

In your `ecb_violations.yml` file, add a reference to the sql file to the end of the dataset object. (make sure it lines up with the `fields` and 'files' keys!)

```
sql:
  - ecb_violations.sql
```


### Step 6 - re-install nycdb to register the new dataset

> 🐳 When running via Docker, this step is handled automatically, so there's no need to do anything here.

- `pip uninstall nycdb`
- `pip setup.py install` (from inside of the `src` directory)


### Step 7 - verify

> 🐳 When running via docker, replace all the `nycdb` commands listed below with `docker-compose run nycdb` equivalents. For example, instead of running `nycdb --list`, run `docker-compose run nycdb --list`.

To see if your dataset registers:

- `nycdb --list`

Then download and load the dataset into your database. When that's done, query it or use a GUI tool like `dbeaver` to ensure that the data was loaded correctly.

- `nycdb --download ecb_violations`
- `nycdb --load ecb_violations`

You also need to add an estimated count of the # of rows into the file called `verify.py`

Count the number of rows that exist in your new dataset

With SQL, this is:
```
SELECT COUNT(*) FROM <dataset_table_name>
```

and then add a key to `verify.py` with a rounded number thats below the true count:

```
'ecb_violations': {'ecb_violations': 1300000},
```

Now, when you run the terminal command `nycdb --verify ecb_violations`, it should say your data is verified.


### Step 8 - write an integration test!

Integration tests are a way to ensure that all the code works without having to manually download and check everything (which would take hours!)

Find the file `test_nycdb.py` inside of `tests/integration` and look at this example for how to write a test here:

```
def test_hpd_complaint_problems(conn):
    drop_table(conn, 'hpd_complaint_problems')
    ecb_violations = nycdb.Dataset('ecb_violations', args=ARGS)
    ecb_violations.db_import()
    assert row_count(conn, 'ecb_violations') == 5
```

What this test does is insert a series of fake records into a testing database and then tests to see if all the rows were successfully inserted.

We need to create some fake data first! Go to `tests/integation/data` and create a file named after your dataset, or `ecb_violations.csv` in this case.

Then, in terminal, print a few lines from the data file you downloaded for this dataset_table_name
```
# This will print the headers and the first 5 rows of the CSV file.
head -6 data/ecb_violations.csv
```

Copy and paste the results from the terminal into the fake data file.

Run the test command:

```
pytest
```

> 🐳 When running via Docker, run the tests via `docker-compose run --entrypoint=pytest nycdb`

If it says all the tests passed, you passed! If it says a test failed, you'll have to debug.

#### Running a failing test faster

It might be the case that the new test you added is the only one that's failing.
If that's the case, you can re-run *only* that test via command-line options like this:

```
pytest tests/integration/test_nycdb.py -k test_hpd_complaint_problems
```

> 🐳 When running via Docker, run a specific test via `docker-compose run --entrypoint='pytest tests/integration/test_nycdb.py -k test_hpd_complaint_problems' nycdb`

This allows you to debug and iterate on your code faster.


### Step 9 - Update the documentation

Now just update [`README.md`](../README.md) to list your dataset in the list of datasets, so
future users know it's in NYCDB.


### Conclusion

This was an oversimplified guide for a complicated procedure and it may not cover every scenario you'll run into. Be sure to test your dataset after downloading and loading it to ensure that it appears the way you'd expect it to.
