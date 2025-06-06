class IFileReader:
    def read_file(self, file_path: str) -> str:
        raise NotImplementedError("Subclasses should implement this method.")

class FileReader(IFileReader):
    def read_file(self, file_path: str) -> str:
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return f"Error: The file {file_path} does not exist."
        except Exception as e:
            return f"An error occurred: {e}"
        