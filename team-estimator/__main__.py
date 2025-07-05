#!/usr/bin/env python3

from itertools import product
from class_argparse import ClassArgParser

from .team_estimator.py import TeamOptimizer


class Main(ClassArgParser):

    def __init__(self):
        super().__init__("Team Optimizer CLI")
        self.team_optimizer = TeamOptimizer()

    def team_size(self):
        """Find optimal minimum team"""
        man_hours_required = 3000
        duration_months = 3

        TECH_ROLES = [
            {'name': 'frontend', 'max_seniors': 10, 'max_juniors': 10},
            {'name': 'backend', 'max_seniors': 10, 'max_juniors': 10}
        ]

        self.team_optimizer.calculate_team_size(
            man_hours_required,
            duration_months,
            self.TECH_ROLES,
            self.HOURS_PER_DAY,
            self.WORK_DAYS_PER_MONTH,
            self.SENIOR_PRODUCTIVITY_FACTOR,
            self.MAX_QA,
            self.MAX_DESIGNER,
            self.EFFECTIVE_UTILIZATION,
            self.BUFFER_PERCENTAGE
        )

    def delivery_timeline(self):
        """Calculate delivery time for a fixed team"""
        man_hours_required = 10000

        self.team_optimizer.calculate_weeks_needed(
            man_hours_required,
            ['frontend', 'backend'],
            {'frontend': 1, 'backend': 1},
            {'frontend': 10, 'backend': 10},
            self.MAX_QA,
            self.MAX_DESIGNER,
            self.HOURS_PER_DAY,
            self.DAYS_PER_WEEK,
            self.SENIOR_PRODUCTIVITY_FACTOR,
            self.EFFECTIVE_UTILIZATION,
            self.BUFFER_PERCENTAGE
        )
        man_hours_required *= (1 + buffer_percentage)

        total_weekly_capacity = 0

        for role in tech_roles_with_team:
            seniors = seniors_per_role.get(role, 0)
            juniors = juniors_per_role.get(role, 0)

            role_weekly_capacity = (
                (seniors * senior_productivity_factor) + juniors
            ) * hours_per_day * days_per_week * effective_utilization

            total_weekly_capacity += role_weekly_capacity

        if total_weekly_capacity <= 0:
            print("\n❌ Invalid team config — no capacity.")
            return

        weeks_needed = man_hours_required / total_weekly_capacity

        print(f"\n✅ Estimated delivery for fixed team (incl. {int(buffer_percentage*100)}% buffer, {int(effective_utilization*100)}% utilization):")
        print(f"  Seniors: {seniors_per_role}")
        print(f"  Juniors: {juniors_per_role}")
        print(f"  QA: {qa} (does not add capacity)")
        print(f"  Designer: {designer} (does not add capacity)")
        print(f"  ➜ Weekly dev capacity: {int(total_weekly_capacity)} man-hours/week")
        print(f"  ➜ Delivery time: {weeks_needed:.1f} weeks for {int(man_hours_required)} man-hours")


if __name__ == "__main__":
    Main()()
