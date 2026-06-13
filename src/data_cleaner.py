"""
Data cleaning and preprocessing utilities.

Functions:
    - remove_duplicates: Remove duplicate rows
    - handle_missing_values: Fill or remove missing data
    - normalize_columns: Standardize column values
"""

import logging
from typing import Optional, List

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class DataCleaner:
    """Clean and preprocess agricultural data."""

    def __init__(self, df: pd.DataFrame):
        """
        Initialize the cleaner with a DataFrame.

        Args:
            df: Input DataFrame to clean
        """
        self.df = df.copy()
        self.original_df = df.copy()
        self.cleaning_log = []

    def remove_duplicates(self, subset: Optional[List[str]] = None) -> "DataCleaner":
        """
        Remove duplicate rows.

        Args:
            subset: Columns to consider for duplicates. If None, uses all columns

        Returns:
            Self for method chaining
        """
        initial_size = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset)
        removed = initial_size - len(self.df)
        logger.info(f"Removed {removed} duplicate rows")
        self.cleaning_log.append(f"Removed {removed} duplicates")
        return self

    def handle_missing_values(
        self, method: str = "drop", subset: Optional[List[str]] = None
    ) -> "DataCleaner":
        """
        Handle missing values in the data.

        Args:
            method: 'drop' to remove rows, 'mean' to fill with mean, 'forward_fill' for forward fill
            subset: Columns to apply cleaning to

        Returns:
            Self for method chaining
        """
        initial_missing = self.df.isnull().sum().sum()

        if method == "drop":
            self.df = self.df.dropna(subset=subset)
        elif method == "mean":
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if subset is None or col in subset:
                    self.df[col].fillna(self.df[col].mean(), inplace=True)
        elif method == "forward_fill":
            self.df = self.df.fillna(method="ffill")
        else:
            raise ValueError(f"Unknown method: {method}")

        final_missing = self.df.isnull().sum().sum()
        removed_missing = initial_missing - final_missing
        logger.info(f"Handled {removed_missing} missing values using {method}")
        self.cleaning_log.append(f"Handled {removed_missing} missing values ({method})")
        return self

    def remove_outliers(
        self, columns: List[str], method: str = "iqr", threshold: float = 1.5
    ) -> "DataCleaner":
        """
        Remove outliers from specified columns.

        Args:
            columns: Columns to check for outliers
            method: 'iqr' or 'zscore'
            threshold: IQR multiplier or zscore threshold

        Returns:
            Self for method chaining
        """
        initial_size = len(self.df)

        if method == "iqr":
            for col in columns:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                self.df = self.df[(self.df[col] >= lower_bound) & (self.df[col] <= upper_bound)]
        elif method == "zscore":
            from scipy import stats
            z_scores = np.abs(stats.zscore(self.df[columns]))
            self.df = self.df[(z_scores < threshold).all(axis=1)]

        removed = initial_size - len(self.df)
        logger.info(f"Removed {removed} outliers using {method}")
        self.cleaning_log.append(f"Removed {removed} outliers ({method})")
        return self

    def normalize_column(
        self, column: str, method: str = "minmax"
    ) -> "DataCleaner":
        """
        Normalize a numeric column.

        Args:
            column: Column to normalize
            method: 'minmax' or 'zscore'

        Returns:
            Self for method chaining
        """
        if method == "minmax":
            min_val = self.df[column].min()
            max_val = self.df[column].max()
            self.df[f"{column}_normalized"] = (self.df[column] - min_val) / (max_val - min_val)
        elif method == "zscore":
            mean = self.df[column].mean()
            std = self.df[column].std()
            self.df[f"{column}_normalized"] = (self.df[column] - mean) / std

        logger.info(f"Normalized {column} using {method}")
        self.cleaning_log.append(f"Normalized {column} ({method})")
        return self

    def get_cleaned_data(self) -> pd.DataFrame:
        """
        Get the cleaned DataFrame.

        Returns:
            Cleaned DataFrame
        """
        return self.df

    def get_cleaning_report(self) -> dict:
        """
        Get a report of all cleaning operations.

        Returns:
            Dictionary with cleaning statistics
        """
        return {
            "original_rows": len(self.original_df),
            "final_rows": len(self.df),
            "rows_removed": len(self.original_df) - len(self.df),
            "original_columns": len(self.original_df.columns),
            "final_columns": len(self.df.columns),
            "operations": self.cleaning_log,
        }
