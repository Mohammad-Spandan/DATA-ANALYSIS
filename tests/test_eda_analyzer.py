"""
Unit tests for EDA analyzer module.
"""

import pytest
import pandas as pd
import numpy as np

from src.eda_analyzer import EDAAnalyzer


class TestEDAAnalyzer:
    """Test cases for EDAAnalyzer class."""

    @pytest.fixture
    def sample_df(self):
        """Create sample DataFrame for testing."""
        return pd.DataFrame({
            "crop_id": [1, 1, 1, 2, 2, 2],
            "crop_name": ["Rice", "Rice", "Rice", "Wheat", "Wheat", "Wheat"],
            "crop_category": ["Major Crops", "Major Crops", "Major Crops",
                             "Cereals", "Cereals", "Cereals"],
            "year": ["2020-21", "2021-22", "2022-23", "2020-21", "2021-22", "2022-23"],
            "production": [100, 120, 130, 200, 210, 220],
            "area_000ac": [50, 52, 55, 80, 82, 85],
        })

    def test_get_summary_statistics(self, sample_df):
        """Test summary statistics generation."""
        analyzer = EDAAnalyzer(sample_df)
        summary = analyzer.get_summary_statistics()
        
        assert summary is not None
        assert len(summary) > 0

    def test_analyze_crop(self, sample_df):
        """Test crop analysis."""
        analyzer = EDAAnalyzer(sample_df)
        analysis = analyzer.analyze_crop(1)
        
        assert analysis["crop_name"] == "Rice"
        assert analysis["crop_id"] == 1
        assert "growth_rate_pct" in analysis

    def test_analyze_nonexistent_crop(self, sample_df):
        """Test analysis of non-existent crop."""
        analyzer = EDAAnalyzer(sample_df)
        analysis = analyzer.analyze_crop(999)
        
        assert "error" in analysis

    def test_get_top_crops(self, sample_df):
        """Test getting top crops."""
        analyzer = EDAAnalyzer(sample_df)
        top_crops = analyzer.get_top_crops(metric="production", n=2)
        
        assert len(top_crops) == 2
        assert "crop_name" in top_crops.columns

    def test_analyze_category(self, sample_df):
        """Test category analysis."""
        analyzer = EDAAnalyzer(sample_df)
        analysis = analyzer.analyze_category("Major Crops")
        
        assert analysis["category"] == "Major Crops"
        assert "crops" in analysis

    def test_get_production_correlation(self, sample_df):
        """Test production correlation analysis."""
        analyzer = EDAAnalyzer(sample_df)
        correlation = analyzer.get_production_correlation()
        
        assert correlation is not None
        assert len(correlation) > 0
        assert "correlation" in correlation.columns
