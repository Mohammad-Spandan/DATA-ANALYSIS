# Agricultural Crop Data Analysis

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This project is a comprehensive data analysis platform for agricultural crop production, covering 26 crop varieties across 5 categories (Major Crops, Cereals, Pulses, Condiments & Spices, and Miscellaneous Cash Crops). It analyzes production trends, area utilization, and yield patterns from 2007 to 2024.

**Project Focus**: Transform raw agricultural data into actionable insights through exploratory data analysis, statistical modeling, and comprehensive visualization.

## Features

✅ **Data Pipeline**: Automated data loading, validation, and cleaning
✅ **Exploratory Data Analysis (EDA)**: Comprehensive statistical summaries and distribution analysis
✅ **Time Series Analysis**: Production and area trends with growth rate calculations
✅ **Visualization Suite**: Interactive and static charts for stakeholder communication
✅ **Quality Assurance**: Unit tests and data validation checks
✅ **Reproducibility**: Jupyter notebooks documenting the full analysis workflow
✅ **Scalability**: Modular architecture for easy extension

## Dataset

**Source**: `data/raw/consolidated_crop_data.csv`

**Coverage**:
- **Time Period**: 2007-2024 (with gaps)
- **Crops Analyzed**: 26 varieties
- **Categories**: 
  - Major Crops (Rice, Jute, Sugarcane, Tea, Pulses, Oilseeds, Condiments, Tobacco)
  - Cereals (Maize, Jowar, Barley, Bajra)
  - Pulses (Masur, Moong, Gram, Mashkalai, Arhar)
  - Condiments & Spices (Chilies, Onion, Garlic)
  - Miscellaneous Cash Crops (Potato, Sweet Potato, Betelnut, Cotton, Hemp, Mulberry)

**Key Metrics**:
- Area planted (in 000 acres)
- Production volume (varies by crop)
- Production unit (Mton, Bales, Tons, lbs)

For detailed data dictionary, see [docs/DATA_DICTIONARY.md](docs/DATA_DICTIONARY.md)

## Installation

### Prerequisites
- Python 3.8 or higher
- pip or conda
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mohammad-Spandan/DATA-ANALYSIS.git
   cd DATA-ANALYSIS
   ```

2. **Create a virtual environment**
   ```bash
   # Using venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Or using conda
   conda create -n crop-analysis python=3.8
   conda activate crop-analysis
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python -c "import pandas, numpy, matplotlib; print('✓ All dependencies installed')"
   ```

## Usage

### Quick Start

#### Run Full Analysis Pipeline
```bash
python scripts/run_analysis.py
```
This generates processed data, analysis reports, and visualizations.

#### Generate Report
```bash
python scripts/generate_report.py --output reports/analysis_report.md
```

#### Use as Library
```python
from src.data_loader import CropDataLoader
from src.eda_analyzer import EDAAnalyzer
from src.visualization import Visualizer

# Load data
loader = CropDataLoader()
df = loader.load_data('data/raw/consolidated_crop_data.csv')

# Perform EDA
analyzer = EDAAnalyzer(df)
summary = analyzer.get_summary_statistics()
print(summary)

# Visualize
visualizer = Visualizer(df)
visualizer.plot_production_trends('Rice')
```

### Jupyter Notebooks

Explore the analysis step-by-step:

```bash
jupyter notebook notebooks/
```

Notebooks include:
- **01_data_loading.ipynb**: Data import and initial exploration
- **02_eda_analysis.ipynb**: Distribution analysis and correlations
- **03_statistical_analysis.ipynb**: Time series and statistical modeling

## Project Structure

```
DATA-ANALYSIS/
├── data/
│   ├── raw/                    # Original CSV file
│   └── processed/              # Cleaned, processed data
├── docs/                       # Documentation
├── notebooks/                  # Jupyter analysis notebooks
├── src/                        # Core Python modules
│   ├── data_loader.py         # Data loading utilities
│   ├── data_cleaner.py        # Data cleaning and validation
│   ├── eda_analyzer.py        # Statistical analysis
│   ├── statistical_analyzer.py # Advanced statistics
│   └── visualization.py       # Plotting functions
├── reports/                    # Generated reports
├── visualizations/             # Output charts
├── tests/                      # Unit tests
├── scripts/                    # Runnable scripts
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

