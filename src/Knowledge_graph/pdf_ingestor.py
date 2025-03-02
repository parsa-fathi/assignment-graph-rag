import os
import json
from concurrent.futures import ProcessPoolExecutor
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
    A class to handle file operations such as scanning for PDF files in a folder
    and writing data to a file.
    """

    def __init__(self, folder_path: str) -> None:
        self.folder_path = folder_path

    def retrieve_pdf_paths(self) -> list:
        """
        Scans the specified folder for PDF files and returns their paths as a list.

        Returns:
            list: A list of PDF file paths.
        """
        pdf_files = []
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_files.append(os.path.join(root, file))
        return pdf_files

    def write_data(self, path: str, data: str) -> None:
        """
        Writes the given data to the specified file.

        Args:
            path (str): The file path where data will be written.
            data (str): The data to write.
        """
        with open(path, "w", encoding="utf-8") as file:
            file.write(data)


def process_pdf(file_path: str) -> str:
    """
    Processes a PDF file and returns the cleaned text data.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The cleaned text data extracted from the PDF.
    """
    text_data = ""
    elements = partition_pdf(file_path, strategy="auto")
    for element in elements:
        element.apply(replace_unicode_quotes, remove_punctuation)
        text_data += element.text
    return text_data


def main():
    # Scanning for PDF file paths in the given folder.
    handler = FileHandler(r"Resources")  # Set this folder to where your PDFs are located.
    pdf_paths = handler.retrieve_pdf_paths()

    # Process PDFs in parallel using ProcessPoolExecutor for CPU-bound tasks.
    max_workers = os.cpu_count() or 1
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(
            tqdm(
                executor.map(process_pdf, pdf_paths),
                total=len(pdf_paths),
                desc="Processing PDFs",
            )
        )
    text_data = "".join(results)

    # Clean and group the text data.
    clean(
        text_data,
        extra_whitespace=True,
        trailing_punctuation=True,
        bullets=True,
        dashes=True,
    )
    cleaned_text = group_broken_paragraphs(text_data)

    # Write the cleaned text data to a file.
    handler.write_data(r"src/Knowledge_graph/Data.txt", cleaned_text)


if __name__ == "__main__":
    main()
