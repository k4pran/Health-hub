from data.importer import get_swim_activities, get_swim_stroke_counts, get_swim_laps

swimming_df = get_swim_activities()
swimming_laps_df = get_swim_laps()
swimming_stroke_counts = get_swim_stroke_counts()


def get_distances():
    """
    :return: swim distances in meters
    """
    return swimming_df['distance'].apply(lambda d: d * 1000)


def get_total_distance():
    """
    :return: the total distance of all swims in meters
    """
    return get_distances().sum()


def get_mean_distance():
    """
    :return: the mean distance of swims in meters
    """
    return get_distances().mean()


def get_minutes_per_100m():
    return (swimming_df['duration'] / get_distances()) * 100