import uuid


def generate_public_id() -> str:
    return str(uuid.uuid4())
