import data.importer as imp
import data.plotter as plotter

activity_summaries_df = imp.gather_activity_summaries()


def get_total_calories():
    activity_summaries_df['activeEnergyBurned'].sum()


def total_calories_burned_by_day():
    return activity_summaries_df.groupby([activity_summaries_df['date'].dt.dayofweek])['activeEnergyBurned'].sum()


def total_calories_burned_by_month():
    return activity_summaries_df.groupby([activity_summaries_df['date'].dt.month])['activeEnergyBurned'].sum()


def total_calories_burned_by_year():
    return activity_summaries_df.groupby([activity_summaries_df['date'].dt.year])['activeEnergyBurned'].sum()


def mean_calories_burned_by_day():
    return activity_summaries_df.groupby([activity_summaries_df['date'].dt.dayofweek])['activeEnergyBurned'].mean()


def mean_calories_burned_by_month():
    return activity_summaries_df.groupby([activity_summaries_df['date'].dt.month])['activeEnergyBurned'].mean()


def mean_calories_burned_by_year():
    return activity_summaries_df.groupby([activity_summaries_df['date'].dt.year])['activeEnergyBurned'].mean()


if __name__ == "__main__":
    plotter.bar_plot_daily(mean_calories_burned_by_day(), "Calories burned (kcal)", "Mean Calories Burned by Day")
    get_total_calories()