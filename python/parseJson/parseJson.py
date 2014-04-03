#coding _*_ utf-8 _*_
import json
#f = open('test.json')
#f = open('device.json')
f = open('Att31D4.tmp.json')
#print f.read()
fjson = json.load(f)
fjson2 = json.loads(fjson[0]['status'])
print fjson2['id']

#fjson = json.dumps(f.read(), sort_keys = True,indent = 4, separators = (',', ':'))
#print fjson
#s = json.loads('{"name":"test", "type":{"name":"seq", "parameter":["1", "2"]}}')
