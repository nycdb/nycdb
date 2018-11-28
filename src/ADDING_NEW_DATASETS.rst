## Adding a new dataset

This can be tricky depending on the dataset - some might require you to write code to clean and format the data properly. Others might not.

This guide will cover adding a dataset from NYC Open Data.

#### Step 1 - find the raw `.csv` download url


For the DOB ECB Violations (the dataset we're adding in this example), when you visit the [NY Open Data page](https://data.cityofnewyork.us/Housing-Development/DOB-ECB-Violations/6bgk-3dad) for this dataset, the url you get is:

`https://data.cityofnewyork.us/Housing-Development/DOB-ECB-Violations/6bgk-3dad`


Make note of the last part of this path - `6bgk-3dad` - this is the dataset's ID code


The raw `.csv` download link for this the entire dataset is `https://data.cityofnewyork.us/api/views/6bgk-3dad/rows.csv?accessType=DOWNLOAD`

Note how the code `6bgk-3dad` was included after the part of the url that says `views`

This link will automatically initiate a download of the entire dataset, which is what NYCDB needs. Other URLs may only give you 1000 lines at a time or not initiate a download.


For any other NY Open Data dataset, you'll need to use the link above but replace the dataset ID code with the correct one.


#### Step 2 - tell NYCDB how to manage the files


Go to `datasets.yml` in `nycdb`


At the top of the file, add your new dataset following the strict formatting of the other datasets as an example.

```yml
ecb_violations:
  files:
    -
      url: https://data.cityofnewyork.us/api/views/6bgk-3dad/rows.csv?accessType=DOWNLOAD
      dest: ecb_violations.csv
```

The first line is where you name your dataset - this is the name that `nycdb` commands like `nycdb --download` and `nycdb --load` will look for. This configuration will allow you to run commands like `nycdb --download ecb_violations`

`url:` is where you put the download link

`dest:` is where you name the file when it's downloaded

`nycdb` will automatically handle the downloading and saving of this file from here.


#### Step 3 - tell NYCDB how to parse / understand the data


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

**************


** NOTE **

You might have found a table in the NY Open Data portal [like this for example](https://data.cityofnewyork.us/Housing-Development/DOB-ECB-Violations/6bgk-3dad) that lists of the columns in the dataset and their data type. Even if a column says "Text" here, if the column can be parsed as a `date`, then `nycdb` *might* by smart enough to know how to convert this "text" into a "date". I know this is vague, but if you check in the `typecast.py` file, you might be able to see how `nycdb` formats the different column types you define in this `.yml` file.

It's also *essential* to note that while columns might appear `snake_cased` in the open data portal, you need to convert these column names to `PascalCase` in the `datasets.yml` file.

For this example, we'll fill out the rest of the `datasets.yml` configuration for `ecb_violations`

```yml
ecb_violations:
  files:
    -
      url: https://data.cityofnewyork.us/api/views/6bgk-3dad/rows.csv?accessType=DOWNLOAD
      dest: ecb_violations.csv
  schema:
    table_name: ecb_violations
    fields:
      isn_dob_bis_extract: text
      ecb_violation_number: text
      ecb_violation_number: text
      dob_violation_number: text
      bin: text
      boro: char(1)
      block: char(5)
      lot: char(4)
      bbl: char(10)
      hearing_date: date
      hearing_time: text
      served_date: date
      issue_date: date
      severity: text
      violation_type: text
      respondent_name: text
      respondent_house_number: text
      respondent_street: text
      respondent_city: text
      respondent_zip: char(5)
      violation_description: text
      penality_imposed: numeric # yes, 'penality' - the typo is theirs
      amount_paid: numeric
      balance_due: numeric
      infraction_code1: text
      section_law_description1: text
      infraction_code2: text
      section_law_description2: text
      infraction_code3: text
      section_law_description3: text
      infraction_code4: text
      section_law_description4: text
      infraction_code5: text
      section_law_description5: text
      infraction_code6: text
      section_law_description6: text
      infraction_code7: text
      section_law_description7: text
      infraction_code8: text
      section_law_description8: text
      infraction_code9: text
      section_law_description9: text
      infraction_code10: text
      section_law_description10: text
      aggravated_level: text
      hearing_status: text
      certification_status: text
```

** NOTE **

If the dataset does not include a `BBL` column, but has `boro` (or `borough`), `block`, and `lot` columns, you can add a `bbl` column in manually and we'll add use `nycdb` construct the value in the next step.


#### Step 4 - apply custom transformations to the data

Each dataset needs a method defined in `dataset_transformations.py` (which shares the same name as the dataset).

With this method, you can add custom transformations, such as adding the `bbl` (see the `to_bbl` method below).


```
def ecb_violations(dataset):
    return with_bbl(to_csv(dataset.files[0].dest), borough='boro')
```

#### Step 5 (optional) - add indexes to the database to speed up search

You can add raw SQL commands to the `--load` process by adding a file named `ecb_violations.sql` into the `sql` directory.

It's always helpful to add indexes to help speed up search.


In mine, I added a couple unique and non-unique indexes on fields that may be heavily queried.

```sql
CREATE INDEX ecb_violations_bbl_idx on ecb_violations (bbl);
CREATE INDEX ecb_violation_type_idx on ecb_violations (ViolationType);
CREATE INDEX ecb_violations_dob_violation_number_idx on ecb_violations (DobViolationNumber);
CREATE UNIQUE INDEX ecb_violations_isndobbisviol_idx on ecb_violations (EcbViolationNumber);
```


In your `datasets.yml` file, add a reference to the sql file to the end of the dataset object. (make sure it lines up with the `fields` and 'files' keys!)
```
sql:
  - ecb_violations.sql
```


#### Step 6 - re-install nycdb to register the new dataset

- `pip uninstall nycdb`
- `pip setup.py install` (from inside of the `src` directory)


#### Step 7 - test

To see if your dataset registers:

- `nycdb --list`

Then download and load the dataset into your database. When that's done, query it or use a GUI tool like `dbeaver` to ensure that the data was loaded correctly.

- `nycdb --download ecb_violations`
- `nycdb --load ecb_violations`


#### Conclusion

This was an oversimplified guide to adding datasets and it may not cover every scenario you'll run into. Be sure to test your dataset after downloading and loading it to ensure that it appears the way you'd expect it to.
