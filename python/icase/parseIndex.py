import json
class IncludeFile:
    pass

def parseIncludejsonfile(file):
    f = open(file)
    jsoncode = json.loads(f.read())
    includeFile = IncludeFile()
    
    print type(jsoncode)
    if jsoncode.has_key("includes"):
        print 'has includes'
    
    for key,val in jsoncode.items():
        print key,val
        print type(key),type(val)
    f.close()
def main():
    parseIncludejsonfile("include.json")

if __name__ == "__main__":
    main()
