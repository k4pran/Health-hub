import pandas as pd

import database


def heart_data():
    return pd.read_sql("SELECT * FROM 'heart'", database.engine)