def score_margin(margin):
    if margin > 0.25:
        return 5
    elif margin > 0.20:
        return 4
    elif margin > 0.15:
        return 3
    elif margin > 0.10:
        return 2
    else:
        return 1