import grpc
import database_pb2
import database_pb2_grpc
from bson import ObjectId


def create_record(name, age, city, roll):
    # name = input("Enter name: ")
    # age = int(input("Enter age: "))
    # roll = input("Enter Roll No: ")
    # city = input("Enter city: ")

    channel = grpc.insecure_channel("localhost:5000")
    stub = database_pb2_grpc.DatabaseServiceStub(channel)
    print("reached client")
    create_response = stub.CreateRecord(
        database_pb2.CreateRecordRequest(name=name, age=age, city=city, roll=roll)
    )
    print("was record created ?")
    print("Record created with ID:", create_response.id)


def read_record(record_id):
    channel = grpc.insecure_channel("localhost:5000")
    stub = database_pb2_grpc.DatabaseServiceStub(channel)
    # record_id = input("Enter record ID: ")
    read_response = stub.ReadRecord(database_pb2.ReadRecordRequest(id=record_id))
    print("Read record:", read_response.name, read_response.age, read_response.city)
    return read_response


def update_record(record_id, name, age, city):
    channel = grpc.insecure_channel("localhost:5000")
    stub = database_pb2_grpc.DatabaseServiceStub(channel)
    # record_id = input("Enter record ID to update: ")
    # name = input("Enter new name: ")
    # age = int(input("Enter new age: "))
    # city = input("Enter new city: ")

    update_response = stub.UpdateRecord(
        database_pb2.UpdateRecordRequest(id=record_id, name=name, age=age, city=city)
    )
    print(update_response.message)


def delete_record(record_id):
    channel = grpc.insecure_channel("localhost:5000")
    stub = database_pb2_grpc.DatabaseServiceStub(channel)
    # record_id = input("Enter record ID to delete: ")

    delete_response = stub.DeleteRecord(database_pb2.DeleteRecordRequest(id=record_id))
    # print("Deleted ?")
    print(delete_response.message)

    # def main():
    # channel = grpc.insecure_channel("localhost:50051")
    # stub = database_pb2_grpc.DatabaseServiceStub(channel)


#     while True:
#         print("\nOptions:")
#         print("1. Create Record")
#         print("2. Read Record")
#         print("3. Update Record")
#         print("4. Delete Record")
#         print("5. Exit")
#         choice = input("Enter your choice: ")

#         if choice == "1":
#             create_record(stub)
#         elif choice == "2":
#             read_record(stub)
#         elif choice == "3":
#             update_record(stub)
#         elif choice == "4":
#             delete_record(stub)
#         elif choice == "5":
#             break
#         else:
#             print("Invalid choice. Please try again.")


# if __name__ == "__main__":
#     main()
