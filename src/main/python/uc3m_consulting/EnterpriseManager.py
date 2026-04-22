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
    def ValidateCIF():
        """RETURNS TRUE IF THE IBAN RECEIVED IS VALID SPANISH IBAN,
        OR FALSE IN OTHER CASE"""
        return True

    def RegisterDocument(self, inputFile: str) -> str:
        """Registers a document and returns its SHA-256 signature."""

        def json_object_pairs_hook(pairs):
            """Helper method for TC8 to
            parse JSON while detecting duplicate fields."""

            SEEN_KEYS = set()
            DATA = {}

            for KEY, VALUE in pairs:
                if KEY in SEEN_KEYS:
                    # Only trigger for known valid fields
                    if KEY == "PROJECT_ID":
                        raise EnterpriseManagementException(
                            "JSON does not have the expected structure: duplicate field PROJECT_ID"
                        )
                    # Added to pass TC9
                    if KEY == "FILENAME":
                        raise EnterpriseManagementException(
                            "JSON does not have the expected structure: duplicate field FILENAME"
                        )


                SEEN_KEYS.add(KEY)
                DATA[KEY] = VALUE

            return DATA

        # Refactored to pass TC5
        try:
            with open(inputFile, "r", encoding="utf-8") as FILE:
                # refactored load() parameters to pass TC8
                INPUT_DATA = json.load(
                    FILE,
                    object_pairs_hook=json_object_pairs_hook
                )
        #Added for TC14
        except FileNotFoundError as EXC:
            raise EnterpriseManagementException("Input file not found.") from EXC
        except json.JSONDecodeError as EXC:
            raise EnterpriseManagementException(
                "The file is not JSON formatted." # Hits TC4, TC5 and TC6
            ) from EXC

        # Added for TC7
        if not INPUT_DATA:
            raise EnterpriseManagementException(
                "JSON does not have the expected structure: missing FIELDS"
            )


        if "PROJECT_ID" not in INPUT_DATA:
            raise EnterpriseManagementException(
                # Added to pass TC10
                "JSON does not have the expected structure. Invalid PROJECT_ID label"
            )

        PROJECT_ID = INPUT_DATA["PROJECT_ID"]

        #Added to pass TC14/TC42/TC43
        if not (isinstance(PROJECT_ID, str) and re.fullmatch(r"[0-9a-fA-F]{32}", PROJECT_ID)):
            raise EnterpriseManagementException(
                "JSON data has no valid values: invalid PROJECT_ID value"
            )

        #Added to pass TC21/50/51
        if "FILENAME" not in INPUT_DATA:
            raise EnterpriseManagementException(
                # Added to pass TC21
                "JSON does not have the expected structure. Invalid FILENAME label"
            )

        FILE_NAME = INPUT_DATA["FILENAME"]

        # Added for TC26/63/64/65
        if "." not in FILE_NAME:
            raise EnterpriseManagementException(
                "JSON data has no valid values: invalid EXTENSION"
            )

        NAME_PART, EXTENSION = FILE_NAME.rsplit(".", 1)

        # Added to pass TC63/64/65
        if EXTENSION not in {"pdf", "docx", "xlsx"}:
            raise EnterpriseManagementException(
                "JSON data has no valid values: invalid EXTENSION"
            )

        # Added to pass TC60/61/62
        if "." in NAME_PART:
            raise EnterpriseManagementException(
                "JSON data has no valid values: invalid EXTENSION"
            )

        #Added to pass TC25/58/59 added criteria: length == 8 chars
        if not (NAME_PART.isalnum() and len(NAME_PART) == 8):  # added criteria: length == 8 chars
            raise EnterpriseManagementException(
                "JSON data has no valid values: invalid NAME"
            )

        #Added to pass TC13
        if EXTENSION not in {"pdf", "docx", "xlsx"}:
            raise EnterpriseManagementException(
                "JSON data has no valid values: invalid EXTENSION"
            )

        try:
            DOCUMENT = ProjectDocument(PROJECT_ID, FILE_NAME)
            FILE_SIGNATURE = DOCUMENT.file_signature
        except Exception as EXC:
            raise EnterpriseManagementException(
                "Internal processing error when getting the file_signature."
            ) from EXC

        try:
            with open("all_documents.json", "r", encoding="utf-8") as FILE:
                ALL_DOCUMENTS = json.load(FILE)
        except FileNotFoundError:
            ALL_DOCUMENTS = []

        ALL_DOCUMENTS.append(DOCUMENT.to_json())

        with open("all_documents.json", "w", encoding="utf-8") as FILE:
            json.dump(ALL_DOCUMENTS, FILE, indent=4)

        return FILE_SIGNATURE
