"""Visualization module for generating charts and graphs."""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, Any, List
from .scoring import MAX_POINTS_PER_QUESTION, TOTAL_QUESTIONS, OPTION_SCORES

class ChartGenerator:
    """Handles generation of visualization charts."""
    
    def __init__(self):
        """Initialize the ChartGenerator."""
        self.figure_size = (10, 10)
        
    def create_radar_chart(
        self,
        scores: Dict[str, Any],
        df: pd.DataFrame,
        previous_results: Dict[str, Any] = None,
        show: bool = True
    ) -> plt.Figure:
        """
        Create a radar chart of section scores, optionally overlaying previous results.
        
        Args:
            scores: Dictionary containing section scores and totals
            df: DataFrame containing questions data
            previous_results: Optional dictionary containing previous section scores and totals
            show: Whether to generate and show the chart
            
        Returns:
            matplotlib.figure.Figure: Generated radar chart, or None if show is False
        """
        if not show:
            return None
            
        fig = plt.figure(figsize=self.figure_size)
        ax = fig.add_subplot(111, projection='polar')
        
        # Prepare the data
        sections = list(scores['section_scores'].keys())
        raw_scores = [scores['section_scores'][section] for section in sections]
        max_scores = [40 for _ in sections]  # Each section has 5 questions * 8 points = 40 max points
        max_value = max(max_scores)
        
        # Number of variables
        num_vars = len(sections)
        
        # Compute angle for each axis
        angles = [n / float(num_vars) * 2 * np.pi for n in range(num_vars)]
        angles += angles[:1]  # Complete the circle
        
        # Add the scores to complete the circle
        raw_scores += raw_scores[:1]
        
        # Plot previous results if available
        if previous_results and 'responses' in previous_results:
            # Calculate section scores from previous responses
            prev_section_scores = {}
            for section in sections:
                section_qs = df[df['section'] == section]
                section_score = sum(
                    OPTION_SCORES[previous_results['responses'].get(str(idx), 0)]
                    for idx in section_qs.index
                )
                prev_section_scores[section] = section_score
            
            # Create previous scores list in same order as sections
            prev_raw_scores = [prev_section_scores[section] for section in sections]
            prev_raw_scores += prev_raw_scores[:1]  # Complete the circle
            
            # Plot previous results
            ax.plot(angles, prev_raw_scores, 'o-', linewidth=2, color='gray', alpha=0.5)
            ax.fill(angles, prev_raw_scores, color='orange', alpha=0.5)

        # Plot current data
        ax.plot(angles, raw_scores, 'o-', linewidth=2, color='blue')
        ax.fill(angles, raw_scores, color='blue', alpha=0.25)
        
        # Fix axis to go in the right order and start at 12 o'clock
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        
        # Set chart limits and grid
        ax.set_ylim(0, max_value)
        grid_ticks = [i * max_value/5 for i in range(6)]  # 5 intervals
        ax.set_rgrids(grid_ticks, angle=0, fontsize=8)
        
        # Draw axis lines for each angle and label
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(sections, fontsize=9)
        
        # Rotate the axis labels to be more readable
        self._adjust_label_positions(ax, angles[:-1])
        
        # Set chart title
        plt.title("Section Scores", pad=20)
        
        # Add score labels
        self._add_score_labels(ax, angles[:-1], sections, raw_scores[:-1], max_scores, max_value)
        
        plt.tight_layout()
        return fig
        
    def _adjust_label_positions(self, ax: plt.Axes, angles: List[float]) -> None:
        """
        Adjust the position of axis labels for better readability.
        
        Args:
            ax: Matplotlib axis object
            angles: List of angles for each axis
        """
        for label, angle in zip(ax.get_xticklabels(), angles):
            if angle in (0, np.pi):
                label.set_horizontalalignment('center')
            elif 0 < angle < np.pi:
                label.set_horizontalalignment('left')
            else:
                label.set_horizontalalignment('right')
                
    def _add_score_labels(
        self,
        ax: plt.Axes,
        angles: List[float],
        sections: List[str],
        scores: List[float],
        max_scores: List[float],
        max_value: float
    ) -> None:
        """
        Add score labels to the radar chart.
        
        Args:
            ax: Matplotlib axis object
            angles: List of angles for each axis
            sections: List of section names
            scores: List of raw scores
            max_scores: List of maximum possible scores
            max_value: Maximum value on the chart
        """
        for angle, score, max_score in zip(angles, scores, max_scores):
            # Position label based on relative score
            relative_pos = (score / max_value * max_value)
            label_distance = relative_pos + (2 if relative_pos < max_value * 0.8 else -2)
            ha = 'left' if 0 <= angle <= np.pi else 'right'
            label = f'{int(score)}/{max_score}'
            ax.text(angle, label_distance, label, ha=ha, va='center', fontsize=9)
