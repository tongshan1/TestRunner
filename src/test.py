import json

a = json.loads(
    "[{\"name\":\"Content-type\", \"value\":\"application/x-www-form-urlencoded\"},{\"name\":\"ts\", \"value\":\"str(int(time.time()))\"},{\"name\":\"App-Language\", \"value\":\"EN\"}]")
print(a)

"{\"mobile\":\"18912940592\"," \
"\"mobile_country_code\":\"CN\",\"device_hash\":\"\",\"language\":\"\",\"version\":\"\",\"app_version\":\"\"}"

"[{\"name\":\"mobile\", \"value\":\"18912940592\"},{\"name\":\"mobile_country_code\", \"value\":\"CN\"},{\"name\":\"language\", \"value\":\"\"},{\"name\":\"version\", \"value\":\"\"},{\"name\":\"app_version\", \"value\":\"\"},{\"name\":\"device_hash\", \"value\":\"\"}]"
