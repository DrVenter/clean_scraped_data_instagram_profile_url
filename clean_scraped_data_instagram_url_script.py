import numpy as np
import pandas as pd

#Open file and create matrix
file_name = "raw_scraped_data_instagram_url.txt"
file = open(file_name, errors="ignore")

matrix = []
for row in file:
    matrix.append(row.strip("\n"))
for column in range(len(matrix)):
    matrix[column] = matrix[column].split("\t")

matrix = np.array(matrix)

#remove empty queries
empty_queries = np.where(matrix[ : , 0] == "")
matrix = np.delete(matrix, empty_queries, axis=0)


#find heading index
def find_heading_title(title):
    heading_row = 0
    title_index_tuple = np.where(matrix[heading_row] == title)
    title_index = title_index_tuple[0]

    return title_index

#remove unnecessary columns and place in correct order
headings = ["query", "instagramUrl", "description", "title"]
heading_indexes = list(map(find_heading_title, headings))
heading_row = 0
columns_to_remove = []
for x in range(len(matrix[heading_row])):
    if x not in heading_indexes:
        columns_to_remove.append(x)

matrix = np.delete(matrix, columns_to_remove, axis = 1)

print(matrix)