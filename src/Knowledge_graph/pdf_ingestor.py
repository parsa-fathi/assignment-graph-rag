import json
import multiprocessing
import os
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


def get_cleaned_data(handler: FileHandler, pdf_results: list) -> str:
    """
    Combines the processed PDFs and performs cleaning.
    """
    text_data = "".join(pdf_results)
    clean(
        text_data,
        extra_whitespace=True,
        trailing_punctuation=True,
        bullets=True,
        dashes=True,
    )
    return group_broken_paragraphs(text_data)


def process_all_pdfs(resource_folder: str, output_file: str) -> None:
    """
    Processes all PDFs in the specified resource folder in parallel,
    cleans the text and writes the output to the given file.
    """
    handler = FileHandler(resource_folder)
    pdf_paths = handler.retrieve_pdf_paths()
    max_workers = os.cpu_count() or 1

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        pdf_results = list(
            tqdm(
                executor.map(process_pdf, pdf_paths),
                total=len(pdf_paths),
                desc="Processing PDFs",
            )
        )
    cleaned_text = get_cleaned_data(handler, pdf_results)
    handler.write_data(output_file, cleaned_text)


if __name__ == "__main__":
    multiprocessing.freeze_support()  # Add this line for Windows support
    process_all_pdfs(r"Resources", r"src/Knowledge_graph/Data.txt")
