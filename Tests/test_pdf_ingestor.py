import os
import sys
import unittest

# Add the src directory to the system path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from Knowledge_graph.pdf_ingestor import process_all_pdfs


class TestPDFIngestor(unittest.TestCase):
    def setUp(self):
        self.resource_folder = os.path.abspath(os.path.join("Tests", "Resources"))
        self.output_file = os.path.abspath(
            os.path.join("Tests", "Resources", "Output.txt")
        )
        self.expected_output_file = os.path.abspath(
            os.path.join("Tests", "Resources", "Data.txt")
        )

    def test_pdf_ingestor_output(self):
        # Process the PDFs and generate the output file
        process_all_pdfs(self.resource_folder, self.output_file)

        # Read the generated output file
        with open(self.output_file, "r", encoding="utf-8") as file:
            generated_output = file.read()

        # Read the expected output file
        with open(self.expected_output_file, "r", encoding="utf-8") as file:
            expected_output = file.read()

        # Compare the generated output with the expected output
        self.assertEqual(generated_output, expected_output)

    def tearDown(self):
        # Clean up the generated output file after the test
        if os.path.exists(self.output_file):
            os.remove(self.output_file)


if __name__ == "__main__":
    unittest.main()
