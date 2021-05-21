import numpy as np
import pandas as pd
from sklearn import neighbors
from sklearn.preprocessing import MinMaxScaler

import warnings

warnings.filterwarnings("ignore")

df = pd.read_csv('./newbooks.csv', error_bad_lines=False)


def most_rated_books():
    my_dict = {}
    x = 0
    most_rated = df.sort_values('ratings_count', ascending=False).head(10)
    my_array = most_rated.index
    for id in my_array:
        my_dict[x] = df.iloc[id].to_json()
        x = x + 1
    return my_dict


def new_books():
    my_dict = {}
    x = 0
    new_book = df.sort_values('publication_date', ascending=False).head(10)
    my_array = new_book.index
    for id in my_array:
        my_dict[x] = df.iloc[id].to_json()
        x = x + 1
    return my_dict


def best_selling():
    my_dict = {}
    x = 0
    best_selling = df.sort_values('text_reviews_count', ascending=False).head(10)
    my_array = best_selling.index
    for id in my_array:
        my_dict[x] = df.iloc[id].to_json()
        x = x + 1
    return my_dict


def segregation(df):
    values = []

    for val in df.average_rating:
        if val >= 0 and val <= 1:
            values.append("Between 0 and 1")
        elif val > 1 and val <= 2:
            values.append("Between 1 and 2")
        elif val > 2 and val <= 3:
            values.append("Between 2 and 3")
        elif val > 3 and val <= 4:
            values.append("Between 3 and 4")
        elif val > 4 and val <= 5:
            values.append("Between 4 and 5")
        else:
            values.append("NaN")

    return values


df['Ratings_Dist'] = segregation(df)

books_features = pd.concat(
    [df['Ratings_Dist'].str.get_dummies(sep=","),
     df['average_rating'],
     df['ratings_count']],
    axis=1)

min_max_scaler = MinMaxScaler()
books_features = min_max_scaler.fit_transform(books_features)
np.round(books_features, 2)

model = neighbors.NearestNeighbors(n_neighbors=11, algorithm='ball_tree')
model.fit(books_features)
distance, indicesKNN = model.kneighbors(books_features)


def get_index_from_name(name):
    return df[df["title"] == name].index.tolist()[0]


def print_similar_books(query=None):
    mydict = {}
    x = 0
    if query:
        found_id = get_index_from_name(query)
        for id in indicesKNN[found_id][1:]:
            mydict[x] = df.iloc[id].to_json()
            x = x + 1
    return mydict