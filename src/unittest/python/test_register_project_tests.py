"""class for testing the register_order method"""
import unittest
import json
from pathlib import Path
from unittest.mock import PropertyMock, patch

import uc3m_consulting
from uc3m_consulting import ProjectDocument


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

    def valid_test_case_alg(self, folder_type: str, json_filename: str, expected_result: str):
        """Helper function for all valid cases to verify outputs"""
        manager = uc3m_consulting.EnterpriseManager()

        json_path = self.get_json_path(folder_type, json_filename)

        with open(json_path, "r", encoding="utf-8") as file:
            input_data = json.load(file)

        project_id = input_data["PROJECT_ID"]
        file_name = input_data["FILENAME"]

        result = manager.RegisterDocument(str(json_path))
        print("expected result: " + expected_result)
        print("actual result: " + result)

        # Assert Output 1: SHA-256 string
        self.assertEqual(expected_result, result)

        # Assert Output 2: reads all_documents.json and verifies it has correct data
        with open("all_documents.json", "r", encoding="utf-8") as file:
            documents = json.load(file)

        last_document = documents[-1]
        self.assertEqual(last_document["alg"], "SHA-256")
        self.assertEqual(last_document["typ"], "DOCUMENT")
        self.assertEqual(last_document["project_id"], project_id)
        self.assertEqual(last_document["file_name"], file_name)
        self.assertIn("register_date", last_document)
        self.assertEqual(last_document["file_signature"], result)

    def test_tc1(self):
        """TC1: valid PROJECT_ID and valid FILENAME with .pdf extension."""
        self.valid_test_case_alg(
            "valid",
            "tc1-valid_pdf.json",
            "1a11adad20dead4345f337a775f3927f78432c1f6441608bb953a2df5133ec41"
        )

    def test_tc2(self):
        """TC2: valid PROJECT_ID and valid FILENAME with .docx extension."""
        self.valid_test_case_alg(
            "valid",
            "tc2-valid_docx.json",
            "caf9f4c756850f8196a4976179a38d6c8d7ea8db3da0bca74b1d0e1e7d8352f0"
        )

    def test_tc3(self):
        """TC3: valid PROJECT_ID and valid FILENAME with .xlsx extension."""
        self.valid_test_case_alg(
            "valid",
            "tc3-valid_xlsx.json",
            "85392121ec2f93860df8697e9bd6bb7cb9e27cb458b8b3b8964b230139182f66"
        )

    def test_tc4(self):
        """TC4: Invalid JSON format from empty file."""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc4-empty_file.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc5(self):
        """TC5: Invalid JSON format from missing curly bracket at start of file"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc5-missing_json_start.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc6(self):
        """TC6: Invalid JSON from missing FIELDS"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc6-missing_fields.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON does not have the expected structure: missing FIELDS",
            str(context.exception)
        )

    def test_tc7(self):
        """TC7: Invalid JSON format from missing curly bracket at end of file"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc7_missing_json_end.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc8(self):
        """TC8: Invalid JSON from missing PROJECT_ID"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc8-missing_project_id.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc9(self):
        """TC9: Invalid JSON from missing SEPARATOR"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc9-missing_separator.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc10(self):
        """TC10: Invalid JSON from missing FILENAME"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc10-missing_filename.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )


    def test_tc11(self):
        """TC11: Invalid JSON from duplicate <PROJECT_ID>"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc11-duplicate_project_id.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON does not have the expected structure: duplicate field PROJECT_ID",
            str(context.exception)
        )

    def test_tc12(self):
        """TC12: Invalid JSON from duplicate <FILENAME>"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc12-duplicate_filename.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON does not have the expected structure: duplicate field FILENAME",
            str(context.exception)
        )

    def test_tc13(self):
        """TC13: Invalid JSON format from missing opening quotations for PROJECT_ID label"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc13_del_open_quote_proj_id_label.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc14(self):
        """TC14: Invalid JSON from missing project <id_label>"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc14_missing_proj_id_label.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON does not have the expected structure. Invalid PROJECT_ID label",
            str(context.exception)
        )

    def test_tc15(self):
        """TC15: Invalid JSON format from missing ending quotations for PROJECT_ID label"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc15_del_close_quote_proj_id_label.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc16(self):
        """TC16: Invalid JSON format from missing colon within PROJECT_ID field"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc16_missing_colon_project_id.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc17(self):
        """TC17: Invalid JSON format from missing opening quotations for PROJECT_ID value"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc17_del_open_quote_proj_id_value.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc18(self):
        """TC18: Invalid JSON format from missing opening quotations for PROJECT_ID value"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc18_missing_proj_id_value.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid PROJECT_ID value",
            str(context.exception)
        )

    def test_tc19(self):
        """TC19: Invalid JSON format from missing ending quotations for PROJECT_ID value"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc19_del_close_quote_proj_id_value.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc20(self):
        """TC20: Invalid JSON format from missing opening quotations for FILENAME label"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc20_del_open_quote_filename_label.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc21(self):
        """TC21: Invalid JSON format from missing FILENAME label"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc21_missing_filename_label.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON does not have the expected structure. Invalid FILENAME label",
            str(context.exception)
        )

    def test_tc22(self):
        """TC22: Invalid JSON format from missing ending quotations for FILENAME label"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc22_del_close_quote_filename_label.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc23(self):
        """TC23: Invalid JSON format from missing colon within FILENAME field"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc23_missing_colon_filename.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc24(self):
        """TC24: Invalid JSON format from missing opening quotations for FILENAME value"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc24_del_open_quote_filename_value.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc25(self):
        """TC25: Invalid JSON format from missing <NAME> field"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc25_missing_name.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid NAME",
            str(context.exception)
        )

    def test_tc26(self):
        """TC26: Invalid JSON format from missing <EXTENSION> field"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc26_missing_extension.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid EXTENSION",
            str(context.exception)
        )

    def test_tc27(self):
        """TC27: Invalid JSON format from missing ending quotations for FILENAME value"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc27_del_close_quote_filename_value.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc28(self):
        """TC28: Duplicate JSON start bracket causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc28_dup_json_start.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc29(self):
        """TC29: Modified JSON start bracket causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc29_mod_json_start.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc30(self):
        """TC30: Duplicate JSON end bracket causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc30_dup_json_end.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc31(self):
        """TC31: Modified JSON end bracket causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc31_mod_json_end.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc32(self):
        """TC32: Duplicate opening quotation mark for PROJECT_ID label causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc32_dup_open_quote_proj_id_label.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc33(self):
        """TC33: Modified opening quotation mark for PROJECT_ID label causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc33_mod_open_quote_proj_id_label.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc34(self):
        """TC34: Invalid JSON from duplicating PROJECT_ID field label"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_project_id_label.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON does not have the expected structure. Invalid PROJECT_ID label",
            str(context.exception)
        )
    def test_tc35(self):
        """TC35: Invalid JSON from modified field name for project ID"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_project_id_label.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON does not have the expected structure. Invalid PROJECT_ID label",
            str(context.exception)
        )

    def test_tc36(self):
        """TC36: Duplicate closing quotation mark for PROJECT_ID label causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc36_dup_close_quote_project_id_label.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc37(self):
        """TC37: Modified closing quotation mark for PROJECT_ID label causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc37_mod_close_quote_project_id_label.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc38(self):
        """TC38: Duplicate colon for PROJECT_ID field causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc38_dup_colon_project_id.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc39(self):
        """TC39: Modified colon for PROJECT_ID field causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc39_mod_colon_project_id.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc40(self):
        """TC40: Duplicate opening quotation mark for PROJECT_ID value causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc40_dup_open_quote_project_id_value.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc41(self):
        """TC41: Modified opening quotation mark for PROJECT_ID value causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc41_mod_open_quote_project_id_value.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc42(self):
        """TC42: Invalid JSON from duplicated project ID value"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_project_id_value.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid PROJECT_ID value",
            str(context.exception)
        )

    def test_tc43(self):
        """TC43: Invalid JSON from modified project ID value"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_project_id_value.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid PROJECT_ID value",
            str(context.exception)
        )

    def test_tc44(self):
        """TC44: Duplicate closing quotation mark for PROJECT_ID value causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc44_dup_close_quote_project_id_value.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc45(self):
        """TC45: Modified closing quotation mark for PROJECT_ID value causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc45_mod_close_quote_project_id_value.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc46(self):
        """TC46: Duplicate separator causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc46_dup_separator.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc47(self):
        """TC47: Modified separator causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc47_mod_separator.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc48(self):
        """TC48: Duplicate opening quotation mark for FILENAME label causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc48_dup_open_quote_filename_label.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc49(self):
        """TC49: Modified opening quotation mark for FILENAME label causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc49_mod_open_quote_filename_label.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    # This will def need to be implemented in method
    def test_tc50(self):
        """TC50: Invalid JSON from duplicating FILENAME field label"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_filename_label.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON does not have the expected structure. Invalid FILENAME label",
            str(context.exception)
        )

    def test_tc51(self):
        """TC51: Invalid JSON from modified FILENAME field label"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_filename_label.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON does not have the expected structure. Invalid FILENAME label",
            str(context.exception)
        )

    def test_tc52(self):
        """TC52: Duplicate closing quotation mark for FILENAME label causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc52_dup_close_quote_filename_label.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc53(self):
        """TC53: Modified closing quotation mark for FILENAME label causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc53_mod_close_quote_filename_label.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc54(self):
        """TC54: Duplicate colon for FILENAME field causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc54_dup_colon_filename.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc55(self):
        """TC55: Modified colon for FILENAME field causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc55_mod_colon_filename.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc56(self):
        """TC56: Duplicate opening quotation mark for FILENAME value causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc56_dup_open_quote_filename_value.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc57(self):
        """TC57: Modified opening quotation mark for FILENAME value causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc57_mod_open_quote_filename_value.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    # REFACTOR TO CHECK LENGTH == 8
    def test_tc58(self):
        """TC58: Invalid JSON from duplicate file name that is not 8 alphanumeric chars"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_name_value.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid NAME",
            str(context.exception)
        )
    def test_tc59(self):
        """TC59: Invalid JSON from duplicate file name that is not 8 alphanumeric chars"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_name_value.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid NAME",
            str(context.exception)
        )

    def test_tc60(self):
        """TC60: Duplicate .pdf extension violates the accepted extension types"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc60_dup_pdf_extension.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid EXTENSION",
            str(context.exception)
        )

    def test_tc61(self):
        """TC61: Duplicate .docx extension violates the accepted extension types"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc61_dup_docx_extension.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid EXTENSION",
            str(context.exception)
        )

    def test_tc62(self):
        """TC62: Duplicate .xlsx extension violates the accepted extension types"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc62_dup_xlsx_extension.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid EXTENSION",
            str(context.exception)
        )

    def test_tc63(self):
        """TC63: Invalid JSON from modifying .pdf extension to invalid extension"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_extension.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid EXTENSION",
            str(context.exception)
        )

    def test_tc64(self):
        """TC64: Invalid JSON from modifying .docx extension to invalid extension"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_extension.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid EXTENSION",
            str(context.exception)
        )

    def test_tc65(self):
        """TC63: Invalid JSON from modifying .xlsx extension to invalid extension"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "shared-invalid_extension.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "JSON data has no valid values: invalid EXTENSION",
            str(context.exception)
        )

    def test_tc66(self):
        """TC66: Duplicate closing quotation mark for FILENAME value causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc66_dup_close_quote_filename_value.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc67(self):
        """TC67: Modified closing quotation mark for FILENAME value causes JSON format error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc67_mod_close_quote_filename_value.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "The file is not JSON formatted.",
            str(context.exception)
        )

    def test_tc68(self):
        """TC68: Invalid from referencing a JSON path that does not exist"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc68-file_does_not_exist.json")

        with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
            manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "Input file not found.",
            str(context.exception)
        )

    def test_tc69(self):
        """TC69: Invalid case by forcing an internal processing error"""
        manager = uc3m_consulting.EnterpriseManager()
        json_path = self.get_json_path("invalid", "tc69-valid_for_signature_error.json")

        with patch.object(
                ProjectDocument,
                "file_signature",
                new_callable=PropertyMock,
                side_effect=Exception("Forced signature error")
        ):
            with self.assertRaises(uc3m_consulting.EnterpriseManagementException) as context:
                manager.RegisterDocument(str(json_path))

        self.assertEqual(
            "Internal processing error when getting the file_signature.",
            str(context.exception)
        )

if __name__ == "__main__":
    unittest.main()
