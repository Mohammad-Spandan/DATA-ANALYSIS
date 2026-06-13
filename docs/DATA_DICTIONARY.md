# Data Dictionary

## Overview

This document describes the structure and content of the agricultural crop data.

## Table: consolidated_crop_data.csv

### Columns

| Column Name | Data Type | Description | Unit | Example |
|------------|-----------|-------------|------|----------|
| **Crop_ID** | Integer | Unique identifier for each crop | N/A | 1 |
| **Year** | String | Agricultural year in format YYYY-YY | N/A | 2010-11 |
| **Crop_Name** | String | Name of the crop | N/A | Rice |
| **Crop_Category** | String | Category classification | N/A | Major Crops |
| **Area_000ac** | Float | Area under cultivation | 000 acres | 28489.0 |
| **Production** | Float | Total production output | Varies | 33542.0 |
| **Production_Unit** | String | Unit of production measurement | N/A | 000Mton |

## Crop Categories

### 1. Major Crops

Main staple and cash crops:
- Rice (ID: 1)
- Jute (ID: 2)
- Sugarcane (ID: 3)
- Tea (ID: 4)
- Pulses (ID: 5)
- Oilseeds (ID: 6)
- Condiments (ID: 7)
- Tobacco (ID: 8)

### 2. Cereals

Grain crops:
- Maize (ID: 9)
- Jowar (ID: 10)
- Barley (ID: 11)
- Bajra (ID: 12)

### 3. Pulses

Legume crops:
- Masur (ID: 13)
- Moong (ID: 14)
- Gram (ID: 15)
- Mashkalai (ID: 16)
- Arhar (ID: 17)

### 4. Condiments and Spices

- Chilies (ID: 18)
- Onion (ID: 19)
- Garlic (ID: 20)

### 5. Miscellaneous Cash Crops

- Potato (ID: 21)
- Sweet Potato (ID: 22)
- Betelnut (ID: 23)
- Cotton (ID: 24)
- Hemp (ID: 25)
- Mulberry (ID: 26)

## Production Units

| Unit | Meaning | Crops |
|------|---------|-------|
| 000Mton | 1000 Metric Tons | Rice, Wheat, Maize, etc. |
| 000Bales | 1000 Bales | Jute, Cotton, Hemp |
| 000lbs | 1000 Pounds | Tea |
| Tons | Metric Tons | Potato, Sweet Potato |
| Mton | Metric Tons | Various cash crops |

## Data Quality Notes

### Missing Values

- **Tea Production (2016-2024)**: Missing data for production column
- **Jowar, Bajra, and Barley**: Some years have gaps
- **Hemp and Mulberry**: Limited historical data

### Data Anomalies

1. **Jute Production Jump (2012-13)**: Production increased significantly from ~1500 to ~7600 (Unit: 000Bales)
2. **Tea Area Reduction (2016-17)**: Significant drop in area from 148 to 133 (000 acres)
3. **Chilies Production Anomaly (2020-21)**: Production jumped from 158 to 492 (000Mton)

### Recommended Data Cleaning

1. Validate Jute production jump with external sources
2. Investigate Tea missing production data
3. Standardize production units for better comparison
4. Fill missing values using interpolation or domain knowledge

## Derived Metrics

Common metrics calculated from raw data:

### Yield
```
Yield = Production / Area
```

### Growth Rate
```
Growth Rate = ((End Value - Start Value) / Start Value) * 100
```

### Compound Annual Growth Rate (CAGR)
```
CAGR = (((End Value / Start Value) ^ (1/Years)) - 1) * 100
```

## Time Coverage

- **Earliest Data**: 2007-08 (Maize, some Pulses)
- **Most Complete**: 2010-11 onwards
- **Latest Data**: 2023-24
- **Gaps**: 2017-18 missing for some crops, 2016-2019 for Tea production

## Related Documentation

- See [ANALYSIS_APPROACH.md](ANALYSIS_APPROACH.md) for analysis methodology
- See [README.md](../README.md) for project overview
