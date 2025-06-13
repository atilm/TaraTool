class IFileWriter:
    def write(self, file_path: str, content: str) -> None:
        """Writes content to a file at the specified path."""
        raise NotImplementedError("This method should be overridden by subclasses.")

class FileWriter(IFileWriter):
    def write(self, file_path: str, content: str) -> None:
        """Writes content to a file at the specified path."""
        try:
            with open(file_path, 'w') as file:
                file.write(content)
        except Exception as e:
            raise IOError(f"An error occurred while writing to the file {file_path}: {e}")
        
class MockFileWriter(IFileWriter):
    def __init__(self):
        self.contents = {}

    def write(self, file_path: str, content: str) -> None:
        """Mocks writing content to a file by storing it in a dictionary."""
        self.contents[file_path] = content
