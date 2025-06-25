class IFileReader:
    def read_file(self, file_path: str) -> str:
        raise NotImplementedError("Subclasses should implement this method.")
    
    def listdir(self, directory_path: str) -> list:
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
        
    def listdir(self, directory_path: str) -> list:
        try:
            import os
            return os.listdir(directory_path)
        except FileNotFoundError:
            return f"Error: The directory {directory_path} does not exist."
        except Exception as e:
            return f"An error occurred: {e}"
        
class MockFileReader(IFileReader):
    def __init__(self):
        self.contents = {}

    def setup_file(self, file_path: str, file_content: str):
        self.contents[file_path] = file_content

    def unset_file(self, file_path: str):
        if file_path in self.contents:
            del self.contents[file_path]

    def unset_files_in_directory(self, directory_path: str):
        files_to_remove = [key for key in self.contents if key.startswith(directory_path)]
        for file_path in files_to_remove:
            self.unset_file(file_path)

    def read_file(self, file_path: str) -> str:
        return self.contents.get(file_path, f"No mock has been set up for file path '{file_path}'")
    
    def listdir(self, directory_path: str) -> list:
        import os
        return [os.path.basename(p) for p in self.contents if p.startswith(directory_path)]