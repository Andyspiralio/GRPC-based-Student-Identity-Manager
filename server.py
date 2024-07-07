import grpc
from concurrent import futures
import database_pb2
import database_pb2_grpc
from pymongo import MongoClient
from bson import ObjectId


class DatabaseService(database_pb2_grpc.DatabaseServiceServicer):
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["mydatabase"]
        self.collection = self.db["mycollection"]

    def CreateRecord(self, request, context):

        data = {
            "_id": request.roll,  # Using roll as the custom ID
            "name": request.name,
            "age": request.age,
            "city": request.city,
            # "roll": request.roll,
        }
        print("reached server")
        # Check if a record with the given roll number already exists
        existing_record = self.collection.find_one({"_id": request.roll})
        if existing_record:
            # If a record with the same roll number exists, return an error
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("Record with the same roll number already exists")
            return database_pb2.CreateRecordResponse(id="")

        # Insert the record with the roll number as primary key (_id)
        result = self.collection.insert_one(data)
        return database_pb2.CreateRecordResponse(id=str(result.inserted_id))

    # def ReadRecord(self, request, context):
    #     result = self.collection.find_one({"_id": ObjectId(request.id)})
    #     return database_pb2.ReadRecordResponse(
    #         name=result["name"], age=result["age"], city=result["city"]
    #     )

    # def UpdateRecord(self, request, context):
    #     update_query = {"_id": ObjectId(request.id)}
    #     new_values = {
    #         "$set": {"name": request.name, "age": request.age, "city": request.city}
    #     }
    #     self.collection.update_one(update_query, new_values)
    #     return database_pb2.UpdateRecordResponse(message="Document updated")
    def ReadRecord(self, request, context):
        result = self.collection.find_one({"_id": request.id})
        if result:
            return database_pb2.ReadRecordResponse(
                name=result["name"], age=result["age"], city=result["city"]
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Record not found")
            return database_pb2.ReadRecordResponse()

    def UpdateRecord(self, request, context):
        update_query = {"_id": request.id}
        new_values = {
            "$set": {"name": request.name, "age": request.age, "city": request.city}
        }
        result = self.collection.update_one(update_query, new_values)
        if result.modified_count > 0:
            return database_pb2.UpdateRecordResponse(message="Document updated")
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Record not found")
            return database_pb2.UpdateRecordResponse()

    def DeleteRecord(self, request, context):
        delete_query = {"_id": request.id}
        # self.collection.delete_one(delete_query)
        result = self.collection.find_one({"_id": request.id})
        if result:
            # delete_query = {"_id": request.id}
            self.collection.delete_one(delete_query)
            return database_pb2.DeleteRecordResponse(message="Document deleted")
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Record not found")
            return database_pb2.DeleteRecordResponse(message="Not Found")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    database_pb2_grpc.add_DatabaseServiceServicer_to_server(DatabaseService(), server)
    server.add_insecure_port("[::]:5000")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
