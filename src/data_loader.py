"""
Data loading utilities for agricultural crop analysis.

Functions:
    - load_data: Load CSV data with validation
    - validate_data: Check data integrity
    - describe_data: Get data summary statistics
"""

import logging
from pathlib import Path
from typing import Optional

import pandas as pd
import numpy as np

from src.config import RAW_DATA_FILE, PROCESSED_DATA_FILE

logger = logging.getLogger(__name__)


class CropDataLoader:
    """Load and manage agricultural crop data."""

    def __init__(self):
        """Initialize the data loader."""
        self.data = None
        self.raw_data = None

    def load_data(
        self, filepath: Optional[str] = None, validate: bool = True
    ) -> pd.DataFrame:
        """
        Load crop data from CSV file.

        Args:
            filepath: Path to CSV file. Defaults to config RAW_DATA_FILE
            validate: Whether to validate data after loading

        Returns:
            DataFrame containing crop data

        Raises:
            FileNotFoundError: If file doesn't exist
            pd.errors.ParserError: If file is not valid CSV
        """
        file_path = Path(filepath) if filepath else RAW_DATA_FILE

        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")

        try:
            logger.info(f"Loading data from {file_path}")
            self.raw_data = pd.read_csv(file_path)
            self.data = self.raw_data.copy()

            # Standardize column names
            self.data.columns = [
                col.lower().replace(" ", "_") for col in self.data.columns
            ]

            logger.info(
                f"Successfully loaded {len(self.data)} rows and {len(self.data.columns)} columns"
            )

            if validate:
                self.validate_data()

            return self.data

        except pd.errors.ParserError as e:
            logger.error(f"Failed to parse CSV file: {e}")
            raise

    def validate_data(self) -> bool:
        """
        Validate data integrity and structure.

        Returns:
            True if valid, raises exception otherwise

        Raises:
            ValueError: If data is invalid
        """
        if self.data is None:
            raise ValueError("No data loaded")

        required_columns = ["crop_id", "year", "crop_name", "area_000ac", "production"]
        missing_columns = [col for col in required_columns if col not in self.data.columns]

        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        logger.info("✓ Data validation passed")
        return True

    def get_summary_statistics(self) -> pd.DataFrame:
        """
        Get summary statistics of the data.

        Returns:
            DataFrame with summary statistics
        """
        if self.data is None:
            raise ValueError("No data loaded")

        summary = {
            "Metric": ["Total Records", "Unique Crops", "Year Range", "Missing Values"],
            "Value": [
                len(self.data),
                self.data["crop_id"].nunique(),
                f"{self.data['year'].min()} - {self.data['year'].max()}",
                self.data.isnull().sum().sum(),
            ],
        }

        return pd.DataFrame(summary)

    def describe_crop(self, crop_id: int) -> dict:
        """
        Get detailed information about a specific crop.

        Args:
            crop_id: ID of the crop

        Returns:
            Dictionary with crop information
        """
        if self.data is None:
            raise ValueError("No data loaded")

        crop_data = self.data[self.data["crop_id"] == crop_id]

        if crop_data.empty:
            raise ValueError(f"Crop ID {crop_id} not found")

        return {
            "crop_name": crop_data["crop_name"].iloc[0],
            "crop_id": crop_id,
            "years_covered": sorted(crop_data["year"].unique()),
            "avg_area": crop_data["area_000ac"].mean(),
            "avg_production": crop_data["production"].mean(),
            "production_unit": crop_data["production_unit"].iloc[0],
            "records": len(crop_data),
        }
