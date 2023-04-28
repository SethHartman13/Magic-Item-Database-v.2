# Import for datatyping
from google.auth.transport.requests import AuthorizedSession

# Build in libraries
import random

def main(auth_session: AuthorizedSession, full_URL: str, item_count: int) -> None:
    
    response = auth_session.get(full_URL)
    
    # If the database says it was a good request
    if response.status_code == 200:
        
        # Puts data into usable format
        response_json = response.json()
        magic_item_tuples = list(response_json.items())
        
        # Loops through and grabs information from dictionary
        for _ in range(item_count):

            information_list = []
            
            # Pulls information out of a random tuple
            # Tuple format: (unique_DB_ID (str), item_dictionary (dict))
            _, item_dict = magic_item_tuples[random.randint(
                0, len(magic_item_tuples) - 1)]
            
            # Collecting information every JSON has
            name = item_dict['name']
            itype = item_dict['type']
            details = item_dict['details']
            homebrew = item_dict['homebrew']
            
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
                attunement = item_dict['attunement']
                variation_list = item_dict['variations']
                
                # If there are no variations, just collect name
                if variation_list == "":
                    information_list.append(name)
                    
                # If there are variations, select random variation.
                else:
                    variation = variation_list[random.randint(0,len(variation_list) - 1)]
                
                    # Collect name and variation
                    information_list.append(f"{name} ({variation})")
                    
                # If the item requires attunement
                if attunement:
                    
                    attunement_type = item_dict["attunement_type"]
                    
                    # If there are no special requirements
                    if attunement_type == "None":
                        information_list.append("Requires attunement")
                
                    elif attunement_type == "class":
                        c_class = item_dict["class"]
                        information_list.append(f"Requires attunement by a creature who has a least one level in the following class(es): {c_class}")
                        
                    elif attunement_type == "race":
                        race = item_dict["race"]
                        information_list.append(f"Requires attunement by the following race(s): {race}")
                    
                    elif attunement_type == "other":
                        other = item_dict["other"]
                        information_list.append(f"Attunement Requirement: {other}")
                        
                    else:
                        assert False, f"attunement_type was given an unknown attunement of {attunement_type} with item {name}"
                
                else:
                    pass
                
                information_list.append(details)
                
                if homebrew:
                    information_list.append("HOMEBREW ITEM\n")
                else:
                    information_list.append("")
                    
            for line in information_list:
                print(line)
                

if __name__ == "__main__":
    print("This code is not meant to be executed directly, please execute main.py instead.")
                