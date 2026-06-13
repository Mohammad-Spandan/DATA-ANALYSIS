"""
Unit tests for data loader module.
"""

import pytest
import pandas as pd
from pathlib import Path

from src.data_loader import CropDataLoader


class TestCropDataLoader:
    """Test cases for CropDataLoader class."""

    @pytest.fixture
    def loader(self):
        """Create a loader instance."""
        return CropDataLoader()

    @pytest.fixture
    def sample_data(self, tmp_path):
        """Create sample CSV data for testing."""
        data = {
            "Crop_ID": [1, 1, 2],
            "Year": ["2020-21", "2021-22", "2020-21"],
            "Crop_Name": ["Rice", "Rice", "Wheat"],
            "Area_000ac": [100, 105, 80],
            "Production": [500, 550, 400],
            "Production_Unit": ["000Mton", "000Mton", "000Mton"],
        }
        df = pd.DataFrame(data)
        file_path = tmp_path / "test_data.csv"
        df.to_csv(file_path, index=False)
        return file_path

    def test_load_data(self, loader, sample_data):
        """Test data loading functionality."""
        df = loader.load_data(str(sample_data), validate=False)
        assert df is not None
        assert len(df) == 3
        assert "crop_id" in df.columns

    def test_validate_data(self, loader, sample_data):
        """Test data validation."""
        df = loader.load_data(str(sample_data), validate=True)
        assert loader.validate_data() is True

    def test_missing_file(self, loader):
        """Test handling of missing file."""
        with pytest.raises(FileNotFoundError):
            loader.load_data("/nonexistent/path/file.csv")

    def test_get_summary_statistics(self, loader, sample_data):
        """Test summary statistics generation."""
        loader.load_data(str(sample_data), validate=False)
        summary = loader.get_summary_statistics()
        assert summary is not None
        assert len(summary) > 0

    def test_describe_crop(self, loader, sample_data):
        """Test crop description."""
        loader.load_data(str(sample_data), validate=False)
        description = loader.describe_crop(1)
        assert description["crop_name"] == "Rice"
        assert description["crop_id"] == 1

    def test_describe_nonexistent_crop(self, loader, sample_data):
        """Test description of non-existent crop."""
        loader.load_data(str(sample_data), validate=False)
        with pytest.raises(ValueError):
            loader.describe_crop(999)
