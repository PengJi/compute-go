# steps
1. 编译  
`python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. route_guide.proto`
   
2. run server
`python route_guide_server.py`

3. run client
`python route_guide_client.py`

# references
[grpc/examples/protos/route_guide.proto](https://github.com/grpc/grpc/blob/v1.34.0/examples/protos/route_guide.proto)
[grpc/examples/python/route_guide/](https://github.com/grpc/grpc/tree/v1.34.0/examples/python/route_guide)