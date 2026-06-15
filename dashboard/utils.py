import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt


def generate_chart(
        df,
        chart_type,
        x_column,
        y_column,
        output_path):

    plt.figure(figsize=(8, 5))

    if chart_type == "bar":

        plt.bar(
            df[x_column],
            df[y_column]
        )

    elif chart_type == "line":

        plt.plot(
            df[x_column],
            df[y_column]
        )

    elif chart_type == "scatter":

        plt.scatter(
            df[x_column],
            df[y_column]
        )

    elif chart_type == "histogram":

        plt.hist(
            df[x_column]
        )

    elif chart_type == "pie":

        plt.pie(
            df[y_column],
            labels=df[x_column],
            autopct='%1.1f%%'
        )

    plt.title(chart_type.upper())

    plt.tight_layout()

    plt.savefig(output_path)

    plt.close()