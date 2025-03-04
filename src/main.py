import os
from concurrent.futures import ProcessPoolExecutor
from sys import exit

from tqdm import tqdm

from Knowledge_graph import API_handeling as AP

env_file_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "Resources", "settings.env")
)
try:
    user_API = AP.start(env_file_path)
except (FileNotFoundError, IOError, ValueError) as e:
    print("Error during API key retrieval:", e)
    exit(1)

from Knowledge_graph import pdf_ingestor as PI


def main():
    while True:
        try:
            user_input = int(
                input(
                    """
Enter your mode for using this app:

0: Generating a new knowledge graph
1: Updating an existing knowledge graph
                           
Your choice: """
                )
            )
        except ValueError:
            print("\nPlease enter a valid integer!!!")
            continue

        if user_input not in [0, 1]:
            print("\nInvalid option. Please enter 0 or 1!!!")
            continue
        break

    PI.process_all_pdfs(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Resources")),
        os.path.abspath(
            os.path.join(os.path.dirname(__file__), "Knowledge_graph", "Data.txt")
        ),
    )

    from Knowledge_graph import graph_generator as GG

    output_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "Resources", "ontology.json")
    )
    input_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "Knowledge_graph", "Data.txt")
    )

    if user_input == 0:
        GG.main(user_API, "Train", input_path, output_path)
    else:
        GG.main(user_API, "Update", input_path, output_path)


if __name__ == "__main__":
    main()
