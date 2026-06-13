"""
Visualization utilities for agricultural data analysis.

Functions:
    - plot_production_trend: Line plot of production over time
    - plot_crop_comparison: Bar chart comparing crops
    - plot_distribution: Histogram of production distribution
"""

import logging
from typing import Optional, List
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from src.config import VIZ_DIR, FIGURE_DPI, FIGURE_SIZE, STYLE, COLOR_PALETTE

logger = logging.getLogger(__name__)

# Set visualization style
plt.style.use(STYLE)
sns.set_palette(COLOR_PALETTE)


class Visualizer:
    """Create visualizations for agricultural data."""

    def __init__(self, df: pd.DataFrame, output_dir: Optional[Path] = None):
        """
        Initialize the visualizer.

        Args:
            df: Input DataFrame
            output_dir: Directory to save visualizations
        """
        self.df = df
        self.output_dir = output_dir or VIZ_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def plot_production_trend(self, crop_name: str, save: bool = True) -> None:
        """
        Plot production trend for a crop over time.

        Args:
            crop_name: Name of the crop
            save: Whether to save the figure
        """
        crop_data = self.df[self.df["crop_name"] == crop_name].sort_values("year")

        if crop_data.empty:
            logger.warning(f"No data found for crop: {crop_name}")
            return

        fig, ax = plt.subplots(figsize=FIGURE_SIZE, dpi=FIGURE_DPI)
        ax.plot(crop_data["year"], crop_data["production"], marker="o", linewidth=2)
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("Production", fontsize=12)
        ax.set_title(f"Production Trend: {crop_name}", fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3)

        if save:
            filename = f"{self.output_dir}/{crop_name}_production_trend.png"
            plt.savefig(filename, dpi=FIGURE_DPI, bbox_inches="tight")
            logger.info(f"Saved visualization: {filename}")

        plt.close()

    def plot_crop_comparison(
        self, crops: List[str], metric: str = "production", save: bool = True
    ) -> None:
        """
        Compare multiple crops using a bar chart.

        Args:
            crops: List of crop names
            metric: Metric to compare ('production' or 'area_000ac')
            save: Whether to save the figure
        """
        comparison_data = self.df[self.df["crop_name"].isin(crops)]
        avg_values = comparison_data.groupby("crop_name")[metric].mean().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=FIGURE_SIZE, dpi=FIGURE_DPI)
        avg_values.plot(kind="bar", ax=ax, color=sns.color_palette(COLOR_PALETTE, len(avg_values)))
        ax.set_xlabel("Crop", fontsize=12)
        ax.set_ylabel(f"Average {metric.replace('_', ' ').title()}", fontsize=12)
        ax.set_title(f"Crop Comparison: {metric.replace('_', ' ').title()}", fontsize=14, fontweight="bold")
        ax.tick_params(axis="x", rotation=45)
        plt.tight_layout()

        if save:
            filename = f"{self.output_dir}/crop_comparison_{metric}.png"
            plt.savefig(filename, dpi=FIGURE_DPI, bbox_inches="tight")
            logger.info(f"Saved visualization: {filename}")

        plt.close()

    def plot_distribution(
        self, column: str, bins: int = 30, save: bool = True
    ) -> None:
        """
        Plot distribution of a numeric column.

        Args:
            column: Column name to plot
            bins: Number of bins for histogram
            save: Whether to save the figure
        """
        fig, ax = plt.subplots(figsize=FIGURE_SIZE, dpi=FIGURE_DPI)
        ax.hist(self.df[column].dropna(), bins=bins, edgecolor="black", alpha=0.7)
        ax.set_xlabel(column.replace("_", " ").title(), fontsize=12)
        ax.set_ylabel("Frequency", fontsize=12)
        ax.set_title(f"Distribution of {column.replace('_', ' ').title()}", fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3, axis="y")

        if save:
            filename = f"{self.output_dir}/distribution_{column}.png"
            plt.savefig(filename, dpi=FIGURE_DPI, bbox_inches="tight")
            logger.info(f"Saved visualization: {filename}")

        plt.close()

    def plot_heatmap(
        self, metric: str = "production", save: bool = True
    ) -> None:
        """
        Create a heatmap of crop metrics by year.

        Args:
            metric: Metric to visualize
            save: Whether to save the figure
        """
        pivot_data = self.df.pivot_table(
            values=metric, index="crop_name", columns="year", aggfunc="mean"
        )

        fig, ax = plt.subplots(figsize=(15, 10), dpi=FIGURE_DPI)
        sns.heatmap(pivot_data, cmap="YlGn", ax=ax, cbar_kws={"label": metric})
        ax.set_title(f"Heatmap: {metric.replace('_', ' ').title()} by Crop and Year",
                     fontsize=14, fontweight="bold")
        plt.tight_layout()

        if save:
            filename = f"{self.output_dir}/heatmap_{metric}.png"
            plt.savefig(filename, dpi=FIGURE_DPI, bbox_inches="tight")
            logger.info(f"Saved visualization: {filename}")

        plt.close()
