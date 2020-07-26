import pandas as pd
import database
from database.tables import Table


def heart_data():
    return pd.read_sql("SELECT * FROM {}".format(Table.HEART.name.lower()), database.engine)


def activity_summaries():
    return pd.read_sql("SELECT * FROM {}".format(Table.ACTIVITY_SUMMARIES.name.lower()), database.engine)


def swimming():
    return pd.read_sql("SELECT * FROM {}".format(Table.SWIMMING.name.lower()), database.engine)


def calories():
    return pd.read_sql("SELECT * FROM {}".format(Table.CALORIES.name.lower()), database.engine)


def swimming_laps():
    return pd.read_sql("SELECT * FROM {}".format(Table.SWIMMING_LAPS.name.lower()), database.engine)


def swimming_strokes():
    return pd.read_sql("SELECT * FROM {}".format(Table.SWIMMING_STROKES.name.lower()), database.engine)


def env_audio_exposure():
    return pd.read_sql("SELECT * FROM {}".format(Table.ENV_AUDIO_EXPOSURE.name.lower()), database.engine)


def phones_audio_exposure():
    return pd.read_sql("SELECT * FROM {}".format(Table.PHONES_AUDIO_EXPOSURE.name.lower()), database.engine)
