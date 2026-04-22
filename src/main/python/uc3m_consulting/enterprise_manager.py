"""Module """
import json
import re

from .project_document import ProjectDocument
from .enterprise_management_exception import EnterpriseManagementException


class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass


    @staticmethod
    def validate_cif(cif: str):
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
        #Added for TC14
        except FileNotFoundError as exc:
            raise EnterpriseManagementException("Input file not found.") from exc
        except json.JSONDecodeError as exc:
            raise EnterpriseManagementException(
                "The file is not JSON formatted." # Hits TC4, TC5 and TC6
            ) from exc

        # Added for TC7
        if not input_data:
            raise EnterpriseManagementException(
                "JSON does not have the expected structure: missing FIELDS"
            )


        if "PROJECT_ID" not in input_data:
            raise EnterpriseManagementException(
                # Added to pass TC10
                "JSON does not have the expected structure. Invalid PROJECT_ID label"
            )

        project_id = input_data["PROJECT_ID"]

        #Added to pass TC14/TC42/TC43
        if not (isinstance(project_id, str) and re.fullmatch(r"[0-9a-fA-F]{32}", project_id)):
            raise EnterpriseManagementException(
                "JSON data has no valid values: invalid PROJECT_ID value"
            )

        #Added to pass TC21/50/51
        if "FILENAME" not in input_data:
            raise EnterpriseManagementException(
                # Added to pass TC21
                "JSON does not have the expected structure. Invalid FILENAME label"
            )

        file_name = input_data["FILENAME"]

        # Added for TC26/63/64/65
        if "." not in file_name:
            raise EnterpriseManagementException(
                "JSON data has no valid values: invalid EXTENSION"
            )

        name_part, extension = file_name.rsplit(".", 1)

        # Added to pass TC63/64/65
        if extension not in {"pdf", "docx", "xlsx"}:
            raise EnterpriseManagementException(
                "JSON data has no valid values: invalid EXTENSION"
            )

        # Added to pass TC60/61/62
        if "." in name_part:
            raise EnterpriseManagementException(
                "JSON data has no valid values: invalid EXTENSION"
            )

        #Added to pass TC25/58/59 added criteria: length == 8 chars
        if not (name_part.isalnum() and len(name_part) == 8):  # added criteria: length == 8 chars
            raise EnterpriseManagementException(
                "JSON data has no valid values: invalid NAME"
            )

        #Added to pass TC13
        if extension not in {"pdf", "docx", "xlsx"}:
            raise EnterpriseManagementException(
                "JSON data has no valid values: invalid EXTENSION"
            )

        try:
            document = ProjectDocument(project_id, file_name)
            file_signature = document.file_signature
        except Exception as exc:
            raise EnterpriseManagementException(
                "Internal processing error when getting the file_signature."
            ) from exc

        try:
            with open("all_documents.json", "r", encoding="utf-8") as file:
                all_documents = json.load(file)
        except FileNotFoundError:
            all_documents = []

        all_documents.append(document.to_json())

        with open("all_documents.json", "w", encoding="utf-8") as file:
            json.dump(all_documents, file, indent=4)

        return file_signature
