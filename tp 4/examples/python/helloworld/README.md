# gRPC Python quickstart

Depuis `tp 4/examples/python/helloworld`, lance :

```powershell
py greeter_server.py
```

Dans un autre terminal :

```powershell
py greeter_client.py
```

Pour regénérer les fichiers gRPC après une modification du `.proto` :

```powershell
py -m grpc_tools.protoc -I../../protos --python_out=. --pyi_out=. --grpc_python_out=. ../../protos/helloworld.proto
```
