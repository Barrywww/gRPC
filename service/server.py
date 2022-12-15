from concurrent import futures
import logging

import grpc
import inventory_pb2
import service_pb2
import service_pb2_grpc

# book storage
books = [
    {
        "isbn": "9783161484100",
        "title": "Fantasy Book",
        "author": "John Doe",
        "year": 2022,
        "genre": 1
    },
    {
        "isbn": "9783161484101",
        "title": "Adventure Book",
        "author": "John Doe",
        "year": 2020,
        "genre": 2
    },
    {
        "isbn": "9783161484102",
        "title": "Romance Book",
        "author": "John Doe",
        "year": 2019,
        "genre": 3
    },
    {
        "isbn": "9783161484103",
        "title": "Contemporary Book",
        "author": "John Doe",
        "year": 2018,
        "genre": 4
    }
]


class InventoryService(service_pb2_grpc.InventoryServicer):
    # get a book by isbn
    def GetBook(self, request, context):
        filtered_book = list(filter(lambda book: book["isbn"] == request.isbn, books))
        # if there is one book with the given isbn
        if len(filtered_book) > 0:
            # flatten the book object
            grpc_book = inventory_pb2.Book(**filtered_book[0])
            return service_pb2.GetBookResponse(book=grpc_book)

        # otherwise, return empty response
        return service_pb2.GetBookResponse()

    # create a new book in the database by user input
    def CreateBook(self, request, context):
        filtered_books = list(filter(lambda book: book["isbn"] == request.isbn, books))
        # if the book does not exist
        if len(filtered_books) == 0:
            # verify the user input
            if not (request.isbn and request.title and request.author and request.genre):
                return service_pb2.Status(code=3, message="Invalid request.")

            db_book = {
                "isbn": request.isbn,
                "title": request.title,
                "author": request.author,
                "year": request.year,
                "genre": request.genre
            }
            books.append(db_book)
            return service_pb2.Status(code=0, message="Book created successfully.")

        # set the error code and message
        return service_pb2.Status(code=6, message="Book with the same ISBN already exists in the database.")


# Start the server
# Adapted from https://github.com/grpc/grpc/blob/master/examples/python/helloworld/greeter_server.py
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_InventoryServicer_to_server(InventoryService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started successfully!")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
