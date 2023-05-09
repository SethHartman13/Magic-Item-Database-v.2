import json

base_dictionary = {}
VALID_ITEM_TYPES = ["potion", "armor", "ring", "rod", "staff", "wand", "weapon", "wondrous item"]
VALID_RARITIES = ["common", "uncommon", "rare", "varies", "very rare", "legendary", "artifact"]
YES_RESPONSES = ["yes", "y", "1"]
NO_RESPONSES = ["no", "n", "0"]
VALID_LEVELS = ["0", "cantrip", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
VALID_ATTUNEMENT_TYPES = ["none", "class", "race", "other"]

def name(     
) -> None:
    
    global base_dictionary

    base_dictionary["name"] = input("What is the name of the item? ")
    return


def type(
) -> None:
    
    global base_dictionary

    while True:

        item_type = input("What is the item type? ")
        item_type.lower()

        if item_type in VALID_ITEM_TYPES:
            base_dictionary['type'] = item_type
            break
        else:
            print("Invalid Input")

    return


def rarity(
) -> None:
    
    global base_dictionary
    
    while True:

        item_rarity = input("What is the item rarity? ")
        item_rarity.lower()

        if item_rarity in VALID_RARITIES:
            base_dictionary['rarity'] = item_rarity
            break
        else:
            print("Invalid Input")

    return


def homebrew(
) -> None:
    
    global base_dictionary
    
    while True:

        item_homebrew = input("Is this item homebrew? ")
        item_homebrew.lower()

        if item_homebrew in YES_RESPONSES or item_homebrew in NO_RESPONSES:
            if item_homebrew in NO_RESPONSES:
                base_dictionary["homebrew"] = False
            else:
                base_dictionary["homebrew"] = True

            break
        else:
            print("Invalid Input")

    return


def details(
) -> None:
    
    global base_dictionary

    base_dictionary['details'] = input("Enter in item details: ")
    return

# ----------------------------------------------------------------------------------
# Other items

def attunement(
) -> None:
    
    global base_dictionary
    
    while True:

        item_attunement = input("Is this item require attunement? ")
        item_attunement.lower()

        if item_attunement in YES_RESPONSES or item_attunement in NO_RESPONSES:
            if item_attunement in NO_RESPONSES:
                base_dictionary["attunement"] = False
            else:
                base_dictionary["attunement"] = True
                attunement_type()

            break
        else:
            print("Invalid Input")

    return


def attunement_class(
) -> None:
    
    global base_dictionary

    base_dictionary["class"] = input("What are the class attunement details? ")

    return


def attunement_race(
) -> None:
    
    global base_dictionary

    base_dictionary["race"] = input("What are the race attunement details? ")

    return


def attunement_other(
) -> None:
    
    global base_dictionary

    base_dictionary["other"] = input("What are the attunement details? ")

    return


def attunement_type(
) -> None:
    
    global base_dictionary

    while True:
        user_input = input("What is the attunement type? ")
        user_input.lower()

        if user_input in VALID_ATTUNEMENT_TYPES:
            if user_input == "none":
                base_dictionary["attunement_type"] = "None"

            elif user_input == "class":
                base_dictionary["attunement_type"] = "class"
                attunement_class()

            elif user_input == "race":
                base_dictionary["attunement_type"] = "race"
                attunement_race()

            else:
                base_dictionary["attunement_type"] = "other"
                attunement_other()

            break

        else:
            print("Invalid Input")

    return


def variations(
) -> None:
    global base_dictionary
    variations = []

    while True:

        user_input = input("What variations do you want? (leave empty to finish) ")

        if user_input != "":
            variations.append(user_input)

        else:
            break


def main(
) -> None:

    global base_dictionary

    while True:
        base_dictionary = {}
        name()
        type()
        rarity()
        homebrew()
        details()
        attunement()
        variations()

    









        print(base_dictionary)

        user_input = input("Want to do another one? ")










    
