# Import for datatyping
from google.auth.transport.requests import AuthorizedSession

# Built-in libraries
import json
import threading

# Created modules
import connection_error

# Global variables
error_files = []


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

    def run(
        self
    ) -> None:
        global error_files

        # Checks to see if the file in in the index
        with open(self.index_json_dir, "r") as f:
            index_json = json.load(f)

        # If the file is already in the index
        if self.file_name not in index_json.keys():
            # Print lock
            with self.print_lock:
                print(f"{self.file_name} doesn't already exist! ")

        # If the file is not already in the index
        else:
            # Builds file path
            full_file_dir = f"{self.file_dir}/{self.file_name}"

            # Opens JSON file (thread safe because threads are accessing different files)
            with open(full_file_dir, "r") as f:
                json_file = f.read()

            # Creates the final portion of the DB full_URL
            self.full_url = f"{self.full_url}{index_json[self.file_name]}/.json"

            # Sends JSON to database
            response = self.session.put(self.full_url, data=json_file)

            # If the database says it was a good request
            if response.status_code == 200:
                # Print lock
                with self.print_lock:
                    print(f"{self.file_name} successfully updated!\n")

            # If the databases says it was not a good request
            else:
                # Error lock
                with self.error_lock:
                    error_files.append(
                        f"{self.file_name} Error: {response.status_code}"
                    )


def main(
    auth_session: AuthorizedSession,
    file_dir: str,
    index_json_dir: str,
    db_folder_url: str,
    file_list: list[str],
) -> None:
    """
    Main function to add JSONS to the database

    Args:
        auth_session (AuthorizedSession): Authenticated request object
        file_dir (str): Directory of JSONs
        index_json_dir (str): Directory of index.json
        db_folder_url (str): URL of target database folder
        file_list (list[str]): List of file names within target directory
    """

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


if __name__ == "__main__":
    print(
        "This code is not meant to be executed directly, please execute main.py instead."
    )
