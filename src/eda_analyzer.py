"""
Exploratory Data Analysis (EDA) utilities.

Functions:
    - get_crop_statistics: Statistics for individual crops
    - get_category_statistics: Statistics by crop category
    - analyze_trends: Analyze production trends over time
"""

import logging
from typing import Dict, List, Tuple

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class EDAAnalyzer:
    """Perform exploratory data analysis on crop data."""

    def __init__(self, df: pd.DataFrame):
        """
        Initialize the EDA analyzer.

        Args:
            df: Input DataFrame
        """
        self.df = df
        self.crop_names = {
            1: "Rice", 2: "Jute", 3: "Sugarcane", 4: "Tea", 5: "Pulses",
            6: "Oilseeds", 7: "Condiments", 8: "Tobacco", 9: "Maize",
            10: "Jowar", 11: "Barley", 12: "Bajra", 13: "Masur", 14: "Moong",
            15: "Gram", 16: "Mashkalai", 17: "Arhar", 18: "Chilies",
            19: "Onion", 20: "Garlic", 21: "Potato", 22: "Sweet Potato",
            23: "Betelnut", 24: "Cotton", 25: "Hemp", 26: "Mulberry"
        }

    def get_summary_statistics(self) -> pd.DataFrame:
        """
        Get summary statistics for numeric columns.

        Returns:
            DataFrame with summary statistics
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        summary = self.df[numeric_cols].describe().T
        logger.info(f"Computed summary statistics for {len(numeric_cols)} numeric columns")
        return summary

    def analyze_crop(self, crop_id: int) -> Dict:
        """
        Analyze a specific crop in detail.

        Args:
            crop_id: ID of the crop

        Returns:
            Dictionary with crop analysis
        """
        crop_data = self.df[self.df["crop_id"] == crop_id].sort_values("year")

        if crop_data.empty:
            return {"error": f"Crop ID {crop_id} not found"}

        # Calculate growth rate
        production_values = crop_data["production"].dropna()
        if len(production_values) > 1:
            growth_rate = ((production_values.iloc[-1] - production_values.iloc[0]) /
                          production_values.iloc[0] * 100)
        else:
            growth_rate = None

        return {
            "crop_name": crop_data["crop_name"].iloc[0],
            "crop_id": crop_id,
            "years_covered": len(crop_data),
            "avg_area": crop_data["area_000ac"].mean(),
            "avg_production": crop_data["production"].mean(),
            "min_production": crop_data["production"].min(),
            "max_production": crop_data["production"].max(),
            "std_production": crop_data["production"].std(),
            "growth_rate_pct": growth_rate,
            "missing_data_pct": (crop_data["production"].isnull().sum() / len(crop_data)) * 100,
        }

    def get_top_crops(self, metric: str = "production", n: int = 10) -> pd.DataFrame:
        """
        Get top N crops by specified metric.

        Args:
            metric: Metric to rank by ('production' or 'area')
            n: Number of top crops to return

        Returns:
            DataFrame with top crops
        """
        if metric not in ["production", "area_000ac"]:
            raise ValueError(f"Unknown metric: {metric}")

        column = "production" if metric == "production" else "area_000ac"
        top_crops = self.df.groupby("crop_name")[column].mean().nlargest(n)
        logger.info(f"Retrieved top {n} crops by {metric}")
        return top_crops.to_frame().reset_index()

    def analyze_category(self, category: str) -> Dict:
        """
        Analyze crops in a specific category.

        Args:
            category: Category name

        Returns:
            Dictionary with category statistics
        """
        category_data = self.df[self.df["crop_category"] == category]

        if category_data.empty:
            return {"error": f"Category {category} not found"}

        return {
            "category": category,
            "num_crops": category_data["crop_id"].nunique(),
            "total_production_avg": category_data["production"].mean(),
            "total_area_avg": category_data["area_000ac"].mean(),
            "crops": sorted(category_data["crop_name"].unique().tolist()),
        }

    def get_production_correlation(self) -> pd.DataFrame:
        """
        Calculate correlation between area and production.

        Returns:
            Correlation values by crop
        """
        correlations = []
        for crop_id in self.df["crop_id"].unique():
            crop_data = self.df[self.df["crop_id"] == crop_id]
            correlation = crop_data[["area_000ac", "production"]].corr().iloc[0, 1]
            crop_name = crop_data["crop_name"].iloc[0]
            correlations.append({
                "crop_name": crop_name,
                "correlation": correlation
            })

        result = pd.DataFrame(correlations).sort_values("correlation", ascending=False)
        logger.info(f"Computed area-production correlations for {len(result)} crops")
        return result

    def identify_trends(self, crop_id: int) -> Dict:
        """
        Identify production trends for a crop.

        Args:
            crop_id: ID of the crop

        Returns:
            Dictionary with trend analysis
        """
        crop_data = self.df[self.df["crop_id"] == crop_id].sort_values("year")
        production = crop_data["production"].dropna()

        if len(production) < 2:
            return {"error": "Insufficient data for trend analysis"}

        # Simple trend detection
        recent_avg = production.tail(3).mean()
        earlier_avg = production.head(3).mean()
        trend_direction = "increasing" if recent_avg > earlier_avg else "decreasing"

        return {
            "crop_name": crop_data["crop_name"].iloc[0],
            "trend_direction": trend_direction,
            "recent_avg": recent_avg,
            "earlier_avg": earlier_avg,
            "volatility": production.std() / production.mean() if production.mean() != 0 else 0,
        }
