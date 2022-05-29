import os
from Position import*
from MatrixSparseDOK import*
import ujson
os.system("cls")

print("------------------Start------------------------")
MQTT_CLIENT_ID = 5
string = "{\"cmd\": \"GET-NODE-LOG-FULL\", \"node_from\": 0}"
teste = ujson.dumps({
    "ola":"adeus",
    "sol":"noite"
})

m = MatrixSparseDOK()
print(m[(1,1)])

# m[(1,1)] = m.__getitem__()
# 'msg_id': 'nao interessa' }