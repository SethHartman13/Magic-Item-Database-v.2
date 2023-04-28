# Request libraries
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

# Built in libraries
import json
import os
import sys

# Created modules
from magic_item_delete import main as item_delete
from magic_item_post import main as item_post
from magic_item_get import main as item_get
from magic_item_put import main as item_put

# Index JSON
INDEX_JSON_DIR = f"{os.getcwd()}/storage_data/index.json"
with open(INDEX_JSON_DIR, 'r') as f:
    index_json = json.load(f)

# DB_URL
DB_URL = "https://magic-item-generator-default-rtdb.firebaseio.com/magic_items"

# Authentication setup
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/firebase.database"
]
CREDENTIALS = service_account.Credentials.from_service_account_file(
    "credentials.json", scopes=SCOPES)

auth_session = AuthorizedSession(CREDENTIALS)

OPTION_LIST = ["0. Exit", "1. Get", "2. Post", "3. Put", "4. Delete"]

LINE_DIVIDE = "=========================================================\n"

RARITY_LIST = os.listdir(f"{os.getcwd()}/magic_items/")
# ----------------------------------------------------------------------------------


def print_options() -> None:
    """
    Function to print options
    """

    print(LINE_DIVIDE)
    print("Please select from the following options:\n")

    for option in OPTION_LIST:
        print(f"{option}\n")
    print(LINE_DIVIDE)

def get_process() -> None:
    
    # While loop to insure valid rarity input
    while True:
        rarity = input("Rarity level: ")
        rarity.lower()

        if rarity in RARITY_LIST:
            break
        else:
            print("Invalid Input.\n")
            
    # While loop to insure valid item count input
    while True:
        try:
            item_count = int(input("How many magic items do you want? "))
            print()

        except:
            print("Invalid Input.\n")

        else:
            break
        
    full_URL = f"https://magic-item-generator-default-rtdb.firebaseio.com/magic_items/{rarity}.json"
    
    print(LINE_DIVIDE)
        
    item_get(auth_session, full_URL, item_count)
    

def post_process() -> None:
    
    # While loop to insure valid rarity input
    while True:
        rarity = input("Rarity level: ")
        print()
        rarity.lower()

        if rarity in RARITY_LIST:
            break
        else:
            print("Invalid Input.\n")

    # Grabs the file names within the rarity folder
    files_in_rarity = os.listdir(
        f"{os.getcwd()}/magic_items/{rarity}/")
    
    file_directory = f"{os.getcwd()}/magic_items/{rarity}/"
    
    db_folder_url = f"{DB_URL}/{rarity}/.json"
    
    print(LINE_DIVIDE)
    
    item_post(auth_session, file_directory, INDEX_JSON_DIR, db_folder_url, files_in_rarity)

def put_process() -> None:
        
    # While loop to insure valid rarity input
    while True:
        rarity = input("Rarity level: ")
        print()
        rarity.lower()

        if rarity in RARITY_LIST:
            break
        else:
            print("Invalid Input.\n")

    # Grabs the file names within the rarity folder
    files_in_rarity = os.listdir(
        f"{os.getcwd()}/magic_items/{rarity}/")
    
    file_directory = f"{os.getcwd()}/magic_items/{rarity}/"
    
    db_folder_url = f"{DB_URL}/{rarity}/"
    
    print(LINE_DIVIDE)
    
    item_put(auth_session, file_directory, INDEX_JSON_DIR, db_folder_url, files_in_rarity)

def delete_process() -> None:
    """
    Function that handles setting up the delete request.
    """

    # While loop to insure valid rarity input
    while True:
        rarity = input("Rarity level: ")
        print()
        rarity.lower()

        if rarity in RARITY_LIST:
            break
        else:
            print("Invalid Input.\n")

    # Grabs the file names within the rarity folder
    files_in_rarity = os.listdir(
        f"{os.getcwd()}/magic_items/{rarity}/")
    
    # While loop to insure valid file input 
    while True:
        file_name = input("What is the name of the file? ")

        if file_name in files_in_rarity:
            break
        else:
            print(f"{file_name} does not exist in {rarity}.\n")

    # Puts together information for target url
    target_url = f"{DB_URL}/{rarity}/{index_json[file_name]}"

    print("----------------------------------------------------------\n")

    # Runs function to delete file from index.json and database
    item_delete(auth_session, index_json,
                INDEX_JSON_DIR, target_url, file_name)


def main():

    print("Welcome to Seth Hartman's database querier. Version 1.3.0")

    print_options()

    while True:
        user_input = input("")
        print()

        # 0. Exit
        if user_input == "0":
            input("Thank you for using my program, press enter to exit.")
            sys.exit()

        # 1. Get
        elif user_input == "1":
            get_process()
            print_options()

        # 2. Post
        elif user_input == "2":
            post_process()
            print_options()

        # 3. Put
        elif user_input == "3":
            put_process()
            print_options()

        # 4. Delete
        elif user_input == "4":
            delete_process()
            print_options()


if __name__ == "__main__":
    main()

