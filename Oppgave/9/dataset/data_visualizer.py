import matplotlib.pyplot as plt

class DataVisualizer:
    def __init__(self, df):
        self.df = df

    def simple_visualization(self, column_name):
        """
        Generate a simple visualization for a specified column using matplotlib.
        """
        plt.plot(self.df[column_name])
        plt.title(f'Simple visualization of {column_name}')
        plt.show()

    def advanced_visualization(self, column_name):
        """
        Generate an advanced visualization for a specified column using seaborn.
        """
        import seaborn as sns
        sns.histplot(self.df[column_name])
        plt.title(f'Advanced visualization of {column_name}')
        plt.show()

    def scatter_plot(self, x_column, y_column):
        """
        Generate a scatter plot between two columns using matplotlib.
        """
        plt.scatter(self.df[x_column], self.df[y_column])
        plt.title(f'Scatter plot between {x_column} and {y_column}')
        plt.show()

    def pair_plot(self, columns):
        """
        Generate a pair plot for specified columns using seaborn.
        """
        import seaborn as sns
        sns.pairplot(self.df[columns])
        plt.title(f'Pair plot of {columns}')
        plt.show()

    def correlation_matrix(self):
        """
        Generate a correlation matrix for the DataFrame using seaborn.
        """
        import seaborn as sns
        sns.heatmap(self.df.corr(), annot=True)
        plt.title('Correlation matrix')
        plt.show()

    def box_plot(self, x_column, y_column):
        """
        Generate a box plot for specified columns using seaborn.
        """
        import seaborn as sns
        sns.boxplot(x=self.df[x_column], y=self.df[y_column])
        plt.title(f'Box plot of {x_column} and {y_column}')
        plt.show()

    def count_plot(self, column_name):
        """
        Generate a count plot for a specified column using seaborn.
        """
        import seaborn as sns
        sns.countplot(x=self.df[column_name])
        plt.title(f'Count plot of {column_name}')
        plt.show()

    def violin_plot(self, x_column, y_column):
        """
        Generate a violin plot for specified columns using seaborn.
        """
        import seaborn as sns
        sns.violinplot(x=self.df[x_column], y=self.df[y_column])
        plt.title(f'Violin plot of {x_column} and {y_column}')
        plt.show()

    def lm_plot(self, x_column, y_column):
        """
        Generate a linear regression plot between two columns using seaborn.
        """
        import seaborn as sns
        sns.lmplot(x=x_column, y=y_column, data=self.df)
        plt.title(f'Linear regression plot between {x_column} and {y_column}')
        plt.show()

    def joint_plot(self, x_column, y_column):
        """
        Generate a joint plot between two columns using seaborn.
        """
        import seaborn as sns
        sns.jointplot(x=x_column, y=y_column, data=self.df)
        plt.title(f'Joint plot of {x_column} and {y_column}')
        plt.show()

    def pie_chart(self, column_name):
        """
        Generate a pie chart for a specified column using matplotlib.
        """
        counts = self.df[column_name].value_counts()
        plt.pie(counts, labels=counts.index, autopct='%1.1f%%')
        plt.title(f'Pie chart of {column_name}')
        plt.show()

    def histogram(self, column_name):
        """
        Generate a histogram for a specified column using matplotlib.
        """
        plt.hist(self.df[column_name], bins=20, color='skyblue', edgecolor='black', alpha=0.7)

        plt.title(f'Histogram of {column_name}')
        plt.show()