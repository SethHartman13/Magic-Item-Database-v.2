# Import for data-typing
from google.auth.transport.requests import AuthorizedSession

# Build-in libraries
import random

# Global Constants
MINI_DIVIDE = "---------------------------------------------------------\n"
# ----------------------------------------------------------------------------------


def main(
    auth_session: AuthorizedSession, 
    full_URL: str, 
    item_count: int
) -> None:
    """
    Main request function

    Args:
        auth_session (AuthorizedSession): Authenticated request object
        full_URL (str): URL of database
        item_count (int): number of items desired
    """

    # Sends response to the server to delete the json
    response = auth_session.get(full_URL)

    # If the database says it was a good request
    if response.status_code == 200:
        # Puts data into usable format
        response_json = response.json()
        magic_item_tuples = list(response_json.items())

        counter = 0
        # Loops through and grabs information from dictionary
        for _ in range(item_count):
            information_list = []

            # Pulls information out of a random magic item tuple
            # Tuple format: (unique_DB_ID (str), item_dictionary (dict))
            _, item_dict = magic_item_tuples[
                random.randint(0, len(magic_item_tuples) - 1)
            ]

            # Collecting information every JSON has
            name = item_dict["name"]
            itype = item_dict["item_type"]
            details = item_dict["details"]
            homebrew = item_dict["homebrew"]
            legacy = item_dict["legacy"]

            schema = item_dict["schema"]
            json_id = item_dict["id"]

            # Potions
            if itype == "potion":
                information_list.append(name)
                information_list.append(details)

            # Scrolls
            elif itype == "scroll":
                # Gets spell list
                spell_list = item_dict["spells"]

                # Grabs random spell
                spell = spell_list[random.randint(0, len(spell_list) - 1)]

                # Adds information to list
                information_list.append(f"{name} ({spell})")
                information_list.append(details)

            else:
                # Collects information every other item has
                attunement = item_dict["attunement"]
                variation_list = item_dict["variations"]

                # If there are no variations, just collect name
                if variation_list[0] == "":
                    information_list.append(name)

                # If there are variations, select random variation.
                else:
                    variation = variation_list[
                        random.randint(0, len(variation_list) - 1)
                    ]

                    # Collect name and variation
                    information_list.append(f"{name} ({variation})")

                # If the item requires attunement
                if attunement:
                    attunement_type = item_dict["attunement_type"]

                    # If there are no special requirements
                    if attunement_type == "None":
                        information_list.append("Requires attunement\n")

                    # If the special requirement is a class
                    elif attunement_type == "class":
                        c_class = item_dict["class"]
                        information_list.append(
                            f"Requires attunement by a creature who has a least one level in the following class(es): {c_class}\n"
                        )

                    # If the special requirement is a race
                    elif attunement_type == "race":
                        race = item_dict["race"]
                        information_list.append(
                            f"Requires attunement by the following race(s): {race}\n"
                        )

                    # If the special requirement is something special
                    elif attunement_type == "other":
                        other = item_dict["other"]
                        information_list.append(f"Attunement Requirement: {other}\n")

                    # This is to ensure that a JSON error can be corrected
                    else:
                        assert (
                            False
                        ), f"attunement_type was given an unknown attunement of {attunement_type} with item {name}"

                # If the item does not require attunement
                else:
                    information_list.append("")

                # Appends details to the list
                information_list.append(details)

                if legacy:
                    information_list.append("LEGACY ITEM\n")

                # If the item is not homebrew
                if not homebrew:
                    information_list.append("")
                
                # If the item is homebrew
                else:
                    information_list.append("HOMEBREW ITEM\n")

            # Prints all the information for an item
            for line in information_list:
                print(line)

            # Makes it so that there is a break between items, but not at the end
            counter += 1
            if counter <= item_count - 1:
                print(MINI_DIVIDE)


# If the program is run directly when it is not supposed to 
if __name__ == "__main__":
    print(
        "This code is not meant to be executed directly, please execute main.py instead."
    )
