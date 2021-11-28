import numpy as np
import pandas as pd
from sklearn import neighbors
from sklearn.preprocessing import MinMaxScaler
import warnings

warnings.filterwarnings("ignore")

df = pd.read_csv('market/data/newbooks.csv', error_bad_lines=False)


def send_books(value):
    my_dict = {}
    x = 0
    value = value.lower()

    if value == "mostrated":
        my_array = df.sort_values(
            'ratings_count', ascending=False).head(10).index
    elif value == "newbooks":
        my_array = df.sort_values(
            'publication_date', ascending=False).head(10).index
    elif value == "bestselling":
        my_array = df.sort_values(
            'text_reviews_count', ascending=False).head(10).index
    else:
        return {"msg": "type error:not found"}

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


def print_similar_books(query):
    try:
        my_dict = {}
        x = 0
        found_id = df[df["title"] == query].bookID.tolist()[0]
        found_index = get_index_from_name(query)
        for id in indicesKNN[found_index][1:]:
            my_dict[x] = df.iloc[id].to_json()
            x = x + 1
        return {"msg": "ok", "data": my_dict, "search_book_id": found_id, "search_book_name": query}
    except Exception as e:
        print(e)
        return {"msg": "Error"}


def get_details(book_id):
    book_id = int(book_id)
    my_dict = df.iloc[df[df["bookID"] == book_id].index.tolist()[0]].to_json()
    return my_dict


all_books_names = list(df.title.values)


def get_names_and_id_from_partial_name(partial):
    my_dict = {}
    x = 0
    for name in all_books_names:
        if partial in name:
            my_dict[x] = {"name": name, "index": all_books_names.index(name)}
            x = x + 1
    return my_dict
