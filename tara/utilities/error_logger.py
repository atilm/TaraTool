class IErrorLogger:
    def log_error(self, error: Exception) -> None:
        """Logs an error message."""
        raise NotImplementedError("This method should be overridden by subclasses.")

    def log_warning(self, warning: str) -> None:
        """Logs a warning message."""
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def has_errors(self) -> bool:
        """Returns True if there are any logged errors."""
        raise NotImplementedError("This method should be overridden by subclasses.")


class ErrorLogger(IErrorLogger):
    def __init__(self):
        self.has_errors = False

    def log_error(self, error: Exception) -> None:
        """Logs an error message to the console."""
        print(f"Error: {error}")

    def log_warning(self, warning: str) -> None:
        """Logs a warning message to the console."""
        print(f"Warning: {warning}")

    def has_errors(self) -> bool:
        """Returns True if there are any logged errors."""
        return self.has_errors


class MemoryErrorLogger(IErrorLogger):
    def __init__(self):
        self.errors = []
        self.warnings = []

    def log_error(self, error: Exception) -> None:
        """Logs an error message to memory."""
        self.errors.append(str(error))

    def log_warning(self, warning: str) -> None:
        """Logs a warning message to memory."""
        self.warnings.append(warning)

    def has_errors(self) -> bool:
        """Returns True if there are any logged errors."""
        return len(self.errors) > 0

    def get_errors(self) -> list[str]:
        """Returns the list of logged errors."""
        return self.errors

    def get_warnings(self) -> list[str]:
        """Returns the list of logged warnings."""
        return self.warnings
    