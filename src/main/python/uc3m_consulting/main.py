"""file for getting expected file signature"""

from uc3m_consulting import ProjectDocument


def show_signature():
    """Show expected file signature"""
    document = ProjectDocument("deca2698d32baefe542ef5c3ba8236a2", "File1234.pdf")
    file_signature = document.file_signature
    print(file_signature)

if __name__ == '__main__':
    show_signature()
