# Built in libraries
import json
import os
import sys
from jsonschema import validate
from jsonschema import ValidationError
import threading
import multiprocessing as mp
from pathlib import Path

os.chdir(Path.cwd())

RARITY_LIST = os.listdir(f"{os.getcwd()}/magic_items/")
problem_counter = 0

thread_lock = threading.Lock()
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
                valid = ['None', 'class', 'race', 'other']
                if json_file['attunement'] not in valid:
                    problems.append('attunement')
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


class CheckThread(threading.Thread):
    def __init__(self, 
                json_name: str, 
                rarity: str, 
                # print_lock: threading.Lock,
                # problem_lock: threading.Lock
                ):
        """
        Thread that handles checking each JSON in storage

        Args:
            json_name (str): Name of the JSON
            rarity (str): Rarity of the JSON
            print_lock (threading.Lock): Lock to prevent race conditions while printing
            problem_lock (threading.Lock): Lock to prevent race conditions while adding to the problem counter
        """
        
        threading.Thread.__init__(self)
        self.json_name = json_name
        self.rarity = rarity
        # self.print_lock = print_lock
        # self.problem_lock = problem_lock

    def run(self):
        """
        Overrides default method behavior
        """
        global problem_counter        
        
        # Opens potion
        with open(
            self.json_name, "r"
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
            # with self.print_lock:
            with process_lock:
                print(f"Error with file '{self.json_name}' in rarity '{self.rarity}' with the following problem{end}")
                for problem in problems:
                    print(problem)
                
            print()
            
            # Adds one to the problem counter
            # with self.problem_lock:
            #     problem_counter += 1
        else:
            pass
                

def start_thread(item_list: list) -> None:
    global process_lock
    threads = []

    for temp_list in item_list:
        # print(f"First item in list = {temp_list[0]}")
        # print(f"Second item in list = {temp_list[1]}")

        directory = temp_list[0]
        rarity = temp_list[1]

        threads.append(CheckThread(directory, rarity))

    # Start threads
    for thread in threads:
        thread.start()

    # Join threads
    for thread in threads:
        thread.join()
    

def divide_list(to_split_list: list[list], n: int):

    for i in range(0, len(to_split_list), n):
        yield to_split_list[i:i+n]



def main() -> None:
    """
    Main program function
    """
    global process_lock
    # Create thread list and locks
    dir_list = []
    # print_lock = mp.Lock()
    # problem_lock = mp.Lock()

    # For each rarity we have folders for
    for rarity in RARITY_LIST:
        json_list = os.listdir(f"{os.getcwd()}/magic_items/{rarity}")

        # If the rarity is not empty
        if len(json_list) != 0:
            
            # Create a thread for each JSON
            for json_name in json_list:
                temp_list = []

                temp_list.append(f"{os.getcwd()}\\magic_items\\{rarity}\{json_name}")
                temp_list.append(rarity)
                dir_list.append(temp_list)

        else:
            pass


    n = (len(dir_list) // os.cpu_count()) + 1

    pool_item_list = list(divide_list(dir_list, n))


    pool = mp.Pool(processes=os.cpu_count())

    pool.map(start_thread, pool_item_list)

    mp.Barrier(os.cpu_count())
    
    # # If there were problem JSONs
    # if problem_counter > 0:
        
    #     # Singular or plural
    #     if problem_counter == 1:
    #         end = "."
    #     else:
    #         end = "s."
    #     print(f"\nValidation process complete with {problem_counter} problem{end}")
        
    # # If there were no problem JSONs
    # else:
    #     print(f"Validation process complete with no problems.")

# Makes the program run it it is executed directly
if __name__ == "__main__":
    main()
