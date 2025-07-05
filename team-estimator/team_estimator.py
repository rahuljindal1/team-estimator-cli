class TeamOptimizer:
    def __init__(self):
        pass

    def calculate_team_size(
        self,
        man_hours_required: float,
        duration_months: int,
        hours_per_day: int,
        work_days_per_month: int,
        senior_productivity_factor: float,
        max_juniors: int,
        max_seniors: int,
        min_seniors: int,
        total_qa: int,
        total_designers: int,
        effective_utilization: float,
        buffer_percentage: float,
    ):
        """
        Calculate optimal team size for given project effort.

        Parameters:
        ----------
        man_hours_required
            The estimated total development man-hours needed to deliver the project *before* adding buffer.

        duration_months
            Total project duration in months available to deliver the required work.

        hours_per_day
            Number of productive working hours per developer per day.

        work_days_per_month
            Number of effective working days in a month (after accounting for weekends, holidays, etc.).

        senior_productivity_factor
            Factor indicating how much more productive a senior developer is compared to a junior.
            For example, 1.5 means a senior contributes 1.5 times as much as a junior.

        max_juniors
            Maximum number of junior developers you can allocate to this project.

        max_seniors
            Maximum number of senior developers you can allocate to this project.

        min_seniors
            Minimum number of seniors developers need to allocate to this project.

        total_qa
            Number of QA resources required (does not contribute to development man-hours directly).

        total_designers
            Number of designers required (does not contribute to development man-hours directly).

        effective_utilization
            Expected utilization percentage of each developer (e.g., 0.8 means 80% of total time is productive).

        buffer_percentage
            Risk buffer to handle unforeseen tasks, rework, delays, etc.
            For example, 0.2 adds 20% more effort to the estimated man-hours.
        """
        # Increase required effort by buffer to safeguard against risks
        man_hours_required *= 1 + buffer_percentage

        hours_per_month_per_dev = work_days_per_month * hours_per_day
        total_hours_per_dev = hours_per_month_per_dev * duration_months
        total_hours_per_dev *= effective_utilization

        best_combo = None

        for seniors in range(min_seniors, max_seniors + 1):
            for juniors in range(0, max_juniors + 1):
                total_effective_hours = (
                    seniors * senior_productivity_factor + juniors
                ) * total_hours_per_dev

                if total_effective_hours >= man_hours_required:
                    if (
                        not best_combo
                        or seniors < best_combo["seniors"]
                        or (
                            seniors == best_combo["seniors"]
                            and juniors < best_combo["juniors"]
                        )
                    ):
                        best_combo = {
                            "seniors": seniors,
                            "juniors": juniors,
                            "capacity": total_effective_hours,
                        }

        if best_combo:
            print(
                f"\n✅ Optimal team for {int(man_hours_required)} man-hours in {duration_months} months "
                f"(incl. {int(buffer_percentage * 100)}% buffer, {int(effective_utilization * 100)}% utilization):"
            )
            print(
                f"  Developers: {best_combo['seniors']} seniors, {best_combo['juniors']} juniors"
            )
            print(f"  QA: {total_qa} (does not add capacity)")
            print(f"  Designers: {total_designers} (does not add capacity)")
            print(
                f"  ➜ Total effective dev capacity: {int(best_combo['capacity'])} man-hours"
            )
        else:
            print(
                "\n❌ No feasible team found under given constraints. Increase duration or role caps."
            )

    def calculate_weeks_needed(
        self,
        man_hours_required: float,
        total_seniors: int,
        total_juniors: int,
        hours_per_day: int,
        days_per_week: int,
        senior_productivity_factor: float,
        effective_utilization: float,
        buffer_percentage: float,
    ):
        man_hours_required *= 1 + buffer_percentage

        total_weekly_capacity = (
            ((total_seniors * senior_productivity_factor) + total_juniors)
            * hours_per_day
            * days_per_week
            * effective_utilization
        )

        if total_weekly_capacity <= 0:
            print("\n❌ Invalid team config — no capacity.")
            return

        weeks_needed = man_hours_required / total_weekly_capacity

        print(
            f"\n✅ Estimated delivery for fixed team (incl. {int(buffer_percentage * 100)}% buffer, {int(effective_utilization * 100)}% utilization):"
        )
        print(f"  Seniors: {total_seniors}")
        print(f"  Juniors: {total_juniors}")
        print(f"  ➜ Weekly dev capacity: {int(total_weekly_capacity)} man-hours/week")
        print(
            f"  ➜ Delivery time: {weeks_needed:.1f} weeks for {int(man_hours_required)} man-hours"
        )
