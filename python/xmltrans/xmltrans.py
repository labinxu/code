#coding uft-8
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def getfiledata(files):
    tree = ET.ElementTree(file=files)
    return [(elem.attrib['id'], elem.attrib['translation']) for elem in tree.iterfind(".//text")]

def transFile(srcfile, destfile):

    header ='<TSPKG><TSPKG xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n\
    <TS language="en-GB" lang-name="English" layout-direction="left-to-right" localized-numerals="0123456789" number-format-changeable="true" number-of-strings="2923">\n'
    file = open(file=destfile, mode='w',encoding='utf8')
    file.write(header)
    elemTemp = '\
     <message id="%s" >\n\
       <original>%s</original>\n\
       <translation translated="yes">%s</translation>\n\
     </message>\n'
    for id, text in getfiledata(srcfile):
        #file.write(elemTemp%((id,text,text)))
        file.write(elemTemp%((id,text,text)))
        #pass
    tail ='</TS>\n</TSPKG></TSPKG>'
    file.write(tail)
    file.close()

if __name__ == '__main__':
    transFile('Main_texts.xml','en-GB.xml')

