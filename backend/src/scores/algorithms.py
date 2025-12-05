from backend.src.scores.schemas import ScoresParameters


async def compute_score(
        user_driver_prediction: int,
        mygrid_driver_prediction: int,
        driver_result: int,
        grid_size: int,
        parameters: ScoresParameters):
    """
    Returns the score computed from one user driver predictions in function of
    our prediction and the actual result of the driver.
    :param user_driver_prediction: user prediction
    :param mygrid_driver_prediction: server prediction
    :param driver_result: session result for this driver
    :param grid_size: how many drivers registered in the session
    :param parameters: parameters needed to compute scores
    :return: the computed score
    """
    # Get datas from inputs
    difference = abs(user_driver_prediction - driver_result)
    rarity = abs(user_driver_prediction - mygrid_driver_prediction)
    final_score = 0

    # For every parameter, add points to the final score
    # Use if statement to separate rarity and quality computation.
    # If the difference is higher than the margin allowed
    # by a parameter, just skip it.
    for param in parameters.__class_vars__:
        max_margin = len(param)-1

        if difference > max_margin:
            continue

        param_points = getattr(parameters, param)
        param_points.sort(reverse=True)

        if "rarity" in param:
            # In case of a rarity parameter, because it will come
            # in a rarity{margin} format, use that margin number
            # to check whether we are in the right case of rarity or
            # whether we have to skip the computation.
            rarity_margin = int(param.removeprefix("rarity"))
            if rarity_margin == rarity:
                final_score += param_points[difference]
            continue

        match param:
            case "position":
                final_score += param_points[difference]
            case "top10":
                final_score += param_points[difference] if user_driver_prediction <= 10 else 0
            case "top5":
                final_score += param_points[difference] if user_driver_prediction <= 5 else 0
            case "top3":
                final_score += param_points[difference] if user_driver_prediction <= 3 else 0
            case "top1":
                final_score += param_points[difference] if user_driver_prediction == 1 else 0
            case "last":
                final_score += param_points[difference] if user_driver_prediction == grid_size else 0
            case "penultimate":
                final_score += param_points[difference] if user_driver_prediction == grid_size-1 else 0

    return final_score
