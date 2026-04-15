"""Module """
import hashlib
import json
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
        with open(input_file, "r", encoding="utf-8") as file:
            input_data = json.load(file)

        project_id = input_data["PROJECT_ID"]
        file_name = input_data["FILENAME"]

        text_to_hash = (
            f"{{alg:SHA-256, typ:DOCUMENT, "
            f"project_id:{project_id}, file_name:{file_name}}}"
        )
        file_signature = hashlib.sha256(
            text_to_hash.encode("utf-8")
        ).hexdigest()

        document = {
            "project_id": project_id,
            "file_name": file_name,
            "file_signature": file_signature
        }

        try:
            with open("all_documents.json", "r", encoding="utf-8") as file:
                all_documents = json.load(file)
        except FileNotFoundError:
            all_documents = []

        all_documents.append(document)

        with open("all_documents.json", "w", encoding="utf-8") as file:
            json.dump(all_documents, file, indent=4)

        return file_signature