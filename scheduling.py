from datetime import date

from dateutil.relativedelta import relativedelta

# This function allows me to get the interval between
# months when provided with a frequency.
def get_month_interval(frequency: str) -> int:
    intervals = {
        "Annual": 12,
        "Semi-Annual": 6,
        "Quarterly": 3,
    }

    try:
        return intervals[frequency]
    except KeyError:
        raise ValueError(f"Invalid frequency {frequency}")


# This function accepts the start date of the inspection,
# the frequency of the inspection and when
def get_next_scheduled_date(
        start_date: date,
        frequency: str,
        current_scheduled_date: date
) -> date:

    months = get_month_interval(frequency)
    return current_scheduled_date + relativedelta(months=months)

def get_cycle(
        start_date: date,
        scheduled_date: date,
        frequency: str,
) -> str:

    months = get_month_interval(frequency)

    months_past = (
    (scheduled_date.year - start_date.year) * 12
    + scheduled_date.month
    - start_date.month
    )

    cycles_per_year = 12 // months

    position = (months_past // months) % cycles_per_year + 1

    if cycles_per_year == 1:
        return "1/1"

    return f"{position}/{cycles_per_year}"

def generate_schedule(
        start_date: date,
        frequency: str,
        number_of_inspections: int,
) -> list[dict]:

    schedule = []

    scheduled_date = start_date

    for _ in range(number_of_inspections):
        cycle = get_cycle(
            start_date,
            scheduled_date,
            frequency,
        )

        schedule.append(
            {
                "scheduled_date": scheduled_date,
                "cycle": cycle,
            }
        )

        scheduled_date = get_next_scheduled_date(
            start_date,
            frequency,
            scheduled_date,
        )

    return schedule

#########################################################
