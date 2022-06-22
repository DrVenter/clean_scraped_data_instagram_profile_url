import numpy as np
import pandas as pd

class CleanInstagram:
    matrix = []
    check_string_matrix = []
    f_f_p = []
    instagram_handles = []
    email_address = []

    def __init__(self, file_name):
        self.file_name = file_name
        file = open(self.file_name, errors="ignore")

        row_delimiter = "\n"
        column_delimiter = "\t"

        for row in file: self.matrix.append(row.strip(row_delimiter))
        for column in range(len(self.matrix)): self.matrix[column] = self.matrix[column].split(column_delimiter)
        
        self.matrix = np.array(self.matrix)

    def remove_empty_queries(self):
        query_column = 0

        empty_queries = np.where(self.matrix[ : , query_column] == "")
        self.matrix = np.delete(self.matrix, empty_queries, axis=0)

    def find_heading_index(self, heading_title):
        heading_row = 0

        title_index_tuple = np.where(self.matrix[heading_row] == heading_title)
        title_index = title_index_tuple[0]

        return title_index

    def create_check_string_matrix(self):
        description = self.find_heading_index("description")
        title = self.find_heading_index("title")
        inner_element = 0
        heading_row = 0
        title_description = [["title and description"]]

        for row in range(heading_row + 1, len(self.matrix)):
            check_string = (str(self.matrix[row, description][inner_element]) + " " + str(self.matrix[row, title][inner_element])).replace("," , "").lower().split(" ")
            title_description.append(check_string)

        self.check_string_matrix = title_description

    def remove_unneeded_columns(self, heading_titles = ["query", "instagramUrl"]):
        heading_indexes = list(map(self.find_heading_index, heading_titles))
        heading_row = 0
        columns_to_remove = []

        for column in range(len(self.matrix[heading_row])):
            if column not in heading_indexes: columns_to_remove.append(column)

        self.matrix = np.delete(self.matrix, columns_to_remove, axis=1)
    
    def check_number_validity(self, string):
        items_usually_in_numbers = [".", ",", "k"]
        
        for item in items_usually_in_numbers:
            if item in string: string = string.replace(item, "")
        
        return string.isdigit()

    def create_follower_following_posts_matrix(self):
        keywords = ["followers", "following", "posts"]
        heading_row = 0
        f_f_p = [["followers", "following", "posts"]]

        for row in range(heading_row + 1, len(self.matrix)):
            rows = ["", "", ""]
            check_string = self.check_string_matrix[row]

            for keyword in range(len(keywords)):
                if keywords[keyword] in check_string: 
                    string_start = 0
                    string_end = len(check_string) - 1
                    count = check_string.count(keywords[keyword])

                    rows[keyword] = check_string[check_string.index(keywords[keyword]) - 1]

                    while self.check_number_validity(rows[keyword]) == False and string_start < string_end and count > 1:
                        string_start = check_string.index(keywords[keyword]) + 1
                        count = check_string[string_start:].count(keywords[keyword])

                        rows[keyword] = check_string[check_string[string_start:].index(keywords[keyword]) - 1]
                    if self.check_number_validity(rows[keyword]) == False: rows[keyword] = ""

                else: 
                    rows[keyword] = ""
            f_f_p.append(rows)
        self.f_f_p = np.array(f_f_p)

    def create_instagram_handle_email_matrix(self):
        instagram_handles = [["Instagram Handles"]]
        email_address = [["Email Addresses"]]
        column_heading = 0

        for row in range(column_heading + 1, len(self.matrix)):
            check_string = self.check_string_matrix[row]
            handles = ""
            email = ""

            for word in range(len(check_string)):
                check_string[word] = check_string[word].strip("â€œ¢/()").replace("artists:", "")

                if check_string[word].startswith("@"): handles = handles + " " + check_string[word].strip(".")
                if "@" in check_string[word] and not check_string[word].startswith("@"): email = email + " " + check_string[word].strip(".")

            handles = handles.strip().split()
            handles = list(dict.fromkeys(handles))
            handles = " ".join(handles)
            
            instagram_handles.append([handles])

            email = email.strip()
            email_address.append([email])
        self.instagram_handles = np.array(instagram_handles)
        self.email_address = np.array(email_address)
    
    def combine_matrices(self):
        self.matrix = np.concatenate((self.matrix, self.f_f_p, self.instagram_handles, self.email_address), axis=1)

    def matrix_to_csv(self):
        data_frame = pd.DataFrame(self.matrix)
        data_frame.to_csv(f"cleaned_{self.file_name}.csv", index=False, header=False)

data = CleanInstagram("scraped_data_instagram_url.txt")
data.remove_empty_queries()
data.create_check_string_matrix()
data.remove_unneeded_columns()
data.create_follower_following_posts_matrix()
data.create_instagram_handle_email_matrix()
data.combine_matrices()
data.matrix_to_csv()