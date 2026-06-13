# Raw Data Directory

This directory contains raw, unprocessed data files.

## Files

### consolidated_crop_data.csv

Main agricultural crop dataset containing production and area data for 26 crops across multiple years.

**Columns**:
- Crop_ID: Unique crop identifier
- Year: Agricultural year (YYYY-YY format)
- Crop_Name: Name of the crop
- Crop_Category: Category classification
- Area_000ac: Cultivated area (000 acres)
- Production: Production volume
- Production_Unit: Unit of measurement

**Data Quality Notes**:
- Some production values missing for Tea (2016-2024)
- Minor gaps in cereals data for some years
- Different production units used for different crops

## Database Schema

See `database_schema.sql` in the project root for database structure.

## Usage

To load this data:

```python
from src.data_loader import CropDataLoader

loader = CropDataLoader()
df = loader.load_data('data/raw/consolidated_crop_data.csv')
```

## Notes

- Do not modify files in this directory
- Keep backup copies of original data
- Document any data quality issues found
