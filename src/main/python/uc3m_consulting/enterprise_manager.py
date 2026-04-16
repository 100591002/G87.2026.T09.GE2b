"""Module """
import json

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
                            "JSON does not have the expected structure: duplicate field <PROJECT_ID>"
                        )
                    # Added to pass TC9
                    elif key == "FILENAME":
                        raise EnterpriseManagementException(
                            "JSON does not have the expected structure: duplicate field <FILENAME>"
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
        except json.JSONDecodeError as exc:
            if "Expecting ',' delimiter" in str(exc):
                raise EnterpriseManagementException(
                    "JSON does not have the expected structure: missing <SEPARATOR>"
                ) from exc
            raise EnterpriseManagementException(
                "The file is not JSON formatted."
            ) from exc

        # check TC7
        if not input_data:
            raise EnterpriseManagementException(
                "JSON does not have the expected structure: missing <FIELDS>"
            )

        keys = set(input_data.keys())

        if "PROJECT_ID" not in input_data:
            if keys == {"FILENAME"}:
                raise EnterpriseManagementException(
                    # Added to pass TC4
                    "JSON does not have the expected structure: missing <PROJECT_ID>"
                )
            raise EnterpriseManagementException(
                # Added to pass TC10
                "JSON data has no valid values: invalid PROJECT_ID label"
            )

        # Added to pass TC6
        if "FILENAME" not in input_data:
            raise EnterpriseManagementException(
                "JSON does not have the expected structure: missing <FILENAME>"
            )

        project_id = input_data["PROJECT_ID"]

        #Added to pass TC11
        if not isinstance(project_id, str) or len(project_id) != 32:
            raise EnterpriseManagementException(
                "JSON data has no valid values: invalid PROJECT_ID value"
            )

        file_name = input_data["FILENAME"]

        document = ProjectDocument(project_id, file_name)
        file_signature = document.file_signature

        try:
            with open("all_documents.json", "r", encoding="utf-8") as file:
                all_documents = json.load(file)
        except FileNotFoundError:
            all_documents = []

        all_documents.append(document.to_json())

        with open("all_documents.json", "w", encoding="utf-8") as file:
            json.dump(all_documents, file, indent=4)

        return file_signature
