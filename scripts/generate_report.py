#!/usr/bin/env python
"""
Generate a detailed analysis report.

Usage:
    python scripts/generate_report.py --output reports/report.md
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.data_loader import CropDataLoader
from src.eda_analyzer import EDAAnalyzer
from src.statistical_analyzer import StatisticalAnalyzer


def generate_detailed_report(output_path):
    """Generate a detailed analysis report."""
    
    # Load data
    loader = CropDataLoader()
    df = loader.load_data()
    
    # Analyze
    eda_analyzer = EDAAnalyzer(df)
    stat_analyzer = StatisticalAnalyzer(df)
    
    # Generate report
    report = "# Detailed Agricultural Crop Analysis Report\n\n"
    report += "## 1. Dataset Overview\n\n"
    report += f"- Total Records: {len(df)}\n"
    report += f"- Unique Crops: {df['crop_id'].nunique()}\n"
    report += f"- Year Range: {df['year'].min()} to {df['year'].max()}\n\n"
    
    report += "## 2. Crop Statistics\n\n"
    for crop_id in sorted(df['crop_id'].unique())[:10]:  # Top 10 crops
        analysis = eda_analyzer.analyze_crop(crop_id)
        if 'error' not in analysis:
            report += f"### {analysis['crop_name']}\n\n"
            report += f"- Average Area: {analysis['avg_area']:.2f}\n"
            report += f"- Average Production: {analysis['avg_production']:.2f}\n"
            report += f"- Growth Rate: {analysis['growth_rate_pct']:.2f}%\n\n"
    
    report += "## 3. Correlation Analysis\n\n"
    corr = eda_analyzer.get_production_correlation()
    report += corr.to_markdown(index=False)
    report += "\n\n"
    
    report += "## 4. Recommendations\n\n"
    report += "- Implement forecasting models for production prediction\n"
    report += "- Analyze regional variations in crop production\n"
    report += "- Correlate with climate data for better insights\n"
    
    # Save report
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"✓ Report saved to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate detailed analysis report")
    parser.add_argument(
        "--output",
        default="reports/detailed_analysis_report.md",
        help="Output file path"
    )
    args = parser.parse_args()
    
    generate_detailed_report(args.output)
