# Import for data-typing
from google.auth.transport.requests import AuthorizedSession
import google.auth.transport.requests as requests
from http import client

# Built-in libraries
import json
import threading
import time

# Global variables
error_files = []
# ----------------------------------------------------------------------------------


class RequestThread(
    threading.Thread
):
    def __init__(
        self,
        auth_session: AuthorizedSession,
        file_dir: str,
        index_json_dir: str,
        full_url: str,
        file_name: str,
        index_lock: threading.Lock,
        print_lock: threading.Lock,
        error_lock: threading.Lock,
    ) -> None:
        """
        Thread to handle POST requests

        Args:
            auth_session (AuthorizedSession): Authenticated request object
            file_dir (str): Directory of JSONs
            index_json_dir (str): Directory of index.json
            full_db_url (str): URL of database
            file_name (str): Name of file to add to database
            index_lock (threading.Lock): Lock to prevent race conditions while accessing/editing index.json
            print_lock (threading.Lock): Lock to prevent race conditions while printing
            error_lock (threading.Lock): Lock to prevent race conditions while adding to error list
        """
        threading.Thread.__init__(self)
        self.session = auth_session
        self.file_dir = file_dir
        self.index_json_dir = index_json_dir
        self.full_url = full_url
        self.file_name = file_name
        self.index_lock = index_lock
        self.print_lock = print_lock
        self.error_lock = error_lock
        self.connection_attempts = 0

    def run(
        self
    ) -> None:
        """
        Function that overrides threading.Thread's default behavior.
        """
        global error_files

        # Ensures that the program will attempt a few times to connect to the database
        while self.connection_attempts < 3:
            try:
                # Checks to see if the file has already been added to the index
                with self.index_lock:
                    with open(self.index_json_dir, "r", encoding="utf-8") as f:
                        index_json = json.load(f)

                # If the file is already in the index
                if self.file_name in index_json.keys():
                    # Print lock
                    with self.print_lock:
                        print(f"{self.file_name} already exists! ")

                # If the file is not already in the index
                else:
                    # Builds file path
                    full_file_dir = f"{self.file_dir}/{self.file_name}"

                    # Opens JSON file (thread safe because threads are accessing different files)
                    with open(full_file_dir, "r", encoding="utf-8") as f:
                        edit_json_file = json.load(f)

                    # Renames keys since Firebase does not like $'s in keys
                    schema = edit_json_file['$schema']
                    json_id = edit_json_file['$id']

                    del edit_json_file['$schema']
                    del edit_json_file['$id']

                    edit_json_file['schema'] = schema
                    edit_json_file['id'] = json_id

                    json_file = json.dumps(edit_json_file, indent=4, sort_keys=True)

                    # Sends JSON to database
                    response = self.session.post(self.full_url, data=json_file)

                    # If the database says it was a good request
                    if response.status_code == 200:

                        # Puts response into a JSON
                        response_detail = response.json()

                        # Index lock
                        with self.index_lock:
                            # Pulls up latest version of index
                            with open(self.index_json_dir, "r", encoding="utf-8") as f:
                                index_json = json.load(f)

                            # We add the added json name to the index file with the unique ID assigned by the db
                            index_json[str(self.file_name)] = response_detail["name"]

                            # Overwrites index JSON (with formatting)
                            with open(self.index_json_dir, "w") as f:
                                json.dump(index_json, f, indent=4, sort_keys=True)

                        # Print lock
                        with self.print_lock:
                            print(f"{self.file_name} successfully added!")

                    # If the databases says it was not a good request
                    else:
                        # Error lock
                        with self.error_lock:
                            error_files.append(
                                f"{self.file_name} Error: {response.status_code}"
                            )

            # If there is a connection error
            except client.RemoteDisconnected:
                print(f"Connection failed with {self.file_name}")
                self.connection_attempts += 1

                if self.connection_attempts >= 3:
                    error_files.append(f"{self.file_name} Error: ConnectionError")
                    break

                else:
                    time.sleep(3)
                    pass

            else:
                break


def main(
    auth_session: AuthorizedSession,
    file_dir: str,
    index_json_dir: str,
    db_folder_url: str,
    file_list: list[str],
) -> None:
    """
    Main function to add JSONs to the database

    Args:
        auth_session (AuthorizedSession): Authenticated request object
        file_dir (str): Directory of JSONs
        index_json_dir (str): Directory of index.json
        db_folder_url (str): URL of target database folder
        file_list (list[str]): List of file names within target directory
    """
    global error_files

    # Creates locks
    index_lock = threading.Lock()
    print_lock = threading.Lock()
    error_lock = threading.Lock()

    # Creates threads
    threads = []
    for file in file_list:
        threads.append(
            RequestThread(
                auth_session,
                file_dir,
                index_json_dir,
                db_folder_url,
                file,
                index_lock,
                print_lock,
                error_lock,
            )
        )

    # Starts threads
    for thread in threads:
        thread.start()

    # Joins threads
    for thread in threads:
        thread.join()

    # Error notifications
    if len(error_files) > 0:
        print("The following files had errors:\n")

        for file in error_files:
            print(file)

        error_files = []

    print()


# If the program is run directly when it is not supposed to
if __name__ == "__main__":
    print(
        "This code is not meant to be executed directly, please execute main.py instead."
    )
