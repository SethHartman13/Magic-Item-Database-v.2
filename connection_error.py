# Built-in libraries

import webbrowser
import time


def main(
    error_code: int, 
    file_name: str
) -> None:
    """
    Function to handle connection_errors

    Args:
        error_code (int): Error code received by response
        file_name (str): File name in which the error occurred
    """

    print(f"Response came back with status code {error_code} with {file_name}")

    while True:
        user_input = input(
            f"Would you like to look up status code {error_code}? (Y/N) "
        )
        user_input.lower()

        if user_input == "y" or user_input == "yes" or user_input == "1":
            print("Your browser will pull up a wikipedia article.")
            time.wait(2)
            webbrowser.open("https://en.wikipedia.org/wiki/List_of_HTTP_status_codes")
            break
        elif user_input == "n" or user_input == "no" or user_input == "0":
            break

        else:
            print("Invalid input")


if __name__ == "__main__":
    print("This file is not supposed to be run by itself.")
