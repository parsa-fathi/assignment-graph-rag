import os
import sys
import unittest

# Add the src directory to the system path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
)

from Knowledge_graph.API_handeling import read_env_file


class TestAPIHandling(unittest.TestCase):
    def setUp(self):
        self.env_file_path = os.path.abspath(
            os.path.join("Tests", "Resources", "test.env")
        )

    def test_read_env_file(self):
        expected_value = "Just for Test"
        actual_value = read_env_file(self.env_file_path)
        self.assertEqual(actual_value, expected_value)


if __name__ == "__main__":
    unittest.main()
