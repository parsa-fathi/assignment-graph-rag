import os


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
        """
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"The file {self.file_path} does not exist.")

        try:
            with open(self.file_path, "r") as file:
                return file.readline().strip()
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
    """
    api_key_reader = APIKeyReader(env_file_path)
    return api_key_reader.read_api_key()


def start(env_file_path: str) -> None:
    """
    Starts the process of retrieving and printing the API key.

    Args:
        env_file_path (str): The path to the .env file.
    """
    try:
        API = get_api_key(env_file_path)
        print(API)
    except (FileNotFoundError, IOError) as e:
        print(e)


# Example usage
if __name__ == "__main__":
    env_file_path = r"Resources\settings.env"
    start(env_file_path)
