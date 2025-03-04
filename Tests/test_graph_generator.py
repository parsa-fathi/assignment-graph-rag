import os
import sys
import unittest
from unittest.mock import patch

# Add the src directory to the system path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from Knowledge_graph.graph_generator import main

# Adjust the import statement to use an absolute import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from Tests import config


class TestGraphGenerator(unittest.TestCase):
    def setUp(self):
        self.ontology_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "Resources", "ontology.json")
        )
        self.data_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "Resources", "Data.txt")
        )

    @patch("builtins.input", return_value=config.api_key)
    def test_train_functionality(self, mock_input):
        # Run the main function with the test API key and mode
        main(
            API_key=config.api_key,
            mode="Train",
            input_path=self.data_file_path,
            output_path=self.ontology_file_path,
        )

        # Check if the ontology file is created and non-empty
        self.assertTrue(os.path.exists(self.ontology_file_path))
        self.assertTrue(os.path.getsize(self.ontology_file_path) > 0)

    def tearDown(self):
        # Clean up the generated ontology file after the test
        if os.path.exists(self.ontology_file_path):
            os.remove(self.ontology_file_path)


if __name__ == "__main__":
    unittest.main()
