#!/usr/bin/env python3

from itertools import product
from class_argparse import ClassArgParser

class TeamOptimizer:
    HOURS_PER_DAY = 8
    WORK_DAYS_PER_MONTH = 20
    DAYS_PER_WEEK = 5
    SENIOR_PRODUCTIVITY_FACTOR = 1.8
    EFFECTIVE_UTILIZATION = 0.8
    BUFFER_PERCENTAGE = 0.15
    MAX_QA = 1
    MAX_DESIGNER = 1

    def __init__(self):
        pass

    def calculate_team_size(
        self,
        man_hours_required,
        duration_months,
        tech_roles,
        hours_per_day,
        work_days_per_month,
        senior_productivity_factor,
        max_qa,
        max_designer,
        effective_utilization,
        buffer_percentage
    ):
        man_hours_required *= (1 + buffer_percentage)

        hours_per_month_per_dev = work_days_per_month * hours_per_day
        total_hours_per_dev = hours_per_month_per_dev * duration_months
        total_hours_per_dev *= effective_utilization

        best_combo = None

        role_ranges = []
        for role in tech_roles:
            seniors_range = range(1, role['max_seniors'] + 1)
            juniors_range = range(0, role['max_juniors'] + 1)
            role_ranges.append(list(product(seniors_range, juniors_range)))

        for combo in product(*role_ranges):
            for qa in range(0, max_qa + 1):
                for designer in range(0, max_designer + 1):
                    total_effective_hours = 0
                    total_seniors = 0
                    total_juniors = 0

                    for i, (seniors, juniors) in enumerate(combo):
                        tech_hours = (
                            seniors * senior_productivity_factor + juniors
                        ) * total_hours_per_dev
                        total_effective_hours += tech_hours
                        total_seniors += seniors
                        total_juniors += juniors

                    if total_effective_hours >= man_hours_required:
                        if (not best_combo or
                            total_seniors < best_combo['total_seniors'] or
                            (total_seniors == best_combo['total_seniors'] and total_juniors < best_combo['total_juniors'])):
                            best_combo = {
                                'role_combo': combo,
                                'qa': qa,
                                'designer': designer,
                                'total_capacity': total_effective_hours,
                                'total_seniors': total_seniors,
                                'total_juniors': total_juniors
                            }

        if best_combo:
            print(f"\n✅ Optimal team for {int(man_hours_required)} man-hours in {duration_months} months (incl. {int(buffer_percentage*100)}% buffer, {int(effective_utilization*100)}% utilization):")
            for i, (seniors, juniors) in enumerate(best_combo['role_combo']):
                tech_role = tech_roles[i]['name']
                print(f"  {tech_role.title()}: {seniors} seniors, {juniors} juniors")
            print(f"  QA: {best_combo['qa']} (does not add capacity)")
            print(f"  Designer: {best_combo['designer']} (does not add capacity)")
            print(f"  ➜ Total seniors: {best_combo['total_seniors']}")
            print(f"  ➜ Total juniors: {best_combo['total_juniors']}")
            print(f"  ➜ Total effective dev capacity: {int(best_combo['total_capacity'])} man-hours")
        else:
            print("\n❌ No feasible team found under given constraints. Increase duration or role caps.")

    def calculate_weeks_needed(
        self,
        man_hours_required,
        tech_roles_with_team,
        seniors_per_role,
        juniors_per_role,
        qa,
        designer,
        hours_per_day,
        days_per_week,
        senior_productivity_factor,
        effective_utilization,
        buffer_percentage
    ):
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

