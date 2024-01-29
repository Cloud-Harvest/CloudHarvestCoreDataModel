# Harvest Core Data Model
The CDM is responsible for converting parameters into data manipulation instructions the API, CLI, or Data Collectors can interpret. This module is not intended as a standalone resource; rather, a git submodule.

The most direct example of this is record matching using the CLI:
```
[] report rds.clusters -m Account=dev
```
Where `-m Account=dev` is a field (`Account`), comparison operator (`=`), and value (`dev`) which needs conversion. Matching logic may be converted into MongoDb query syntax or applied to locally-furnished data, depending on underlying commands.
