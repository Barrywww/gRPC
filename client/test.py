from unittest.mock import MagicMock
from unittest import TestCase
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from client.get_book_titles import GetBooksByISBNList
from service.inventory_pb2 import Book
from service.service_pb2 import GetBookResponse
from inventory_client import InventoryClient

# create the mock return of book
book_as_dict = {
    "isbn": "9783161484100",
    "title": "Fantasy Book",
    "author": "John Doe",
    "year": 2022,
    "genre": 1
}
sample_book = Book(**book_as_dict)


class InventoryTest(TestCase):
    # test the get book by isbn with mock client
    def test_get_book_mock(self):
        mock_client = InventoryClient()
        mock_client.get_book = MagicMock(return_value=GetBookResponse(book=sample_book))
        book = GetBooksByISBNList(mock_client, ["9783161484100"])
        self.assertEqual(book, [GetBookResponse(book=sample_book)])

    # test the get book by isbn with real client
    def test_get_book(self):
        client = InventoryClient()
        book = GetBooksByISBNList(client, ["9783161484100"])
        self.assertEqual(book, [GetBookResponse(book=sample_book)])

