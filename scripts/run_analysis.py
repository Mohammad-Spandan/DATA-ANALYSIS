#!/usr/bin/env python
"""
Main script to run the complete analysis pipeline.

Usage:
    python scripts/run_analysis.py
"""

import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data_loader import CropDataLoader
from src.data_cleaner import DataCleaner
from src.eda_analyzer import EDAAnalyzer
from src.visualization import Visualizer
from src.config import RAW_DATA_FILE, PROCESSED_DATA_DIR, REPORTS_DIR

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def run_pipeline():
    """Execute the complete analysis pipeline."""
    try:
        logger.info("="*60)
        logger.info("Starting Agricultural Crop Data Analysis Pipeline")
        logger.info("="*60)

        # Step 1: Load data
        logger.info("\n[1/5] Loading data...")
        loader = CropDataLoader()
        df = loader.load_data()
        logger.info(f"✓ Loaded {len(df)} records")

        # Step 2: Clean data
        logger.info("\n[2/5] Cleaning data...")
        cleaner = DataCleaner(df)
        cleaned_df = cleaner.remove_duplicates().get_cleaned_data()
        report = cleaner.get_cleaning_report()
        logger.info(f"✓ Cleaned data: {report}")

        # Step 3: Perform EDA
        logger.info("\n[3/5] Performing Exploratory Data Analysis...")
        analyzer = EDAAnalyzer(cleaned_df)
        
        # Get summary statistics
        summary = analyzer.get_summary_statistics()
        logger.info(f"✓ Computed summary statistics")
        
        # Analyze top crops
        top_crops = analyzer.get_top_crops(metric="production", n=5)
        logger.info(f"✓ Top 5 crops by production:")
        for idx, row in top_crops.iterrows():
            logger.info(f"  - {row['crop_name']}: {row['production']:.2f}")

        # Step 4: Create visualizations
        logger.info("\n[4/5] Creating visualizations...")
        visualizer = Visualizer(cleaned_df)
        
        crops_to_plot = ["Rice", "Maize", "Wheat", "Potato", "Onion"]
        for crop in crops_to_plot:
            try:
                visualizer.plot_production_trend(crop)
                logger.info(f"✓ Created plot for {crop}")
            except Exception as e:
                logger.warning(f"Could not plot {crop}: {e}")

        # Plot distributions
        visualizer.plot_distribution("production")
        visualizer.plot_distribution("area_000ac")
        logger.info(f"✓ Created distribution plots")

        # Step 5: Generate report
        logger.info("\n[5/5] Generating report...")
        report_content = generate_report(analyzer, top_crops, report)
        report_path = REPORTS_DIR / "analysis_report.md"
        with open(report_path, "w") as f:
            f.write(report_content)
        logger.info(f"✓ Report saved to {report_path}")

        # Save cleaned data
        processed_path = PROCESSED_DATA_DIR / "processed_crop_data.csv"
        cleaned_df.to_csv(processed_path, index=False)
        logger.info(f"✓ Processed data saved to {processed_path}")

        logger.info("\n" + "="*60)
        logger.info("✓ Analysis pipeline completed successfully!")
        logger.info("="*60)

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise


def generate_report(analyzer, top_crops, cleaning_report):
    """Generate a markdown report of the analysis."""
    report = """# Agricultural Crop Data Analysis Report

## Executive Summary

This report presents findings from the analysis of agricultural crop production data.

## Data Quality

- **Original Records**: {}
- **Final Records**: {}
- **Records Removed**: {}
- **Cleaning Operations**: {}

## Top 5 Crops by Production

""".format(
        cleaning_report["original_rows"],
        cleaning_report["final_rows"],
        cleaning_report["rows_removed"],
        ", ".join(cleaning_report["operations"])
    )

    for idx, row in top_crops.iterrows():
        report += f"\n{idx+1}. {row['crop_name']}: {row['production']:.2f}"

    report += """\n
## Key Insights

- Data spans multiple agricultural seasons
- Multiple crop categories analyzed
- Production trends tracked over time

## Next Steps

1. Implement forecasting models
2. Analyze regional variations
3. Correlate with climate data

---

*Report Generated Automatically*
"""

    return report


if __name__ == "__main__":
    run_pipeline()
