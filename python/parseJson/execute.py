
import os, zipfile, subprocess, shutil, sys, fnmatch, fileinput, re, time, traceback, glob,json


class writer: 
    def __init__(self, logfile, stdout): 
        self.stdout = stdout 
        self.logfile = logfile 
        self.log = file(logfile, 'w') 
    def write(self, text): 
        self.stdout.write(text) 
        self.log.write(text) 
        self.stdout.flush() 
        self.log.flush() 
    def store(self, workspace): 
        print 'compressing test results to ' + workspace + '/results.zip' 
        zf = zipfile.ZipFile(workspace + '/results.zip', 'a') 
        try: 
            print 'adding ' + self.logfile 
            zf.write(self.logfile) 
        finally: 
            zf.close() 


class commandTool: 
    def __init__(self, workspace): 
        self.workspace = workspace 

    def run(self, command, logfilename): 
        exitcode = 0 
        try: 
            tool = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT) 
            toolOutputs = tool.stdout 
            logger = writer(logfilename, sys.stdout) 
            sys.stdout = logger 

            while 1: 
                outputFromTool = toolOutputs.readline() 
                time.sleep(1.0 / 1000.0) 
                if not outputFromTool: 
                    break 

                print 'Tool: ' + outputFromTool 

            exitcode = tool.wait() 
            sys.stdout = sys.__stdout__ 
            logger.store(self.workspace) 
            print 'Tool execution finished' 
        except OSError, e:
            sys.stdout = sys.__stdout__ 
            print 'An error occured during execution: ', e 
        except: 
            sys.stdout = sys.__stdout__ 
            print 'Unexpected error:', sys.exc_info()[0] 
            exitMessage = 'Failure: Unknown reason' 

        return exitcode 

    def runMonkey(self, toolArguments, logfilename): 
        exitcode = 0 

        # Prepare command 
        command='adb' 
        command += toolArguments 
        print command 
        exitcode = self.run(command, logfilename) 
        if exitcode != 0: 
            raise ExecutorError('Granite tool failed', exitcode) 

class product: 
    role = '' 
    imei = '' 
    connectionId = '' 
    detailedConnectionId = '' 
    productConfXml = '' 

    def __init__(self): 
        self.parseJson() 

    def showDetails(self): 
        print ' --- PRODUCT --- ' 
        print 'IMEI:                 ' + self.imei 
        print 'Role:                 ' + self.role 
        print 'ConnectionId:         ' + self.connectionId 
        print 'DetailedConnectionId: ' + self.detailedConnectionId 
        print ' --------------- ' 

    def parseJson(self):
        f=open('device.json')
        try: 
            print 'parse json start...'             
            content=f.read()
            encodedContent=json.dumps(content)
            decodeJson=json.loads(encodedContent)
            print type(decodeJson)          
           
                
        except Exception as e:
            raise ExecutorError('Cannot process product arguments: ' + e.message, 1)
        finally:
            f.close()
        
        

class ExecutorError(Exception): 
    message = '' 
    errorCode = 0 
    def __init__(self, message, errorCode): 
        self.message = message 
        self.errorCode = errorCode 


def main(): 

    exitMessage = 'Success' 
    exitCode = 0 

    try: 
        execution() 
    except ExecutorError as e: 
        # Known reason 
        exitMessage = 'Failure: ' + e.message 
        exitCode = e.errorCode 
    except Exception as e: 
        # Unknown reason 
        print 'Unexpected error: ' + e.message 
        print traceback.print_exc() 
        exitMessage = 'Failure: Unknown reason' 
        exitCode = 1 
    finally: 
        print 'CLEANUP: Removing NoSE connections from Fuse... ' 

    return exitMessage, exitCode 


def execution(): 
    # Product list 
    products = list() 
    newProduct = product()
    #newProduct.showDetails() 
    #products.append(newProduct) 
    # Workspace for launch dir 
    workspace = os.getcwd() 
    print 'Workspace directory: ' + workspace 

    compiledCommand =' -s emulator-5554 shell monkey --throttle 500 -s 100 -v -v -v 1000' 
    print 'Workspace directory: ' + workspace 
    tool = commandTool(workspace) 
    #tool.runMonkey(compiledCommand, 'Monkey.log') 


if __name__ == '__main__': 
    exitMessage, exitCode = main() 
    print exitMessage + ' [ %d ] ' % exitCode 
    sys.exit(exitCode) 

