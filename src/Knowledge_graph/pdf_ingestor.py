from concurrent.futures import ThreadPoolExecutor

from tqdm import tqdm
from unstructured.cleaners.core import (
    clean,
    group_broken_paragraphs,
    remove_punctuation,
    replace_unicode_quotes,
)
from unstructured.partition.pdf import partition_pdf


class FileHandler:
    """
    A class to handle file operations such as reading addresses from a file
    and writing data to a file.
    """

    def __init__(self, path: str) -> None:
        self.path = path

    def retrieve_addresses(self) -> list:
        """
        Reads file addresses from the specified file and returns them as a list.
        """
        relative_addresses = []
        with open(self.path, "r") as file:
            for line in tqdm(file, desc="Reading File Addresses"):
                line = line.strip()
                relative_addresses.append(line)
        return relative_addresses

    def write_data(self, path: str, data: str) -> None:
        """
        Writes the given data to the specified file.
        """
        with open(path, "w") as file:
            file.write(data)


def process_pdf(address: str) -> str:
    """
    Processes a PDF file and returns the cleaned text data.
    """
    text_data = ""
    elements = partition_pdf(address, strategy="auto")
    for element in elements:
        element.apply(replace_unicode_quotes, remove_punctuation)
        text_data += element.text
    return text_data


def main():
    # Retrieving PDFs Addresses
    handler = FileHandler(r"Resources\PDF_addresses.txt")
    relative_addresses = handler.retrieve_addresses()

    # Using ThreadPoolExecutor for parallel processing
    text_data = ""
    with ThreadPoolExecutor() as executor:
        results = list(
            tqdm(
                executor.map(process_pdf, relative_addresses),
                total=len(relative_addresses),
                desc="Processing PDFs",
            )
        )
        text_data = "".join(results)

    # Clean and group the text data
    clean(
        text_data,
        extra_whitespace=True,
        trailing_punctuation=True,
        bullets=True,
        dashes=True,
    )
    text_data = group_broken_paragraphs(text_data)

    # Write the cleaned text data to a file
    handler.write_data(r"src\Knowledge_graph\Data.txt", text_data)


if __name__ == "__main__":
    main()
