# Request libraries
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

# Built in libraries
import json
import os
import sys
from pathlib import Path

# Created modules
from magic_item_delete import main as item_delete
from magic_item_post import main as item_post
from magic_item_get import main as item_get
from magic_item_put import main as item_put

# Sets current working directory to the directory of the file
os.chdir(Path.cwd())

# Index JSON
INDEX_JSON_DIR = f"{os.getcwd()}/storage_data/index.json"
with open(INDEX_JSON_DIR, "r") as f:
    index_json = json.load(f)

# DB_URL
DB_URL = "https://magic-item-generator-default-rtdb.firebaseio.com/magic_items"

# Authentication setup
SCOPES = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/firebase.database",
]
CREDENTIALS = service_account.Credentials.from_service_account_file(
    "credentials.json", scopes=SCOPES
)

auth_session = AuthorizedSession(CREDENTIALS)

# Global Constants
OPTION_LIST = ["0. Exit", "1. Get", "2. Post", "3. Put", "4. Delete"]

LINE_DIVIDE = "=========================================================\n"
MINI_DIVIDE = "---------------------------------------------------------\n"

RARITY_LIST = os.listdir(f"{os.getcwd()}/magic_items/")
# ----------------------------------------------------------------------------------


def print_options(
) -> None:
    """
    Function to print options
    """

    print(LINE_DIVIDE)
    print("Please select from the following options:\n")

    for option in OPTION_LIST:
        print(f"{option}\n")
    print(LINE_DIVIDE)


def get_process(
) -> None:
    """
    Function that handles setting up the get request.
    """

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
    """
    Function that handles setting up the post request.
    """

    # While loop to insure valid rarity input
    while True:
        rarity = input("Rarity level: ")
        print()
        rarity.lower()

        if rarity in RARITY_LIST or rarity =="all":
            break
        else:
            print("Invalid Input.\n")

    if rarity != "all":

        # Grabs the file names within the rarity folder
        files_in_rarity = os.listdir(f"{os.getcwd()}/magic_items/{rarity}/")

        file_directory = f"{os.getcwd()}/magic_items/{rarity}/"

        db_folder_url = f"{DB_URL}/{rarity}/.json"

        print(LINE_DIVIDE)

        item_post(
            auth_session, file_directory, INDEX_JSON_DIR, db_folder_url, files_in_rarity
        )

    else:
        # For each rarity list
        for rarity_item in RARITY_LIST:

            # Grabs the file names within the rarity folder
            files_in_rarity = os.listdir(f"{os.getcwd()}/magic_items/{rarity_item}/")
            file_directory = f"{os.getcwd()}/magic_items/{rarity_item}/"
            db_folder_url = f"{DB_URL}/{rarity_item}/.json"

            print(LINE_DIVIDE)

            item_post(
                auth_session, file_directory, INDEX_JSON_DIR, db_folder_url, files_in_rarity
            ) 


def put_process() -> None:
    """
    Function that handles setting up the put request.
    """
    
    # While loop to insure valid rarity input
    while True:
        rarity = input("Rarity level: ")
        print()
        rarity.lower()

        if rarity in RARITY_LIST or rarity == "all":
            break
        else:
            print("Invalid Input.\n")

    if rarity != "all":

        # Grabs the file names within the rarity folder
        files_in_rarity = os.listdir(f"{os.getcwd()}/magic_items/{rarity}/")
        file_directory = f"{os.getcwd()}/magic_items/{rarity}/"
        db_folder_url = f"{DB_URL}/{rarity}/"

        print(LINE_DIVIDE)

        item_put(
            auth_session, file_directory, INDEX_JSON_DIR, db_folder_url, files_in_rarity
        )

    else:
        
        # For each rarity list
        for rarity_item in RARITY_LIST:

            # Grabs the file names within the rarity folder
            files_in_rarity = os.listdir(f"{os.getcwd()}/magic_items/{rarity_item}/")
            file_directory = f"{os.getcwd()}/magic_items/{rarity_item}/"
            db_folder_url = f"{DB_URL}/{rarity_item}/"

            print(LINE_DIVIDE)

            item_put(
                auth_session, file_directory, INDEX_JSON_DIR, db_folder_url, files_in_rarity
            )    


def delete_process(
) -> None:
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
    files_in_rarity = os.listdir(f"{os.getcwd()}/magic_items/{rarity}/")

    # While loop to insure valid file input
    while True:
        file_name = input("What is the name of the file? ")

        if file_name in files_in_rarity:
            break
        else:
            print(f"{file_name} does not exist in {rarity}.\n")

    # Puts together information for target url
    target_url = f"{DB_URL}/{rarity}/{index_json[file_name]}"

    print(MINI_DIVIDE)

    # Runs function to delete file from index.json and database
    item_delete(auth_session, index_json, INDEX_JSON_DIR, target_url, file_name)


def main(
) -> None:
    print("Welcome to Seth Hartman's magic item querier. Version 1.4.0")

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

        else:
            print("Invalid input, please try again.")


if __name__ == "__main__":
    main()
