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

#create matrix for followers, following and posts
placeholder = np.zeros((len(matrix), 3), dtype="S")

placeholder[0] = ["Followers", "Following", "Posts"]

description = find_heading_title("description")
title = find_heading_title("title")

def check_validity(string):
    items_usualy_in_number = [".", ",", "k"]
    k = 0
    for x in items_usualy_in_number:
        if x in string: string = string.replace(x, "")
    
    return string.isdigit()

i = 1
while i < len(matrix):
    check_string = (str(matrix[i, description][0]) + " " + str(matrix[i, title][0])).replace("," , "").lower().split(" ")
    keyword = ["followers", "following", "posts"]
    row = ["", "", ""]

    j = 0
    while j < len(keyword): #need to change these stupid while loops to for loops
        if keyword[j] in check_string: 
            string_start = 0
            string_end = len(check_string) - 1
            count = check_string.count(keyword[j])

            row[j] = check_string[check_string.index(keyword[j]) - 1]

            while check_validity(row[j]) == False and string_start < string_end and count > 1:
                string_start = check_string.index(keyword[j]) + 1
                count = check_string[string_start:].count(keyword[j])

                row[j] = check_string[check_string[string_start:].index(keyword[j]) - 1]
                #print(row[j], check_string.count(keyword[j]))

            if check_validity(row[j]) == False: row[j] = ""
                
                
        else: 
            row[j] = ""
        j+=1
    print(row)
    i+=1

#print(placeholder)