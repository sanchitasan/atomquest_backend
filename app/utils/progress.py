def calculate_progress(goal, actual_value):

    target = goal.target_value

    if goal.uom.lower() == "min":

        if target == 0:
            return 0

        return round(
            (actual_value / target) * 100,
            2
        )

    elif goal.uom.lower() == "max":

        if actual_value == 0:
            return 100

        return round(
            (target / actual_value) * 100,
            2
        )

    elif goal.uom.lower() == "zero":

        if actual_value == 0:
            return 100

        return 0

    else:
        return 0

def calculate_status(progress_score):

    if progress_score >= 100:
        return "Completed"

    elif progress_score >= 50:
        return "On Track"

    return "Not Started"