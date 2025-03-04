import os
import sys


class APIKeyReader:
    """
    A class to handle reading the API key from a specified .env file.
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = os.path.abspath(file_path)

    def read_api_key(self) -> str:
        """
        Reads the API key from the first line of the specified .env file.

        Returns:
            str: The API key.

        Raises:
            FileNotFoundError: If the .env file does not exist.
            IOError: If there is an error reading the file.
            ValueError: If the file is empty.
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"The file settings.env does not exist.")

        try:
            with open(self.file_path, "r") as file:
                api_key = file.readline().strip()
                if not api_key:
                    raise ValueError("There is no API key in the specified file!")
                return api_key
        except IOError as e:
            raise IOError(f"An error occurred while reading the file: {e}")


def get_api_key(env_file_path: str) -> str:
    """
    Retrieves the API key from the specified .env file.

    Args:
        env_file_path (str): The path to the .env file.

    Returns:
        str: The API key.

    Raises:
        FileNotFoundError: If the .env file does not exist.
        IOError: If there is an error reading the file.
        ValueError: If the file is empty.
    """
    api_key_reader = APIKeyReader(env_file_path)
    return api_key_reader.read_api_key()


def start(env_file_path: str) -> None:
    """
    Starts the process of retrieving the API key.

    Args:
        env_file_path (str): The path to the .env file.
    """
    try:
        API = get_api_key(env_file_path)
        return API
    except (FileNotFoundError, IOError, ValueError) as e:
        print(e)
        sys.exit(1)


def read_env_file(env_file_path):
    with open(env_file_path, "r", encoding="utf-8") as file:
        return file.read().strip()


# Example usage
if __name__ == "__main__":
    env_file_path = r"Resources\settings.env"
    start(env_file_path)
