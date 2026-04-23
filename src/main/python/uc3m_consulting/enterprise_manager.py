"""Module """
import json
import re

from uc3m_consulting.project_document import ProjectDocument
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass


    @staticmethod
    def validate_cif():
        """RETURNS TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
        return True

    def register_document(self, input_file: str) -> str:
        """Registers a document and returns its SHA-256 signature."""

        def json_object_pairs_hook(pairs):
            """Helper method for TC8 to
            parse JSON while detecting duplicate fields."""

            seen_keys = set()
            data = {}

            for key, value in pairs:
                if key in seen_keys:
                    # Only trigger for known valid fields
                    if key == "PROJECT_ID":
                        raise EnterpriseManagementException(
                            "JSON does not have the expected structure: duplicate field PROJECT_ID"
                        )
                    # Added to pass TC9
                    if key == "FILENAME":
                        raise EnterpriseManagementException(
                            "JSON does not have the expected structure: duplicate field FILENAME"
                        )


                seen_keys.add(key)
                data[key] = value

            return data

        # Refactored to pass TC5
        try:
            with open(input_file, "r", encoding="utf-8") as file:
                # refactored load() parameters to pass TC8
                input_data = json.load(
                    file,
                    object_pairs_hook=json_object_pairs_hook
                )
        # Added for TC68
        except FileNotFoundError as exc:
            raise EnterpriseManagementException("Input file not found.") from exc
        except json.JSONDecodeError as exc:
            # Hits TC4-TC5, TC7-TC10, TC13, TC15-TC17, TC19-TC20, TC22-TC24
            # TC27-TC33, TC36-TC41, TC44-TC49, TC52-TC57, TC66-TC67
            raise EnterpriseManagementException(
                "The file is not JSON formatted."
            ) from exc

        # Added for TC6
        if not input_data:
            raise EnterpriseManagementException(
                "JSON does not have the expected structure: missing FIELDS"
            )

        # Added to pass TC14/TC34/TC35
        if "PROJECT_ID" not in input_data:
            raise EnterpriseManagementException(
                "JSON does not have the expected structure. Invalid PROJECT_ID label"
            )

        project_id = input_data["PROJECT_ID"]

        #Added to pass TC18/TC42/TC43
        if not (isinstance(project_id, str) and re.fullmatch(r"[0-9a-fA-F]{32}", project_id)):
            raise EnterpriseManagementException(
                "JSON data has no valid values: invalid PROJECT_ID value"
            )

        #Added to pass TC21/TC50/TC51
        if "FILENAME" not in input_data:
            raise EnterpriseManagementException(
                "JSON does not have the expected structure. Invalid FILENAME label"
            )

        file_name = input_data["FILENAME"]

        # Added for TC26/TC63/TC64/TC65
        if "." not in file_name:
            raise EnterpriseManagementException(
                "JSON data has no valid values: invalid EXTENSION"
            )

        name_part, extension = file_name.rsplit(".", 1)

        # Added to pass TC63/TC64/TC65
        if extension not in {"pdf", "docx", "xlsx"}:
            raise EnterpriseManagementException(
                "JSON data has no valid values: invalid EXTENSION"
            )

        # Added to pass TC60/TC61/TC62
        if "." in name_part:
            raise EnterpriseManagementException(
                "JSON data has no valid values: invalid EXTENSION"
            )

        # Added to pass TC25/TC58/TC59 added criteria: length == 8 chars
        if not (name_part.isalnum() and len(name_part) == 8):
            raise EnterpriseManagementException(
                "JSON data has no valid values: invalid NAME"
            )

        try:
            document = ProjectDocument(project_id, file_name)
            file_signature = document.file_signature
        except Exception as exc:
            # Added to pass TC69
            raise EnterpriseManagementException(
                "Internal processing error when getting the file_signature."
            ) from exc

        try:
            with open("all_documents.json", "r", encoding="utf-8") as file:
                all_documents = json.load(file)
        # create output file if it doesn't already exist
        except FileNotFoundError:
            all_documents = []

        all_documents.append(document.to_json())

        with open("all_documents.json", "w", encoding="utf-8") as file:
            json.dump(all_documents, file, indent=4)

        return file_signature
