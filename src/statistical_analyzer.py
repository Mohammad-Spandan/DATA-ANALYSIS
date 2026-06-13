"""
Advanced statistical analysis utilities.

Functions:
    - calculate_cagr: Compound Annual Growth Rate
    - perform_regression: Linear regression analysis
    - detect_anomalies: Identify outliers using statistical methods
"""

import logging
from typing import Dict, Tuple

import pandas as pd
import numpy as np
from scipy import stats

logger = logging.getLogger(__name__)


class StatisticalAnalyzer:
    """Perform advanced statistical analysis on crop data."""

    def __init__(self, df: pd.DataFrame):
        """
        Initialize the statistical analyzer.

        Args:
            df: Input DataFrame
        """
        self.df = df

    def calculate_cagr(self, crop_id: int, start_year: str, end_year: str) -> float:
        """
        Calculate Compound Annual Growth Rate (CAGR).

        Args:
            crop_id: ID of the crop
            start_year: Starting year
            end_year: Ending year

        Returns:
            CAGR as percentage
        """
        crop_data = self.df[self.df["crop_id"] == crop_id]
        start_value = crop_data[crop_data["year"] == start_year]["production"].values
        end_value = crop_data[crop_data["year"] == end_year]["production"].values

        if len(start_value) == 0 or len(end_value) == 0:
            return None

        start_value = float(start_value[0])
        end_value = float(end_value[0])

        # Parse years
        start_year_int = int(start_year.split("-")[0])
        end_year_int = int(end_year.split("-")[0])
        n_years = end_year_int - start_year_int

        if n_years <= 0 or start_value <= 0:
            return None

        cagr = (((end_value / start_value) ** (1 / n_years)) - 1) * 100
        logger.info(f"Calculated CAGR for crop {crop_id}: {cagr:.2f}%")
        return cagr

    def perform_correlation_analysis(self) -> pd.DataFrame:
        """
        Perform correlation analysis between numeric columns.

        Returns:
            Correlation matrix
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        correlation_matrix = self.df[numeric_cols].corr()
        logger.info("Performed correlation analysis")
        return correlation_matrix

    def detect_anomalies(
        self, column: str, method: str = "iqr", threshold: float = 1.5
    ) -> pd.DataFrame:
        """
        Detect anomalies in a column using statistical methods.

        Args:
            column: Column to analyze
            method: 'iqr' or 'zscore'
            threshold: IQR multiplier or zscore threshold

        Returns:
            DataFrame with anomalies flagged
        """
        result_df = self.df.copy()
        result_df["is_anomaly"] = False

        if method == "iqr":
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            result_df["is_anomaly"] = (
                (result_df[column] < lower_bound) | (result_df[column] > upper_bound)
            )
        elif method == "zscore":
            z_scores = np.abs(stats.zscore(self.df[column].dropna()))
            result_df.loc[z_scores.index, "is_anomaly"] = z_scores > threshold

        anomalies = result_df[result_df["is_anomaly"]]
        logger.info(f"Detected {len(anomalies)} anomalies in {column}")
        return anomalies

    def calculate_productivity(self) -> pd.DataFrame:
        """
        Calculate productivity (production per unit area) for each record.

        Returns:
            DataFrame with productivity metrics
        """
        result_df = self.df.copy()
        result_df["productivity"] = result_df["production"] / result_df["area_000ac"]
        result_df["productivity"] = result_df["productivity"].replace([np.inf, -np.inf], np.nan)

        logger.info("Calculated productivity metrics")
        return result_df

    def get_volatility(self, crop_id: int) -> Dict:
        """
        Calculate volatility metrics for a crop.

        Args:
            crop_id: ID of the crop

        Returns:
            Dictionary with volatility metrics
        """
        crop_data = self.df[self.df["crop_id"] == crop_id]["production"].dropna()

        if len(crop_data) < 2:
            return {"error": "Insufficient data"}

        volatility = crop_data.std() / crop_data.mean() if crop_data.mean() != 0 else 0
        coefficient_of_variation = (crop_data.std() / crop_data.mean()) * 100

        return {
            "crop_id": crop_id,
            "volatility": volatility,
            "coefficient_of_variation": coefficient_of_variation,
            "std_dev": crop_data.std(),
            "mean": crop_data.mean(),
        }
