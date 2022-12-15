import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from inventory_client import InventoryClient


def GetBooksByISBNList(client, lst):
    """Returns a list of books from a list of ISBNs."""
    books = []
    for isbn in lst:
        books.append(client.get_book(isbn))
    return books


if __name__ == "__main__":
    isbn_list = ["9783161484100", "9783161484101"]
    # establish client instance
    client = InventoryClient(host="127.0.0.1", port=50051)
    print("Client created successfully!")
    print(GetBooksByISBNList(client, isbn_list))
