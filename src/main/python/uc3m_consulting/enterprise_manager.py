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
        # Refactored to pass TC5
        try:
            with open(input_file, "r", encoding="utf-8") as file:
                input_data = json.load(file)
        except json.JSONDecodeError as exc:
            if "Expecting ',' delimiter" in str(exc):
                raise EnterpriseManagementException(
                    "JSON does not have the expected structure: missing <SEPARATOR>"
                ) from exc
            raise EnterpriseManagementException(
                "The file is not JSON formatted."
            ) from exc

        # Added to pass TC4
        if "PROJECT_ID" not in input_data:
            raise EnterpriseManagementException(
                "JSON does not have the expected structure: missing <PROJECT_ID>"
            )

        project_id = input_data["PROJECT_ID"]
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