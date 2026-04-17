"""class for testing the regsiter_order method"""
import unittest
import json
from pathlib import Path
from unittest.mock import PropertyMock, patch

from uc3m_consulting import EnterpriseManager, EnterpriseManagementException


class MyTestCase(unittest.TestCase):
    """class for testing the register_order method"""

    @staticmethod
    def get_json_path(folder_type: str, json_filename: str):
        """Helper function to get JSON file path for each test case"""
        json_path = (
                Path(__file__).parent
                / "resources"
                / "register_document"
                / folder_type
                / json_filename
        )
        return json_path

    def valid_test_case_algorithm(self, folder_type: str, json_filename: str, expected_result: str):
        """Helper function for all valid cases to verify outputs"""
        manager = EnterpriseManager()

        json_path = self.get_json_path(folder_type, json_filename)

        with open(json_path, "r", encoding="utf-8") as file:
            input_data = json.load(file)

        project_id = input_data["PROJECT_ID"]
        file_name = input_data["FILENAME"]

        result = manager.register_document(str(json_path))
        print("expected result: " + expected_result)
        print("actual result: " + result)

        # Assert Output 1: SHA-256 string
        self.assertEqual(expected_result, result)

        # Assert Output 2: reads all_documents.json and verifies it has correct data
        with open("all_documents.json", "r", encoding="utf-8") as file:
            documents = json.load(file)

        last_document = documents[-1]
        self.assertEqual(last_document["project_id"], project_id)
        self.assertEqual(last_document["file_name"], file_name)
        self.assertEqual(last_document["file_signature"], result)

    def test_tc1_valid_pdf(self):
        """TC1: valid PROJECT_ID and valid FILENAME with .pdf extension."""
        self.valid_test_case_algorithm(
            "valid",
            "tc1-valid_pdf.json",
            "5771041b7746580d20c491b004fdc34fac914dddcb75fed9c19165ece809d7c8"
        )

    def test_tc2_valid_docx(self):
        """TC2: valid PROJECT_ID and valid FILENAME with .docx extension."""
        self.valid_test_case_algorithm(
            "valid",
            "tc2-valid_docx.json",
            "77dfa10d2b667b499d2de86f9ffae784f3582ca58228807696a2744f1af03e19"
        )

    def test_tc3_valid_xlsx(self):
        """TC3: valid PROJECT_ID and valid FILENAME with .xlsx extension."""
        self.valid_test_case_algorithm(
            "valid",
            "tc3-valid_xlsx.json",
            "2609fc088a47dff0da1e1004a6cc17dcb614edc2fcc146677831ab7d93d0987a"
        )

    def test_tc4_empty_file(self):
        """TC4: Invalid JSON format from empty file."""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc4-empty_file.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc5_missing_json_start(self):
        """TC5: Invalid JSON format from missing curly bracket at start of file"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc5-missing_json_start.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc6_missing_fields(self):
        """TC6: Invalid JSON from missing FIELDS"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc6-missing_fields.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON does not have the expected structure: missing <FIELDS>",
            str(context.exception)
        )

    def test_tc7_missing_json_end(self):
        """TC7: Invalid JSON format from missing curly bracket at end of file"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc7_missing_json_end.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc8_missing_project_id(self):
        """TC8: Invalid JSON from missing PROJECT_ID"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc8-missing_project_id.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc9_missing_separator(self):
        """TC9: Invalid JSON from missing SEPARATOR"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc9-missing_separator.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc10_missing_filename(self):
        """TC10: Invalid JSON from missing FILENAME"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc10-missing_filename.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )


    def test_tc11_duplicate_project_id(self):
        """TC11: Invalid JSON from duplicate <PROJECT_ID>"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc11-duplicate_project_id.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON does not have the expected structure: duplicate field <PROJECT_ID>",
            str(context.exception)
        )

    def test_tc12_duplicate_filename(self):
        """TC12: Invalid JSON from duplicate <FILENAME>"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc12-duplicate_filename.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON does not have the expected structure: duplicate field <FILENAME>",
            str(context.exception)
        )

    def test_tc13_del_open_quote_proj_id_label(self):
        """TC13: Invalid JSON format from missing opening quotations for PROJECT_ID label"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc13_del_open_quote_proj_id_label.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc14_missing_proj_id_label(self):
        """TC14: Invalid JSON from missing project <id_label>"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc14_missing_proj_id_label.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON does not have the expected structure. Invalid PROJECT_ID label",
            str(context.exception)
        )

    def test_tc15_del_close_quote_proj_id_label(self):
        """TC15: Invalid JSON format from missing ending quotations for PROJECT_ID label"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc15_del_close_quote_proj_id_label.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc16_missing_colon_project_id(self):
        """TC16: Invalid JSON format from missing colon within PROJECT_ID field"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc16_missing_colon_project_id.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc17_del_open_quote_proj_id_value(self):
        """TC17: Invalid JSON format from missing opening quotations for PROJECT_ID value"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc17_del_open_quote_proj_id_value.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc18_missing_proj_id_value(self):
        """TC18: Invalid JSON format from missing opening quotations for PROJECT_ID value"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc18_missing_proj_id_value.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid PROJECT_ID value",
            str(context.exception)
        )

    def test_tc19_del_close_quote_proj_id_value(self):
        """TC19: Invalid JSON format from missing ending quotations for PROJECT_ID value"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc19_del_close_quote_proj_id_value.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc35_invalid_project_id_label(self):
        """TC35: Invalid JSON from modified field name for project ID"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_project_id_label.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON does not have the expected structure. Invalid PROJECT_ID label",
            str(context.exception)
        )

    def test_tc43_mod_project_id_value(self):
        """TC11: Invalid JSON from modified project ID value"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_project_id_value.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid PROJECT_ID value",
            str(context.exception)
        )

    # REFACTOR TO CHECK LENGTH == 8
    def test_tc59_mod_name(self):
        """TC12: Invalid JSON from modified file name with non-alphanumeric character"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_name_value.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid NAME",
            str(context.exception)
        )

    def test_tc63_mod_node39(self):
        """TC63: Invalid JSON from modified .pdf extension with invalid extension"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_extension.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid EXTENSION",
            str(context.exception)
        )


    def test_tc68_file_does_not_exist(self):
        """TC68: Invalid from referencing a JSON path that does not exist"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc68-file_does_not_exist.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "Input file not found.",
            str(context.exception)
        )

    def test_tc69_internal_processing_error(self):
        """TC69: Invalid case by forcing an internal processing error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc69-valid_for_signature_error.json")

        with patch(
                "uc3m_consulting.enterprise_manager.ProjectDocument.file_signature",
                new_callable=PropertyMock,
                side_effect=Exception("Forced signature error")
        ):
            with self.assertRaises(EnterpriseManagementException) as context:
                manager.register_document(str(json_path))

        self.assertEqual(
            "Internal processing error when getting the file_signature.",
            str(context.exception)
        )

if __name__ == '__main__':
    unittest.main()
