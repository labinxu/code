#coding _*_ utf-8 _*_
import json
#f = open('test.json')
#f = open('device.json')
#f = open('Att31D4.tmp.json')
#print f.read()
#fjson = json.load(f)
#fjson2 = json.loads(fjson[0]['status'])
#print fjson2['id']

#fjson = json.dumps(f.read(), sort_keys = True,indent = 4, separators = (',', ':'))
#print fjson
#s = json.loads('{"name":"test", "type":{"name":"seq", "parameter":["1", "2"]}}')
class product: 

    def __init__(self): 
        #self.parseJson() 
        self.imei=None
        self.role=None
        self.connectionId=None
        self.detailedConnectionId=None
        
    def showDetails(self): 
        print ' --- PRODUCT --- ' 
        print 'IMEI:                 %s'% str(self.imei) 
        print 'Role:                 %s'% str(self.role)
        print 'ConnectionId:         %s'% str(self.connectionId)
        print 'DetailedConnectionId: %s'% str(self.detailedConnectionId)
        print ' --------------- ' 

    def parseJson(self):
        f = open('./test_multi.json')
        try: 
            print 'parse json start...'             
            decodeJson = json.loads(f.read())
            self.imei=decodeJson[1]['attributes']['imei']
            self.role=decodeJson[1]['role']
            self.detailedConnectionId=decodeJson[1]['id'] 
            decodeStatus=json.loads(decodeJson[1]['status'])
            self.connectionId=decodeStatus['id']
                
            
            
        except Exception as e:
            raise ExecutorError('Cannot process product arguments: ' + e.message, 1)
        finally:
            f.close()
pro = product()
pro.parseJson()
pro.showDetails()
