# 0.2.4
- `HarvestRecord.key_value_list_to_dict(name_key: str)` default changed from `Name` to `Key`
- Expanded [README](./README.md) with documentation on callable `HarvestRecord` and `HarvestRecordSet` methods used for `RecordsetTask`
- Renamed `RecordsetTask` to `HarvestRecordSetTask`

# 0.2.3
- Updated to conform with CloudHarvestCorePluginManager 0.2.4

# 0.2.2
- HarvestRecord now attaches its HarvestRecordSet when the `add()` method is called
- `HarvestRecordSet.add()` is now recursive
- Renamed `RecordSetTask` to `RecordsetTask`
- Added new tests for `RecordsetTask`

# 0.2.1
- Updated to conform with CloudHarvestCorePluginManager 0.2.0
  - Implemented `@register_definition` decorator for RecordSetTask
  - Added `__register__.py`
- Added this CHANGELOG
