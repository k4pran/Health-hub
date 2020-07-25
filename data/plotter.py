import matplotlib.pyplot as plt
import seaborn as sns

from activity.swimming import get_minutes_per_100m

sns.set()

days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

def plot_scatter(x, y, x_label="", y_label="", title=""):
    sns.scatterplot(x, y)
    sns.set(style="whitegrid")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title, pad=14)


def bar_plot_daily(values, values_label="", title=""):
    assert len(values) == 7

    sns.set(style="whitegrid")
    sns.barplot(x=days, y=values)
    plt.xlabel("Day of the Week")
    plt.ylabel(values_label)
    plt.title(title, pad=14)
    plt.savefig(title + ".jpg")
    plt.show()

if __name__ == "__main__":
    speeds = get_minutes_per_100m()
    plot_scatter(speeds.index, speeds.values, "Chronology", "minutes per 100m", "Swimming Session Paces")