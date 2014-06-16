import re, sys, os, glob
import xml.etree.cElementTree as ET
TotalExeTime = 0

class TestCase:
    name = ''
    className = ''
    result = ''
    #message = ''
    details = ''
    starttime='0'
    endtime='0'
    runtime='0'
    def setStartTime(self,starttime):
        self.starttime = starttime
    def setEndTime(self,endtime):
        self.endtime = endtime
    def setRunTime(self,runtime):
        self.runtime = runtime
    def getStarttime(self):
        return self.starttime
    def getEndtime(self):
        return self.endtime
    def getRuntime(self):
        return self.runtime

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    '''
    def setMessage(self, message):
        self.message = message

    def getMessage(self):
        return self.message
    '''

    def setDetails(self, details):
        self.details = details

    def getDetails(self):
        return self.details

    def setClassName(self, className):
        self.className = className

    def getClassName(self):
        return self.className

    def setResult(self, result):
        self.result = result

    def getResult(self):
        return self.result


def parseCase(lines):
    testCase = TestCase()
    detailsStart = -1
    for index, line in enumerate(lines):
        if 'Starttime:' in line:
            splits = line.split('=')
            if len(splits)>=2:
                testCase.setStartTime(splits[1].strip())
        if 'Endtime:' in line:
            splits = line.split('=')
            if len(splits)>=2:
                testCase.setEndTime(splits[1].strip())
        if 'Time:' in line:
            splits = line.split('=')
            if len(splits)>=2:
                testCase.setRunTime(splits[1].strip())

        if 'INSTRUMENTATION_STATUS: test=' in line:
            splits = line.split('=')
            if len(splits) >= 2:
                testCase.setName(splits[1].strip())
        if 'INSTRUMENTATION_STATUS: class' in line:
            splits = line.split('=')
            if len(splits) >= 2:
                testCase.setClassName(splits[1].strip())
        if 'Error in' in line:
            testCase.setResult('error')
            detailsStart = index + 1
        if 'INSTRUMENTATION_STATUS: Error' in line:
            testCase.setResult('error')
            testCase.setDetails(line.split('=')[1])
        if 'Failure in' in line:
            testCase.setResult('failed')
            detailsStart = index + 1
        if detailsStart >= 0:
            if 'INSTRUMENTATION_STATUS: numtests=' in line:
                details = ''.join(lines[detailsStart:index])
                testCase.setDetails(details.strip())

    if testCase.getResult().isspace():
        testCase.setResult('passed')

    return testCase


'''
def getPassedNum(lines):
    po = re.compile('OK\s+\((\d+)\s+tests\)')
    num = 0
    for line in lines.reverse():
        matchResult = po.findall(line)
        if len(matchResult) >= 1 and matchResult[0].isdigit():
            num = int(matchResult[0])
            break
    return num

def getFailureErrorNum(lines):
    po = re.compile('Tests run:\s+\d+,\s+Failures:\s+(\d+),\s+Errors:\s+(\d+)')
    failureNum = 0
    errorNum = 0
    for line in lines.reverse():
        matchResult = po.findall(line)
        if len(matchResult) >= 2 and matchResult[0].isdigit() and matchResult[1].isdigit():
            failureNum = int(matchResult[0])
            errorNum = int(matchResult[1])
            break
    return (failureNum, errorNum)

def getAbstract(lines):
    abstract = {'tests':0, 'failures':0, 'errors':0}
    if 'FAILURES!!!\r\n' in lines or 'FAILURES!!!' in lines:
        (failureNum, errorNum) = getFailureErrorNum(lines)
        abstract['failures'] = failureNum;
        abstract['errors'] = errorNum;
    else
        abstract['tests'] = getPassedNum(lines)        
    return abstract

def getClassName(lines):
    po = re.compile('INSTRUMENTATION_STATUS:\s+class=(.+)')
    classname = ''
    for line in lines:
        matchResult = po.findall(line)
        if len(matchResult) >= 1:
            classname = matchResult[0]
            break
    return classname

def getCaseNames(lines):
    po = re.compile('INSTRUMENTATION_STATUS:\s+test=(.+)')
    caseNames = []
    for line in lines:
        matchResult = po.findall(line)
        if len(matchResult) >= 1 and matchResult[0] not in caseNames:
            caseNames.append(matchResult[0])
    return caseNames

def getCases(lines):
    caseNames = getCaseNames(lines)
    cases = []
    for caseName in caseNames:
        cases.append({'name':caseName, ''})
'''

'''
result = 
{
    'classname' : classname
    'abstract'  : {'tests':xx, 'passed':xx, 'failures':xx, 'errors':xx}
    'cases'     : [
                      {'name':casename, 'message':'Error'/'Failure', 'detail':detail}
                      {}
                      {}
                      ...
                  ]
}

INSTRUMENTATION_STATUS_CODE
0:      OK
1:      START
-1:     ERROR
-2:     FAILURE
'''
def getExecuteTime(lines):
    global TotalExeTime
    tmptime = 0
    try:
        for index in range(len(lines)-1,-1,-1):

            if 'Time: ' in lines[index]:
                TotalExeTime -= tmptime
                TotalExeTime += float(lines[index][0:-1].split('Time: ')[1])
            if 'Time:='in lines[index]:
                tmptime = float(lines[index][0:-1].split('Time:=')[1])
                TotalExeTime += tmptime
    except Exception,e:
        print e
