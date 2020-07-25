import data.importer as imp
import matplotlib.pyplot as plt
import seaborn as sns
from function_registrar import procurable

heart_df = imp.get_heart_rates()


@procurable("mean heart rate by hour", ["heart", "rate", "hour", "hourly", "bpm", "beats"])
def mean_rate_by_hour():
    return heart_df.groupby([heart_df['date'].dt.hour])['bpm'].mean()


@procurable("mean heart rate by month", ["heart", "rate", "month", "monthly", "bpm", "beats"])
def mean_rate_by_day_month():
    return heart_df.groupby([heart_df['date'].dt.day])['bpm'].mean()


@procurable("mean heart rate by week", ["heart", "rate", "week", "weekly", "bpm", "beats"])
def mean_rate_by_day_week():
    return heart_df.groupby([heart_df['date'].dt.dayofweek])['bpm'].mean()


if __name__ == "__main__":
    df_bpm_by_hour = mean_rate_by_hour()
    sns.set(style="whitegrid")
    ax = sns.barplot(x=df_bpm_by_hour.index, y=df_bpm_by_hour.values)
    plt.xlabel("Hour of the Day")
    plt.ylabel("Mean BPM")
    plt.title("Average BPM by Hour", pad=14)
    plt.savefig("hourly-bpm.jpg")
    plt.show()
