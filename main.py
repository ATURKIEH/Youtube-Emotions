#Aref Turkieh
# main script that process youtube emotions and that generates an emotion report

import os.path
from emotions import *

VALID_COUNTRIES = ['bangladesh', 'brazil', 'canada', 'china', 'egypt',
                   'france', 'germany', 'india', 'iran', 'japan', 'mexico',
                   'nigeria', 'pakistan', 'russia', 'south korea', 'turkey',
                   'united kingdom', 'united states']

def ask_user_for_input():
    #this function collects the user input for the file names and filters and validating eadh input

    keyword_file = input("Input keyword file (ending in .tsv): ")
    #ask the user to input a file that ends with .tsv
    if not keyword_file.endswith('.tsv'):
        raise ValueError("Keyword file does not end in .tsv!")
    #if the file doesnt end with .tsv it raises value error and prints out a phrase
    if not os.path.exists(keyword_file):
        raise IOError(f"{keyword_file} does not exist!")
    # if the file does not exist it raises the IOError

    comments_file = input("Input comment file (ending in .csv): ")
    # ask the user to input a file that ends with .csv
    if not comments_file.endswith('.csv'):
        raise ValueError("Comments file does not end in .csv!")
    # if the file doesnt end with .csv it raises value error and prints out a phrase
    if not os.path.exists(comments_file):
        raise IOError(f"{comments_file} does not exist!")
    # if the file does not exist it raises the IOError

    country = input("Input a country to analyze (or \"all\" for all countries): ").lower()
    #ask the user to input a country or all for all countries
    if country != "all" and country not in VALID_COUNTRIES:
        raise ValueError(f"{country} is not a valid country to filter by!")
    #it raises a valueError if the country isnt in valid countries

    report_file = input("Input the name of the report file (ending in .txt): ")
    # ask the user to input the report file name that ends with .txt
    if not report_file.endswith('.txt'):
        raise ValueError("Report file does not end in .txt!")
    # same process as the last inputs, raises valueError
    if os.path.exists(report_file):
        raise IOError(f"{report_file} already exists!")
    #raises IOError if it doesnt exist

    return keyword_file, comments_file, country, report_file

def main():
    #the main function is for processing the user input by analyzing comments and then by generating the report

    while True:
        try:
            keyword_file, comments_file, country, report_file = ask_user_for_input()
            #the ask_user_for_input prompts the user to input the keyword file, comments file, country and report file
            keywords = make_keyword_dict(keyword_file)
            #this reads the keyword file
            comments = make_comments_list(country, comments_file)
            #this reads the comments file
            most_common_emotion = make_report(comments, keywords, report_file)
            #this analyzes the filtered comments to determine how many comments align with each emotion
            print(f"Most common emotion is: {most_common_emotion}")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
    # runs the main function
