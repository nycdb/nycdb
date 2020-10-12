# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Add am/pm support for `time()`, add new `timestamp()` ([#133](nycdb/nycdb/pull/133))
- Add OCA (housing court) data ([#129](nycdb/nycdb/pull/129))
### Changed
- Change all BIN (building identification number) columns to `char(7)` ([#140](nycdb/nycdb/pull/140))
- Update rentstab_v2 table to include new 2019 unit counts ([#138]nycdb/nycdb/pull/138)

## [0.1.28] - 2020-03-30
### Added
- Added 2018 rentstab data ([#126](nycdb/nycdb/pull/126))
- Added 2019 Marshal Evictions data ([#124](nycdb/nycdb/pull/125))
- Added schema for pluto19v2 ([#120](nycdb/nycdb/pull/120))
### Removed
- Removed superfluous fields from marshal evictons 19 yml ([#125](nycdb/nycdb/pull/125))
### Changed
- Fixes to docker-compose ([#123](nycdb/nycdb/pull/123))