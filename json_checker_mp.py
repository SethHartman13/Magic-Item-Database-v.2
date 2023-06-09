# Built in libraries
import json
import os
import sys
from jsonschema import validate
import multiprocessing as mp
from pathlib import Path

# Sets file directory as working directory
os.chdir(Path.cwd())

# Gets rarity list
RARITY_LIST = os.listdir(f"{os.getcwd()}/magic_items/")
problem_counter = []

# Creates global process lock for printing
process_lock = mp.Lock()
# ----------------------------------------------------------------------------------

def check_entries(
    json_file: dict[str, any]
) -> list:
    """
    Goes through and lists all the problems within a json

    Args:
        json_file (dict[str, any]): JSON that has at least one problem

    Returns:
        list: list of problems with the JSON file
    """
    
    problems = []
    try:
        # Schema version
        try:
            if json_file["$schema"] != "https://json-schema.org/draft-07/schema":
                problems.append("$schema")
        except:
            problems.append("$schema")

        # Item name
        try:
            if json_file['name'] == 'name':
                problems.append("name")
        except:
            problems.append('name')
            
        # Item rarity
        try:
            if json_file['rarity'] == 'rarity':
                problems.append('name')
        except:
            problems.append('rarity')
            
        # Item homebrew status
        try:
            if json_file['homebrew'] != False and json_file['homebrew'] != True:
                problems.append('homebrew')
        except:
            problems.append('homebrew')
            
        # Item details
        try:
            if json_file['details'] == 'details':
                problems.append('details')
        except:
            problems.append('details')


        # If the item is not a potion or a scroll
        if json_file['item_type'] != 'potion' and json_file['item_type'] != 'scroll':
            
            # Item attunement
            try:
                valid = [True,False]
                if json_file['attunement'] not in valid:
                    problems.append('attunement')

                if json_file['attunement']:
                    valid = ['None', "class", "race", "other"]

                    if json_file['attunement_type'] not in valid:
                        problems.append('attunement_type')

            except:
                problems.append("attunement")

            # Item variations
            try:
                json_file['variations']
            except:
                problems.append('variations')


        # If the item is a potion
        elif json_file['item_type'] != 'potion':
            pass
        

        # If the item is a scroll
        else:
            
            # Scroll level
            try: 
                json_file['level']
            except:
                problems.append('level')
            
            # Scroll spells
            try:
                json_file['spells']
            except:
                problems.append('spells')

    except:
        problems.append('item_type (will need to re-verify after this correction)')
        
    return problems

def start_cb(something: None|list[str]) -> None:
    """
    Callback function for start()

    Args:
        something (None | list[str]): If there are no problems, start_cb recieves a None object. If there are problems, it receives a list of strings
    """
    global problem_counter

    if type(something) != list:
        pass
    else:
        problem_counter.append(1)
              

def start(item_list: list[str]) -> None|list[str]:
    """
    Main function that starts when the pool of processes starts

    Args:
        item_list (list[str]): List containing directory location and rarity

    Returns:
        (None|list[str]): If there are no problems, it returns None to the callback. If there are problems, it returns a list of strings to the callback
    """
    global process_lock

    directory = item_list[0]
    rarity = item_list[1]
     
    
    # Opens potion
    with open(
        directory, "r"
    ) as f:
        json_file = json.load(f)

    # Sets schema reference based upon item type
    if json_file["item_type"] == "potion":
        schema_directory = f"{os.getcwd()}/storage_data/potion_schema.json"

    elif json_file["item_type"] == "scroll":
        schema_directory = f"{os.getcwd()}/storage_data/scroll_schema.json"

    else:
        schema_directory = f"{os.getcwd()}/storage_data/general_schema.json"

    # Opens schema
    with open(schema_directory, "r") as f:
        schema = json.load(f)

    # Checks to see if it is valid
    try:
        validate(json_file, schema)

    # If it is not a valid JSON
    except:
        
        # Calls function to check what the problem is
        problems = check_entries(json_file)
                
        # Singular or plural
        if len(problems) == 1:
            end = ":"
        else:
            end = "s:"
        
        # Prints what the problems are with what file and what rarity
        with process_lock:
            print(f"Error with file '{json_file['name']}' in rarity '{rarity}' with the following problem{end}")
            for problem in problems:
                print(problem)
            
        print()

        return problems
        
    else:
        return None

def main() -> None:
    """
    Main program function
    """

    # Create thread list and locks
    dir_list = []

    # For each rarity we have folders for
    for rarity in RARITY_LIST:
        json_list = os.listdir(f"{os.getcwd()}/magic_items/{rarity}")

        # If the rarity is not empty
        if len(json_list) != 0:
            
            # Create a list for each JSON/rarity and add it to the dir_list
            for json_name in json_list:
                temp_list = []

                temp_list.append(f"{os.getcwd()}\\magic_items\\{rarity}\{json_name}")
                temp_list.append(rarity)
                dir_list.append(temp_list)

        else:
            pass

    # Assigns the number of processors to the pool
    pool = mp.Pool(processes=os.cpu_count())

    # Does an apply (async) to each file
    for list in dir_list:
        pool.apply_async(start,args=(list, ), callback=start_cb)

    # Closes the pool
    pool.close()

    # Joins the pool
    pool.join()
    
    # If there were problem JSONs
    if len(problem_counter) > 0:
        
        # Singular or plural
        if len(problem_counter) == 1:
            end = "."
        else:
            end = "s."
        print(f"Validation process complete with {len(problem_counter)} problem file{end}")
        
    # If there were no problem JSONs
    else:
        print(f"Validation process complete with no problem files.")

# Makes the program run it it is executed directly
if __name__ == "__main__":
    main()
    input("Press enter to exit")
