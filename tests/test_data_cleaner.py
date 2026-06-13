"""
Unit tests for data cleaner module.
"""

import pytest
import pandas as pd
import numpy as np

from src.data_cleaner import DataCleaner


class TestDataCleaner:
    """Test cases for DataCleaner class."""

    @pytest.fixture
    def sample_df(self):
        """Create sample DataFrame for testing."""
        return pd.DataFrame({
            "crop_id": [1, 1, 2, 2, 1],
            "year": ["2020-21", "2020-21", "2020-21", "2021-22", "2021-22"],
            "production": [100, 100, 200, 210, np.nan],
            "area_000ac": [50, 50, 80, 85, 55],
        })

    def test_remove_duplicates(self, sample_df):
        """Test duplicate removal."""
        cleaner = DataCleaner(sample_df)
        assert len(cleaner.df) == 5
        
        cleaner.remove_duplicates(subset=["crop_id", "year"])
        # Should remove one duplicate
        assert len(cleaner.df) == 4

    def test_handle_missing_values_drop(self, sample_df):
        """Test missing value handling with drop method."""
        cleaner = DataCleaner(sample_df)
        initial_len = len(cleaner.df)
        
        cleaner.handle_missing_values(method="drop")
        assert len(cleaner.df) < initial_len

    def test_handle_missing_values_mean(self, sample_df):
        """Test missing value handling with mean method."""
        cleaner = DataCleaner(sample_df)
        cleaner.handle_missing_values(method="mean")
        
        # Check that missing values are filled
        assert not cleaner.df["production"].isna().any()

    def test_normalize_column(self, sample_df):
        """Test column normalization."""
        cleaner = DataCleaner(sample_df)
        cleaner.normalize_column("production", method="minmax")
        
        normalized = cleaner.df["production_normalized"]
        # MinMax normalized values should be between 0 and 1
        assert normalized.min() >= 0
        assert normalized.max() <= 1

    def test_get_cleaned_data(self, sample_df):
        """Test retrieving cleaned data."""
        cleaner = DataCleaner(sample_df)
        result = cleaner.get_cleaned_data()
        assert isinstance(result, pd.DataFrame)

    def test_get_cleaning_report(self, sample_df):
        """Test cleaning report generation."""
        cleaner = DataCleaner(sample_df)
        cleaner.remove_duplicates()
        
        report = cleaner.get_cleaning_report()
        assert "original_rows" in report
        assert "final_rows" in report
        assert "operations" in report
