#!/usr/bin/env python3

from class_argparse import ClassArgParser

from .team_estimator import TeamOptimizer


class Main(ClassArgParser):
    HOURS_PER_DAY = 9
    WORK_DAYS_PER_MONTH = 22
    DAYS_PER_WEEK = 5
    SENIOR_PRODUCTIVITY_FACTOR = 1.25
    EFFECTIVE_UTILIZATION = 0.75
    BUFFER_PERCENTAGE = 0.15

    def __init__(self):
        super().__init__("Team Optimizer CLI")
        self.team_optimizer = TeamOptimizer()

    def team_size(self):
        """Find optimal minimum team"""
        man_hours_required = 10000
        duration_months = 6
        total_qa = 1
        total_designer = 1
        max_seniors = 4
        min_seniors = 2
        max_juniors = 12

        self.team_optimizer.calculate_team_size(
            man_hours_required=man_hours_required,
            duration_months=duration_months,
            hours_per_day=self.HOURS_PER_DAY,
            work_days_per_month=self.WORK_DAYS_PER_MONTH,
            senior_productivity_factor=self.SENIOR_PRODUCTIVITY_FACTOR,
            total_qa=total_qa,
            total_designers=total_designer,
            max_juniors=max_juniors,
            max_seniors=max_seniors,
            min_seniors=min_seniors,
            effective_utilization=self.EFFECTIVE_UTILIZATION,
            buffer_percentage=self.BUFFER_PERCENTAGE,
        )

    def delivery_timeline(self):
        """Calculate delivery time for a fixed team"""
        man_hours_required = 10000
        total_seniors = 4
        total_juniors = 10

        self.team_optimizer.calculate_weeks_needed(
            man_hours_required=man_hours_required,
            total_seniors=total_seniors,
            total_juniors=total_juniors,
            hours_per_day=self.HOURS_PER_DAY,
            days_per_week=self.DAYS_PER_WEEK,
            senior_productivity_factor=self.SENIOR_PRODUCTIVITY_FACTOR,
            effective_utilization=self.EFFECTIVE_UTILIZATION,
            buffer_percentage=self.BUFFER_PERCENTAGE,
        )


if __name__ == "__main__":
    Main()()
