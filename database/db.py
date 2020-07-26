import health
import activity
from database import engine
from database.tables import Table


def update_heart_table():
    df = health.heart_df
    return update_table(df, Table.HEART)


def update_activity_summaries_table():
    df = health.activity_summaries_df
    return update_table(df, Table.ACTIVITY_SUMMARIES)


def update_calories_table():
    df = health.calories_burned
    return update_table(df, Table.CALORIES)


def update_swimming_table():
    df = activity.swimming_laps_df
    return update_table(df, Table.SWIMMING)


def update_swimming_laps_table():
    df = activity.swimming_laps_df
    return update_table(df, Table.SWIMMING_LAPS)


def update_swimming_strokes_table():
    df = activity.swimming_stroke_counts
    return update_table(df, Table.SWIMMING_STROKES)


def update_env_audio_exposure_table():
    df = health.env_audio_exposure_df
    return update_table(df, Table.ENV_AUDIO_EXPOSURE)


def update_phones_audio_exposure_table():
    df = health.phones_audio_exposure_df
    return update_table(df, Table.PHONES_AUDIO_EXPOSURE)


def update_table(df, table):
    table_name = table.name.lower()
    try:
        df.to_sql(table_name, engine, if_exists='replace')
        return {table_name: 'SUCCESS'}
    except Exception as e:
        print(e)
        return {table_name: 'FAILED'}


def update_all():
    results = {}
    results.update(update_heart_table())
    results.update(update_activity_summaries_table())
    results.update(update_calories_table())
    results.update(update_swimming_table())
    results.update(update_swimming_laps_table())
    results.update(update_swimming_strokes_table())
    results.update(update_env_audio_exposure_table())
    results.update(update_phones_audio_exposure_table())
    return results


if __name__ == "__main__":
    update_all()
