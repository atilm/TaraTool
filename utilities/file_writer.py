import os

class IFileWriter:
    def write(self, file_path: str, content: str) -> None:
        """Writes content to a file at the specified path."""
        raise NotImplementedError("This method should be overridden by subclasses.")

    def _exists(self, file_path: str) -> bool:
        """Checks if a file exists at the specified path."""
        raise NotImplementedError("This method should be overridden by subclasses.")

class FileWriter(IFileWriter):
    def write(self, file_path: str, content: str) -> None:
        """Writes content to a file at the specified path.
        If the directory does not exist, it will be created."""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, 'w') as file:
                file.write(content)
        except Exception as e:
            raise IOError(f"An error occurred while writing to the file {file_path}: {e}")

    def _exists(self, file_path: str) -> bool:
        """Checks if a file exists at the specified path."""
        return os.path.exists(file_path)

class MockFileWriter(IFileWriter):
    def __init__(self):
        self.written_files = {}
        self.existing_files = set()

    def write(self, file_path: str, content: str) -> None:
        """Mocks writing content to a file by storing it in a dictionary."""
        self.written_files[file_path] = content
        self.existing_files.add(file_path)

    def setup_exisiting_files(self, file_paths: list[str]) -> None:
        """Sets up a list of existing files for the mock writer."""
        self.existing_files.update(file_paths)

    def _exists(self, file_path: str) -> bool:
        """Checks if a file exists at the specified path."""
        return file_path in self.existing_files
