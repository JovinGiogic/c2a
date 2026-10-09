"""Small implemented service used for source-grounding checks; no web framework implied."""


class MemoryStore:
    def __init__(self, entries):
        self.entries = entries

    def get(self, key):
        return self.entries.get(key)


class LookupService:
    def __init__(self, store):
        self.store = store

    def lookup(self, key):
        normalized = key.strip().lower()
        value = self.store.get(normalized)
        return {"key": normalized, "value": value}


def handle_request(payload, service):
    return service.lookup(payload["key"])


def build_service():
    return LookupService(MemoryStore({"example": 42}))
