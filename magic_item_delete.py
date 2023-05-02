# Import for datatyping
from google.auth.transport.requests import AuthorizedSession

# Built-in libraries
import json

# Created modules
import connection_error


def main(
    auth_session: AuthorizedSession,
    index_json: dict,
    index_json_dir: str,
    full_URL: str,
    file_name: str,
) -> None:
    """
    Main function to delete JSONs from the database

    Args:
        auth_session (AuthorizedSession): Authenticated request object
        index_json (dict): Dictionary of index.json
        index_json_dir (str): Directory of index.json
        full_URL (str): Entire URL of target file
        file_name (str): Name of file to remove from database
    """

    # Sends response to the server to delete the json
    response = auth_session.delete(full_URL)

    # If the database says it was a good request
    if response.status_code == 200:
        # Deletes file from dictionary
        del index_json[file_name]

        # Overwrites file
        with open(index_json_dir, "w") as f:
            json.dump(index_json_dir, f, indent=4, sort_keys=True)

        print(f"{file_name} successfully delete!")

    else:
        # Runs through error code lookup
        connection_error.main(response.status_code, file_name)


if __name__ == "__main__":
    print(
        "This code is not meant to be executed directly, please execute main.py instead."
    )