def parseJUnitLog(logFile):
    cases = []
    with open (logFile) as file:
        lines = file.readlines()
        getExecuteTime(lines)
        caseStart = -1;
        counter = 0
        tmpfile = logFile.replace('\\','/')
        tmpfile = tmpfile.split('/')
        tmpclassname = tmpfile[-1][0:-4]
        for index, line in enumerate(lines):
            if 'INSTRUMENTATION_STATUS: numtests' in line:
                if counter % 2 == 0:
                    if (caseStart >= 0):
                        case = parseCase(lines[caseStart:index])
                        if len(case.getClassName())==0:
                            case.className = tmpclassname
                        cases.append(case)

                    caseStart = index
                counter += 1
        if len(cases)==0:
            caseStart=1
        case = parseCase(lines[caseStart:len(lines)])
        if len(case.getClassName())==0:
            case.className = tmpclassname
        cases.append(case)
        
    '''
    for case in cases:
        print case.getName()
        print case.getClassName()
        print case.getResult()
        print case.getDetails()
        print '\r\n'
    '''
    return cases


'''
def parseJUnitLogs(workspace):
    mappedTests = {}

    resultFolders = glob.glob(workspace + '/result*')
    for resultFolder in resultFolders:
        logs = glob.glob(resultFolder + '/*.log')
        for log in logs:
            print "Processing log file '%s' ..." % os.path.abspath(log)
            cases = parseJUnitLog(log)
            mappedTests[os.path.basename(log)] = cases

    return mappedTests
'''
def parseJUnitLogs(workspace):
    mappedTests = {}
    # Folder structure should be like this:
    # workspace 
    # ----results
    # --------NotePad
    # ------------result.log            (Could be any name that ends with '.log')
    # --------Calculator
    # ------------result.log            (Could be any name that ends with '.log')
    #extact the result.zip

    items = glob.glob(workspace + '/results/*')
    for item in items:
        if not os.path.isfile(item):
            logs = glob.glob(item + '/*.log')
            if len(logs)==0:
                print 'can not found log '
                return
            mappedTests[os.path.basename(item)] = []
            for log in logs:
                print "Processing log file '%s' ..." % os.path.abspath(log)
                cases = parseJUnitLog(log)
                mappedTests[os.path.basename(item)].extend(cases)
                print os.path.basename(item)

    return mappedTests


def createNJUnitReport(mappedTests,destFile):
    testSuites = ET.Element('testsuites')
    global TotalExeTime
    for key in mappedTests:

        # Create a name for test suite
        #testSuiteName = key.replace(".log", "").strip()
        testSuiteName = key
        testSuite = ET.SubElement(testSuites, 'testsuite')
        testSuite.set('name', testSuiteName)
        testSuite.set('time', str(TotalExeTime))
        for testCase in mappedTests[key]:
            testCaseElement = ET.SubElement(testSuite, 'testcase')
            testCaseElement.set('classname', testCase.getClassName())
            testCaseElement.set('name', testCase.getName())
            testCaseElement.set('start_time',testCase.getStarttime())
            testCaseElement.set('stop_time',testCase.getEndtime())
            testCaseElement.set('time',testCase.getRuntime())
            result = testCase.getResult()
            if 'failed' in result:
                failure = ET.SubElement(testCaseElement, 'failure')
                failure.set('details', testCase.getDetails())
                failure.set('message', 'Failure')
            if 'error' in result:
                error = ET.SubElement(testCaseElement, 'failure')
                error.set('details', testCase.getDetails())
                error.set('message', 'Error')

    tree = ET.ElementTree(testSuites)
    print 'write',destFile
    tree.write(destFile)
#    tree.write('njunit.xml')

def parse(destfile):
    global TotalExeTime
    TotalExeTime = 0
    workspace = os.getcwd()
    print 'junit: workspace %s'%workspace
    mappedTests = parseJUnitLogs(workspace)
    createNJUnitReport(mappedTests,destfile)

if __name__ == '__main__':
    print 'enter'
    parse('njunit.xml')


'''
if __name__ == '__main__':
    if len(sys.argv) >= 3:
        print "Info: start parsing '%s' log file '%s'" % (str(sys.argv[2]), str(sys.argv[1]))
        parse(sys.argv[1], sys.argv[2])
        print "\nInfo: Done"
    elif len(sys.argv) == 2:
        print "Info: start parsing junit log file '%s'" % str(sys.argv[1])
        parse(sys.argv[1])
        print "\nInfo: Done"
    else:
        print 'Error: please specify log file and log file type!'
'''
