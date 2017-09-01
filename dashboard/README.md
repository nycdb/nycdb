# Community District Dashboard

A static site with housing statistics for each community district.

## Developer setup:

- Ensure there is a running version of NYCDB (see the main README for instructions)

- Install node modules: ``` npm install ```

- Build the site: ``` make ```

- View the site: ``` npm start ```

Requirements:
  - postgres
  - nodejs > 8

### Included information:

**basic stats**:

- lots
- residential units

**HPD violations**:

- number buildings with violations
- percentage of buildings with violations
- total number of violations
- violations per residential unit

**DOF sales**:

- top 10 highest priced residential sales

**DOB Dobs**:

- recent new building permits

**HPD Registrations (FORTHCOMING)**:

- largest corporate landlords

