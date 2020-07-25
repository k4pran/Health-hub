import health
from database import engine


def update_heart_table():
    health.heart_df.to_sql("heart", engine, if_exists='replace')


def update_activity_summaries_table():
    health.activity_summaries_df.to_sql("activity_summaries", engine, if_exists='replace')


def update_swimming_table():
    health.swimming_df.to_sql("swimming", engine, if_exists='replace')


def update_all():
    update_heart_table()
    update_activity_summaries_table()
    update_swimming_table()


if __name__ == "__main__":
    update_all()
