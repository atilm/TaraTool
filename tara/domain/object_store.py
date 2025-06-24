from utilities.error_logger import IErrorLogger

class ObjectStore:
    def __init__(self, logger: IErrorLogger):
        self._store: dict[str, object] = {}
        self.logger = logger

    def add(self, obj):
        if hasattr(obj, 'id') and obj.id:
            if obj.id in self._store:
                self.logger.log_error(f"Duplicate ID found: {obj.id}")
                return
            self._store[obj.id] = obj
        else:
            raise ValueError("Object does not have a valid ID.")

    def get(self, obj_id):
        return self._store.get(obj_id)

    def has(self, obj_id):
        return obj_id in self._store

    def items(self):
        return self._store.items()
