"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
import logging
import sys

import grpc

import subprocess
from grpc_tools.protoc import main as pbmain
import importlib

SERVICE = """
from codegen.server_pb2_grpc import GreeterServicer, add_GreeterServicer_to_server
from codegen.server_pb2 import HelloReply
    
class Greeter(GreeterServicer):

    def __init__(self):
        globals().update(importlib.import_module('codegen.server_pb2').__dict__)

    def SayHello(self, request, context):
        print(request)
        return HelloReply(message='Hello, %s!' % request.name)

"""


def serve():

    pbmain(['-I.', '--python_out=./codegen', '--grpc_python_out=./codegen', 'server.proto'])
    loc = {}
    exec(SERVICE, globals(), loc)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    loc['add_GreeterServicer_to_server'](loc['Greeter'](), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()