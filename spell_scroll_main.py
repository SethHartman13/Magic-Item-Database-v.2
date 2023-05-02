# Request libraries
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from urllib.request import urlopen

# Built in libraries
import json
import os
import sys

# Created modules
from spell_scroll_rarity import main as scroll_rarity

# Grabs index JSON
JSON_URL = "https://raw.githubusercontent.com/SethHartman13/Magic-Item-Database-v.2/16ea9e18c2d1781a084f3b50976c85c1275f6488/storage_data/index.json"
response = urlopen(JSON_URL)
index_json = json.loads(response.read())
INDEX_KEYS = list(index_json.keys())

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

OPTION_LIST = ["0. Exit", "1. Query by Rarity", "2. Query by Level"]
RARITY_LIST = ["common", "uncommon", "rare", "very rare", "legendary"]
LINE_DIVIDE = "=========================================================\n"
MINI_DIVIDE = "---------------------------------------------------------\n"


grab_level_dict = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
grab_rarity_dict = {
    "common": 0,
    "uncommon": 0,
    "rare": 0,
    "very rare": 0,
    "legendary": 0,
}
# ----------------------------------------------------------------------------------


def initial_check() -> None:
    """
    Runs initial checks to verify files are in database
    """

    errors = []

    # Initial checks to see if the spell scrolls are in the database
    if "spell_scroll_cantrip.json" not in INDEX_KEYS:
        errors.append("Missing Cantrip File!\n")

    if "spell_scroll_first.json" not in INDEX_KEYS:
        errors.append("Missing 1st Level File!\n")

    if "spell_scroll_second.json" not in INDEX_KEYS:
        errors.append("Missing 2nd Level File!\n")

    if "spell_scroll_third.json" not in INDEX_KEYS:
        errors.append("Missing 3rd Level File!\n")

    if "spell_scroll_fourth.json" not in INDEX_KEYS:
        errors.append("Missing 4th Level File!\n")

    if "spell_scroll_fifth.json" not in INDEX_KEYS:
        errors.append("Missing 5th Level File!\n")

    if "spell_scroll_sixth.json" not in INDEX_KEYS:
        errors.append("Missing 6th Level File!\n")

    if "spell_scroll_seventh.json" not in INDEX_KEYS:
        errors.append("Missing 7th Level File!\n")

    if "spell_scroll_eighth.json" not in INDEX_KEYS:
        errors.append("Missing 8th Level File!\n")

    if "spell_scroll_ninth.json" not in INDEX_KEYS:
        errors.append("Missing 9th Level File!\n")

    if len(errors) > 0:
        for error in errors:
            print(error)
    else:
        pass

    return


def print_options() -> None:
    """
    Function to print options
    """

    print(LINE_DIVIDE)
    print("Please select from the following options:\n")

    for option in OPTION_LIST:
        print(f"{option}\n")
    print(LINE_DIVIDE)

def rarity_process() -> None:
    global grab_rarity_dict
    yes_responses = ["yes", 'y', "1"]
    no_responses = ["no", "n", "0"]

    while True:
        while True:
            rarity = input("Rarity level: ")
            rarity.lower()

            if rarity in RARITY_LIST:
                break
            else:
                print("Invalid Input.\n")

        while True:
            try:
                item_count = int(input("How many scrolls of that rarity do you want? "))

            except:
                print("Invalid Input.\n")

            else:
                break

        grab_rarity_dict[rarity] += item_count

        while True:


            response = input("Do you want to roll for other scrolls by rarity? ")
            response.lower()
            print()

            if response in yes_responses or response in no_responses:
                if response in yes_responses:
                    start_search = False
                    print()
                    print(MINI_DIVIDE)

                else:
                    start_search = True
                
                break
            else:
                print("Invalid Input.\n")

        if start_search:
            break
        else:
            pass


    

    scroll_rarity(index_json, grab_rarity_dict, DB_URL, auth_session)



    pass




def main():
    initial_check()

    print("Welcome to Seth Hartman's magic scroll querier. Version 1.0.0")

    print_options()

    while True:
        user_input = input("")
        print()

        # 0. Exit
        if user_input == "0":
            input("Thank you for using my program, press enter to exit.")
            sys.exit()

        # 1. Rarity
        elif user_input == "1":
            rarity_process()
            print_options()

        # 2. Level
        elif user_input == "2":
            #level_process()
            print_options()

        else:
            print("Invalid input, please try again.")

if __name__ == "__main__":
    main()