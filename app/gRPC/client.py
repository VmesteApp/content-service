import grpc

from app.gRPC.gen import profile_pb2
from app.gRPC.gen import profile_pb2_grpc


def run(userID):
    with grpc.insecure_channel('localhost:44044') as channel:
        stub = profile_pb2_grpc.ProfileServiceStub(channel)

        request = profile_pb2.GetVkIDRequest(userID=userID)

        try:

            response = stub.GetVkID(request)
            print(f"Received VkID: {response.vkID}")
        except grpc.RpcError as e:
            print(f"gRPC error: {e.code()} - {e.details()}")
        return response.vkID
