import json
import os
from os import environ

from graphrag_sdk import KnowledgeGraph, Ontology
from graphrag_sdk.model_config import KnowledgeGraphModelConfig
from graphrag_sdk.models.litellm import LiteModel
from graphrag_sdk.source import Source_FromRawText


class OntologyHandler:
    """
    Handles ontology operations such as training and updating.

    Responsibilities:
      - Train a new ontology from provided sources.
      - Update an existing ontology by merging with new data.
    """

    def __init__(
        self, mode: str, sources, model=LiteModel, ontology_file: str = None
    ) -> None:
        """
        Initializes the handler with a mode, sources, a model, and optionally an existing ontology file.

        Args:
            mode (str): Operation mode ("Train" for new ontology, "Update" for merging with an existing one)
            sources: List of source objects for ontology creation.
            model: The language model to use (defaults to LiteModel).
            ontology_file (str, optional): Path to an existing ontology JSON file (required for "Update" mode)
        """
        self.mode = mode
        self.sources = sources
        self.model = model
        self.ontology_file = ontology_file

    def initiation(self) -> Ontology:
        """
        Initiates the ontology creation or update process based on the mode.

        Returns:
            Ontology: The resulting ontology after training or update.
        """
        if self.mode == "Train":
            return self.train_ontology()
        elif self.mode == "Update":
            if not self.ontology_file:
                raise ValueError(
                    "The ontology_file path is mandatory when the mode is 'Update'."
                )
            return self.update_ontology()

    def train_ontology(self) -> Ontology:
        """
        Trains a new ontology using the provided sources.

        Returns:
            Ontology: The trained ontology.
        """
        ontology = Ontology.from_sources(sources=self.sources, model=self.model)
        return ontology

    def update_ontology(self) -> Ontology:
        """
        Updates an existing ontology by merging it with new data.

        Returns:
            Ontology: The updated ontology.
        """
        with open(self.ontology_file, "r", encoding="utf-8") as file:
            old_ontology = Ontology.from_json(json.loads(file.read()))
        new_ontology = self.train_ontology()
        updated_ontology = old_ontology.merge_with(new_ontology)
        return updated_ontology


class SourceHandler:
    """
    Handles retrieval of source data from file system.

    Responsibilities:
      - Read text content from a file.
      - Wrap text in a Source object for ontology generation.
    """

    def __init__(self, mode="Text", path: str = None) -> None:
        """
        Initializes the SourceHandler.

        Args:
            mode (str, optional): The mode for reading (defaults to "Text").
            path (str, optional): The file path to retrieve data from.
        """
        self.mode = mode
        self.path = path

    def get_source(self):
        """
        Retrieves the source data as a Source object.

        Returns:
            Source: The source object created from the file's text.
        """
        if self.mode == "Text":
            return Source_FromRawText(self.text_retrieve())

    def text_retrieve(self) -> str:
        """
        Reads and returns the file content as text.

        Returns:
            str: Text content read from the file.
        """
        with open(self.path, "r", encoding="utf-8") as file:
            return file.read()


def main(API_key: str, mode: str, input_path: str, output_path: str) -> None:
    """
    Main function for executing the ontology handling process.

    Steps:
      1. Configure the API key as an environment variable.
      2. Retrieve source data from a text file.
      3. Train or update the ontology based on the specified mode.
      4. Save the resulting ontology to a JSON file for review.
      5. Load the approved ontology and instantiate the KnowledgeGraph.

    Args:
        API_key (str): The API key to authorize model operations.
        mode (str): Operation mode ("Train" or "Update").
        input_path (str): Path to the input data file.
        output_path (str): Path to the output ontology file.
    """
    # Set the API key environment variable.
    environ["GEMINI_API_KEY"] = API_key

    source_handler = SourceHandler(mode="Text", path=input_path)
    sources = [source_handler.get_source()]

    # Configure the model.
    model = LiteModel(model_name="gemini/gemini-2.0-flash")

    # Create and run the ontology handler.
    handler = OntologyHandler(
        mode=mode, sources=sources, model=model, ontology_file=output_path
    )
    ontology = handler.initiation()

    # Save the generated ontology for review in the Resources folder (always write in Train mode).
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(json.dumps(ontology.to_json(), indent=2))

    # Load approved ontology and instantiate the KnowledgeGraph.
    with open(output_path, "r", encoding="utf-8") as file:
        ontology = Ontology.from_json(json.loads(file.read()))

    kg = KnowledgeGraph(
        name="KnowledgeGraph",
        model_config=KnowledgeGraphModelConfig.with_model(model),
        ontology=ontology,
        host="127.0.0.1",
        port=6379,
        # username=falkor_username,  # optional
        # password=falkor_password   # optional
    )

    kg.process_sources(sources)


if __name__ == "__main__":
    # Example usage for Train mode (ontology file will be written to Resources\ontology.json):
    output_path = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "..", "..", "Resources", "ontology.json"
        )
    )
    input_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Data.txt"))
    main("AIzaSyCzxsT5s5exd6QA1xzlnLrDzC4IjpyCbww", "Train", input_path, output_path)
