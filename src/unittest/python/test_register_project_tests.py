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

    def test_tc20_del_open_quote_filename_label(self):
        """TC20: Invalid JSON format from missing opening quotations for FILENAME label"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc20_del_open_quote_filename_label.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc21_missing_filename_label(self):
        """TC21: Invalid JSON format from missing FILENAME label"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc21_missing_filename_label.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON does not have the expected structure. Invalid FILENAME label",
            str(context.exception)
        )

    def test_tc22_del_close_quote_filename_label(self):
        """TC22: Invalid JSON format from missing ending quotations for FILENAME label"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc22_del_close_quote_filename_label.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc23_missing_colon_filename(self):
        """TC23: Invalid JSON format from missing colon within FILENAME field"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc23_missing_colon_filename.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc24_del_open_quote_filename_value(self):
        """TC24: Invalid JSON format from missing opening quotations for FILENAME value"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc24_del_open_quote_filename_value.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc25_missing_name(self):
        """TC25: Invalid JSON format from missing <NAME> field"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc25_missing_name.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid NAME",
            str(context.exception)
        )

    def test_tc26_missing_extension(self):
        """TC26: Invalid JSON format from missing <EXTENSION> field"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc26_missing_extension.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid EXTENSION",
            str(context.exception)
        )

    def test_tc27_del_close_quote_filename_value(self):
        """TC27: Invalid JSON format from missing ending quotations for FILENAME value"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc27_del_close_quote_filename_value.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc28_dup_json_start(self):
        """TC28: Duplicate JSON start bracket causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc28_dup_json_start.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc29_mod_json_start(self):
        """TC29: Modified JSON start bracket causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc29_mod_json_start.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc30_dup_json_end(self):
        """TC30: Duplicate JSON end bracket causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc30_dup_json_end.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc31_mod_json_end(self):
        """TC31: Modified JSON end bracket causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc31_mod_json_end.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc32_dup_open_quote_proj_id_label(self):
        """TC32: Duplicate opening quotation mark for PROJECT_ID label causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc32_dup_open_quote_proj_id_label.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc33_mod_open_quote_proj_id_label(self):
        """TC33: Modified opening quotation mark for PROJECT_ID label causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc33_mod_open_quote_proj_id_label.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc34_dup_project_id_label(self):
        """TC34: Invalid JSON from duplicating PROJECT_ID field label"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_project_id_label.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON does not have the expected structure. Invalid PROJECT_ID label",
            str(context.exception)
        )
    def test_tc35_mod_project_id_label(self):
        """TC35: Invalid JSON from modified field name for project ID"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_project_id_label.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON does not have the expected structure. Invalid PROJECT_ID label",
            str(context.exception)
        )

    def test_tc36_dup_close_quote_project_id_label(self):
        """TC36: Duplicate closing quotation mark for PROJECT_ID label causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc36_dup_close_quote_project_id_label.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc37_mod_close_quote_project_id_label(self):
        """TC36: Modified closing quotation mark for PROJECT_ID label causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc37_mod_close_quote_project_id_label.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc38_dup_colon_project_id(self):
        """TC38: Duplicate colon for PROJECT_ID field causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc38_dup_colon_project_id.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc39_mod_colon_project_id(self):
        """TC38: Modified colon for PROJECT_ID field causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc39_mod_colon_project_id.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc40_dup_open_quote_project_id_value(self):
        """TC40: Duplicate opening quotation mark for PROJECT_ID value causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc40_dup_open_quote_project_id_value.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc41_mod_open_quote_project_id_value(self):
        """TC41: Modified opening quotation mark for PROJECT_ID value causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc41_mod_open_quote_project_id_value.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc42_dup_project_id_value(self):
        """TC42: Invalid JSON from duplicated project ID value"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_project_id_value.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid PROJECT_ID value",
            str(context.exception)
        )

    def test_tc43_mod_project_id_value(self):
        """TC43: Invalid JSON from modified project ID value"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_project_id_value.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid PROJECT_ID value",
            str(context.exception)
        )

    def test_tc44_dup_close_quote_project_id_value(self):
        """TC44: Duplicate closing quotation mark for PROJECT_ID value causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc44_dup_close_quote_project_id_value.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc45_mod_close_quote_project_id_value(self):
        """TC45: Modified closing quotation mark for PROJECT_ID value causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc45_mod_close_quote_project_id_value.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc46_dup_separator(self):
        """TC46: Duplicate separator causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc46_dup_separator.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc47_mod_separator(self):
        """TC47: Modified separator causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc47_mod_separator.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc48_dup_open_quote_filename_label(self):
        """TC48: Duplicate opening quotation mark for FILENAME label causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc48_dup_open_quote_filename_label.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc49_mod_open_quote_filename_label(self):
        """TC49: Modified opening quotation mark for FILENAME label causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc49_mod_open_quote_filename_label.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    # This will def need to be implemented in method
    def test_tc50_dup_filename_label(self):
        """TC50: Invalid JSON from duplicating FILENAME field label"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_filename_label.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON does not have the expected structure. Invalid FILENAME label",
            str(context.exception)
        )

    def test_tc51_mod_filename_label(self):
        """TC51: Invalid JSON from modified FILENAME field label"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_filename_label.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON does not have the expected structure. Invalid FILENAME label",
            str(context.exception)
        )

    def test_tc52_dup_close_quote_filename_label(self):
        """TC52: Duplicate closing quotation mark for FILENAME label causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc52_dup_close_quote_filename_label.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc53_mod_close_quote_filename_label(self):
        """TC53: Modified closing quotation mark for FILENAME label causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc53_mod_close_quote_filename_label.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc54_dup_colon_filename(self):
        """TC54: Duplicate colon for FILENAME field causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc54_dup_colon_filename.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc55_mod_colon_filename(self):
        """TC55: Modified colon for FILENAME field causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc55_mod_colon_filename.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc56_dup_open_quote_filename_value(self):
        """TC56: Duplicate opening quotation mark for FILENAME value causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc56_dup_open_quote_filename_value.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc57_mod_open_quote_filename_value(self):
        """TC57: Modified opening quotation mark for FILENAME value causes JSON format error"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc57_mod_open_quote_filename_value.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "This file is not JSON formatted.",
            str(context.exception)
        )

    # REFACTOR TO CHECK LENGTH == 8
    def test_tc58_dup_name(self):
        """TC58: Invalid JSON from duplicate file name that is not 8 alphanumeric chars"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_name_value.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid NAME",
            str(context.exception)
        )
    def test_tc59_mod_name(self):
        """TC59: Invalid JSON from duplicate file name that is not 8 alphanumeric chars"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_name_value.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid NAME",
            str(context.exception)
        )

    def test_tc60_dup_pdf_extension(self):
        """TC60: Duplicate .pdf extension violates the accepted extension types"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc60_dup_pdf_extension.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid EXTENSION",
            str(context.exception)
        )

    def test_tc61_dup_docx_extension(self):
        """TC61: Duplicate .docx extension violates the accepted extension types"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc61_dup_docx_extension.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid EXTENSION",
            str(context.exception)
        )

    def test_tc62_dup_xlsx_extension(self):
        """TC62: Duplicate .xlsx extension violates the accepted extension types"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc62_dup_xlsx_extension.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid EXTENSION",
            str(context.exception)
        )

    def test_tc63_mod_pdf_extension(self):
        """TC63: Invalid JSON from modifying .pdf extension to invalid extension"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_extension.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid EXTENSION",
            str(context.exception)
        )

    def test_tc64_mod_docx_extension(self):
        """TC64: Invalid JSON from modifying .docx extension to invalid extension"""
        manager = EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_extension.json")

        with self.assertRaises(EnterpriseManagementException) as context:
            manager.register_document(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid EXTENSION",
            str(context.exception)
        )

    def test_tc65_mod_xlsx_extension(self):
        """TC63: Invalid JSON from modifying .xlsx extension to invalid extension"""
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
