# Harvest Core Data Model
The CDM is responsible for converting parameters into data manipulation instructions the API, CLI, or Data Collectors can interpret.

## Table of Contents
- [Harvest Core Data Model](#harvest-core-data-model)
- [Usage](#usage)
- [License](#license)

# Usage
The most direct example of this is record matching using the CLI:
```
[] report rds.clusters -m Account=dev
```
Where `-m Account=dev` is a field (`Account`), comparison operator (`=`), and value (`dev`) which needs conversion. Matching logic may be converted into MongoDb query syntax or applied to locally-furnished data, depending on underlying commands.

# License
Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

