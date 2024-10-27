from mongoengine import connect, disconnect
from contextlib import contextmanager


@contextmanager
def mongo_connection(mongo_uri: str, database: str):
    # Connect to MongoDB using the provided MongoDB URI
    connect(
        host=mongo_uri,
        db=database
    )
    try:
        # Yield control back to the calling context
        yield
    finally:
        # Ensure disconnection after context is exited
        disconnect()