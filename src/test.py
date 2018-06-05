import json

a = json.loads("[{\"name\":\"Content-type\", \"value\":\"application/x-www-form-urlencoded\"},{\"name\":\"ts\", \"value\":\"str(int(time.time()))\"},{\"name\":\"App-Language\", \"value\":\"EN\"}]")
print(a)
