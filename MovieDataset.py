"""
Program that reads data from IMDB's top 5000 movies, and creates multiple functions which then does analysis on said
data. Uses pandas, matplotlib, seaborn and ast to create plots.

author: Matas Aleksas
version: 1.0.0
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
from collections import Counter

"""
Creates the data frame, converts dates into datetime, and cleans any invalid rows or duplicate columns.

:returns Returns the created and cleaned dataframe.
"""
def create_data():
    # Reads the input data and puts it into a df (Data Frame)
    # Gets rid of unneeded columns
    # Converts all the release dates in the release date column into a more readable date time object
    # Gets rid of any rows that contain NaT to clean the data
    # Gets rid of any duplicates


    df = pd.read_csv("tmdb_5000_movies.csv")

    df = df.drop(columns=["homepage", "tagline"])

    df["release_date"] = pd.to_datetime(df["release_date"], errors='coerce')

    df = df.dropna(subset=["release_date"])
    df = df.drop_duplicates()

    return df

"""
Plots a list of the most common genres in the dataframe.
"""
def most_common_genre():
    df = create_data()

    # Gets the genre column, delete any invalid rows, apply a function which coverts the literal string to a dictionary
    # Then gets just the genres from that dictionary
    genre_list = df["genres"].dropna().apply(lambda x: [i["name"] for i in ast.literal_eval(x)])
    all_genres = [genre for sublist in genre_list for genre in sublist]
    genre_count = pd.Series(Counter(all_genres)).sort_values(ascending=False)

    # Creates the plot and shows it
    genre_count.plot(kind = "bar", title = "Most Common Genres")
    plt.xlabel("Genre")
    plt.ylabel("Number Of Movies")
    plt.tight_layout()
    plt.show()

"""
Gets the trend of the movies released over time.
"""
def movie_trend_time():
    df = create_data()

    # Gets the count of the amount of items with that release year
    # Plots it on a graph
    df["release_year"] = df["release_date"].dt.year
    df["release_year"].value_counts().sort_index().plot(kind = "line", title = "Movie Trend Over Time")

    plt.xlabel("Year")
    plt.ylabel("Number Of Movies Released")
    plt.tight_layout()
    plt.show()

"""
Gets what movies made the most money over time.
"""
def most_money():
    df = create_data()

    # Gets the profit of a movie by doing the revenue - budget
    # Gets the top ten movies with the highest budget
    # Prints out the location of that movie on the list, the name, and the profit which it generated
    df["profit"] = df["revenue"] - df["budget"]
    top_ten = df.sort_values("profit", ascending=False).head(10)
    print(top_ten[['title', 'profit']])

"""
Gets the correlation of the budget vs the rating the movie gets.
"""
def correlation_profit_rating():
    df = create_data()
    df = df[df["budget"] > 1_000_000] # filter out noise, any movies with less than a million budget

    # Creates a scatter plot of the budget vs rating
    # Then scales it on a exponential scale since we're dealing with millions of dollars
    sns.scatterplot(data=df, x="budget", y="vote_average")
    plt.title("Budget Vs. Rating")
    plt.xscale("log")
    plt.show()

"""
Creates a bar plot of the average ratings of genres.
"""
def average_rating_per_genre():
    df = create_data()

    # Parse the genre list into a list of names and expand the genre list into a new column in the data frame
    genre_list = df["genres"].dropna().apply(lambda x: [i["name"] for i in ast.literal_eval(x)])
    df = df.assign(genres_expanded=genre_list)

    # Explode to separate rows per genre
    df_exploded = df.explode("genres_expanded")

    # Group genre and calculate the average rating of each genre`
    avg_rating = df_exploded.groupby("genres_expanded")["vote_average"].mean().sort_values(ascending=False)

    # Plot the findings
    avg_rating.plot(kind="bar", title="Average Rating by Genre")
    plt.xlabel("Genre")
    plt.ylabel("Average Rating")
    plt.tight_layout()
    plt.show()

"""
Shows the top production companies and the amount of movies they have created over time.
"""
def top_production_companies():
    df = create_data()

    # Parse the names of the production companies and count the amount of movies they each have
    companies = df['production_companies'].dropna().apply(lambda x: [i['name'] for i in ast.literal_eval(x)])
    all_companies = [c for sublist in companies for c in sublist]
    pd.Series(Counter(all_companies)).sort_values(ascending=False).head(10).plot(kind='bar',
                                                                                 title='Top Production Companies')

    # Plot the findings
    plt.xlabel("Production Companies")
    plt.ylabel("Number of Movies")
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    while True:
        print("Movie data menu:\n")
        print("1. Show Most Common Genres")
        print("2. Show Movie Trend Over Time")
        print("3. Show Top 10 Most Profitable Movies")
        print("4. Show Budget vs. Rating Scatter Plot")
        print("5. Show Average Rating by Genre")
        print("6. Amount Of Movies Top Production Companies Made")
        print("0. Exit\n")

        choice = input("Enter your choice (0-6): ")

        if choice == '1':
            most_common_genre()
        elif choice == '2':
            movie_trend_time()
        elif choice == '3':
            most_money()
        elif choice == '4':
            correlation_profit_rating()
        elif choice == '5':
            average_rating_per_genre()
        elif choice == '6':
            top_production_companies()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number from 0 to 6.")