## Key Findings (Summary)

Based on analysis of the data:

1. **Rice Production Growth**: Consistent upward trend from 33,542 Mton (2010-11) to 40,697 Mton (2023-24) - **21.3% growth**
2. **Oilseeds Expansion**: Area under cultivation increased 67% while production grew 72%
3. **Pulses Variability**: High variability in area but stable production - suggests improved productivity
4. **Condiments Surge**: Strong growth trajectory, particularly for Onion and Garlic - market demand indicators
5. **Data Quality Issues**: Missing production values for Tea (2016-2024) and gaps in some minor crops

Detailed analysis available in: [reports/](reports/)

## Code Quality

- **PEP 8 Compliant**: All code follows Python style guidelines
- **Docstrings**: Comprehensive documentation for all functions
- **Type Hints**: Function signatures include type annotations
- **Error Handling**: Robust exception handling and validation
- **Testing**: Unit tests with >80% code coverage

### Run Tests

```bash
pytest tests/ -v --cov=src
```

## Technologies Used

| Component | Technology |
|-----------|------------|
| Data Processing | pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Statistical Analysis | SciPy, Statsmodels |
| Testing | pytest |
| Development | Python 3.8+ |
| Version Control | Git, GitHub |

## Future Improvements

### Short Term
- [ ] Implement forecasting models (ARIMA, Prophet)
- [ ] Add interactive Plotly dashboards
- [ ] Handle missing values with imputation strategies
- [ ] Implement price analysis (if price data available)

### Medium Term
- [ ] Database backend (PostgreSQL/SQLite) for scalability
- [ ] REST API for data access
- [ ] Docker containerization
- [ ] Automated data pipeline with scheduling
- [ ] ML models for yield prediction

### Long Term
- [ ] Web dashboard with real-time updates
- [ ] Integration with agricultural policy databases
- [ ] Geospatial analysis with regional breakdowns
- [ ] Climate data correlation analysis
- [ ] Multi-year forecasting and scenario planning

## Performance & Scalability

**Current Performance**:
- Data load time: <100ms
- Full analysis pipeline: <5 seconds
- Memory usage: <100MB for all operations

**Scalability Considerations**:
- For >10M rows, implement Dask or Polars for distributed processing
- Consider database backend for large datasets
- Implement caching for repeated calculations
- Parallel processing for visualization generation

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`
```bash
# Solution: Run from project root
cd /path/to/DATA-ANALYSIS
python scripts/run_analysis.py
```

**Issue**: Missing data columns
```bash
# Solution: Verify data file integrity
python -c "from src.data_loader import CropDataLoader; loader = CropDataLoader(); df = loader.load_data('data/raw/consolidated_crop_data.csv'); print(df.info())"
```

**Issue**: Memory errors with large datasets
```python
# Use chunking for large files
loader = CropDataLoader()
for chunk in loader.load_data_chunked('data/raw/consolidated_crop_data.csv', chunksize=5000):
    # Process chunk
    pass
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas for Contribution
- [ ] New crop categories
- [ ] Enhanced visualization techniques
- [ ] Performance optimization
- [ ] Documentation improvements
- [ ] Bug fixes and issue resolution

## Citation

If you use this project in your research, please cite:

```bibtex
@software{crop_analysis_2026,
  title={Agricultural Crop Data Analysis},
  author={Spandan, Mohammad},
  year={2026},
  url={https://github.com/Mohammad-Spandan/DATA-ANALYSIS}
}
```

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Contact & Support

- **Author**: Mohammad Spandan
- **Issues**: [GitHub Issues](https://github.com/Mohammad-Spandan/DATA-ANALYSIS/issues)
- **Email**: [Project Issues](https://github.com/Mohammad-Spandan/DATA-ANALYSIS/issues)

## Acknowledgments

- Agricultural data from public agricultural statistics
- Data science community for best practices and tools
- Contributors and maintainers

---

**Last Updated**: June 2026
**Status**: ✅ Production Ready
