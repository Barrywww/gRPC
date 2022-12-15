import grpc
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from service import service_pb2
from service import service_pb2_grpc


class InventoryClient:
    def __init__(self, host="127.0.0.1", port=50051):
        self.host = host
        self.port = port
        self.channel = grpc.insecure_channel(self.host + ":" + str(self.port))
        self.stub = service_pb2_grpc.InventoryStub(self.channel)

    def get_book(self, isbn):
        return self.stub.GetBook(service_pb2.GetBookRequest(isbn=isbn))

    def create_book(self, isbn, title, author, year, genre):
        return self.stub.CreateBook(
            service_pb2.CreateBookRequest(
                isbn=isbn, title=title, author=author, year=year, genre=genre))
