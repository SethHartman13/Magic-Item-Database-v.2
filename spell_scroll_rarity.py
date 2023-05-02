from google.auth.transport.requests import AuthorizedSession
import random
import threading

RARITY_FILE_NAMES = {"common":["spell_scroll_cantrip.json","spell_scroll_first.json"], "uncommon": ["spell_scroll_second.json","spell_scroll_third.json"], "rare": ["spell_scroll_fourth.json","spell_scroll_fifth.json"], "very rare": ["spell_scroll_sixth.json","spell_scroll_seventh.json"], "legendary": ["spell_scroll_ninth.json"]}

MINI_DIVIDE = "---------------------------------------------------------\n"

class RequestThread(threading.Thread):

    def __init__(self, auth_session: AuthorizedSession, full_URL: str, file_name: str):
        threading.Thread.__init__(self)
        self.session = auth_session
        self.url = full_URL
        self.file_name = file_name
        self.thread_response = []

    def run(self):
        response = self.session.get(self.url)

        if response.status_code == 200:

            # Puts data into usable format
            response_json = response.json()

            self.thread_response.append(response_json["name"])

            spells = response_json["spells"]
            self.thread_response.append(f"Spell: {spells[random.randint(0, len(spells) - 1)]}\n")

        else:
            print(f"Program had a problem accessing {self.file_name}! with error code {response.status_code}")


def main(index_json: dict[str,str], grab_rarity_dict: dict[str, int], db_URL: str, auth_session: AuthorizedSession):
    threads = []



    for rarity in grab_rarity_dict:
        if grab_rarity_dict[rarity] > 0:
            number_count = grab_rarity_dict[rarity]
            file_names = RARITY_FILE_NAMES[rarity]

            for i in range(number_count):

                file_name = file_names[random.randint(0, len(file_names) - 1)]

                full_URL = f"{db_URL}/{rarity}/{index_json[file_name]}.json"

                threads.append(RequestThread(auth_session, full_URL, file_name))


    for thread in threads:
        thread.start()

    counter = 0
    
    for thread in threads:
        thread.join()
        counter += 1

        for line in thread.thread_response:
            print(line)

        if counter != len(threads):
            print(MINI_DIVIDE)

        else:
            pass
    




