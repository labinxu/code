
import os, zipfile, subprocess, shutil, sys, fnmatch, fileinput, re, time, traceback, glob 

# .NET imports 
import clr 

clr.AddReference('FuseHandler') 
from FuseHandler import * 

clr.AddReference('System.Xml') 
from System.Xml import XmlDocument 


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
        print 'command is:' + command 
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

    def runFlasher(self, products, toolArguments, logfilename): 
        exitcode = 0 

        command = 'flasher.exe ' 

        # Add connection parameters 
        for product in products: 
            if 'main' in product.role in product.role: 
                command += '--guid ' + product.detailedConnectionId + ' ' + toolArguments 
                print command 
                exitcode = self.run(command, logfilename) 
                if exitcode != 0: 
                    raise ExecutorError('Flashing tool failed', exitcode) 
                command = 'flasher.exe ' 
            elif 'remote' in product.role: 
                print 'Remote product will not be flashed' 
            elif 'reference' in product.role: 
                print 'Reference product will not be flashed' 

    def runGranite(self, toolArguments, logfilename): 
        exitcode = 0 

        command = 'ipy granite.py ' 

        # Setup product configurations 
        jsonFilelist = glob.glob(self.workspace + '/*.json') 
        for jsonFile in jsonFilelist: 
            productName = os.path.basename(jsonFile) 
            pythonName = productName.replace('.json', '.py') 
            pyFile = self.workspace + '/granite/settings/default/' + pythonName 
            print 'Python file reference check for removal : ' + os.path.abspath(pyFile) 
            if os.path.exists(pyFile): 
                print 'Removing file: ' + pyFile 
                os.remove(pyFile) 
            targetDir = self.workspace + '/granite/settings/default' 
            print 'Copying product file from: ' + os.path.abspath(jsonFile) 
            print 'Copying product file to: ' + os.path.abspath(targetDir) 
            shutil.copy(jsonFile, targetDir) 

        # Prepare command 
        command += toolArguments 
        print command 
        exitcode = self.run(command, logfilename) 
        if exitcode != 0: 
            raise ExecutorError('Granite tool failed', exitcode) 

    def runCtt(self, products, toolArguments, logfilename): 
        exitcode = 0 
        remoteDeclared = False 

        command = self.workspace + '/ctt/ExecutionForm.exe' 

        # Add connection parameters 
        for product in products: 
            commandParameter = '' 
            if 'main' in product.role: 
                commandParameter = ' PrimaryConnectionString:"Guid:' 
            elif 'remote' in product.role: 
                commandParameter = ' SecondaryConnectionString:"Guid:' 
                remoteDeclared = True 
            elif 'reference' in product.role and False == remoteDeclared: 
                commandParameter = ' SecondaryConnectionString:"Guid:' 

            # Add connection if found 
            if len(commandParameter) > 0: 
                command += commandParameter + product.detailedConnectionId 
                command += '" ' 

        command += toolArguments 

        if len(products) > 0: 
            print command 
            exitcode = self.run(command, logfilename) 
            if exitcode != 0: 
                raise ExecutorError('CTT tool failed', exitcode) 


class product: 
    role = '' 
    imei = '' 
    connectionId = '' 
    detailedConnectionId = '' 
    productConfXml = '' 

    def __init__(self, arguments): 
        self.separateArguments(arguments) 

    def showDetails(self): 
        print ' --- PRODUCT --- ' 
        print 'IMEI:                 ' + self.imei 
        print 'Role:                 ' + self.role 
        print 'ConnectionId:         ' + self.connectionId 
        print 'DetailedConnectionId: ' + self.detailedConnectionId 
        print ' --------------- ' 

    def separateArguments(self, arguments): 
        try: 
            print 'Processing product arguments...' 
            # Parse arguments to separated details 
            if len(arguments) > 0: 
                print 'Splitting arguments...' 
                splittedArguments = re.split(':', arguments) 
                self.role = splittedArguments[0] 
                self.productConfXml = splittedArguments[1] + ':' + splittedArguments[2] 
                print 'Arguments splitted.' 
                if os.path.exists(self.productConfXml): 

                    print 'Product configuration file exists.' 

                    # Get product identifier from file name 
                    print 'Parse IMEI from file name...' 
                    self.imei = os.path.splitext(os.path.basename(self.productConfXml))[0] 

                    # Parse data from the xml file to variables 
                    print 'Find product node...' 
                    productNode = None 
                    sourceXml = XmlDocument() 
                    sourceXml.Load(self.productConfXml) 

                    # search correct product node according to given identifier (imei) 
                    for node in sourceXml.SelectNodes('//product'): 
                        if node.SelectSingleNode('imei[text()="%s"]' % self.imei): 
                            print 'Product node found.' 
                            productNode = node 
                            break 

                    # get setting from product node 
                    if productNode: 
                        print 'Set data...' 
                        self.connectionId = productNode.SelectSingleNode('fuse-connection-name').InnerText 
                        self.detailedConnectionId = productNode.SelectSingleNode('fuse-connection-id').InnerText 
                        print 'Processing product arguments finished.' 
                    else: 
                        raise ExecutorError('Unable to find product node', 1) 
                else: 
                    raise ExecutorError('Unable to find product configuration file', 1) 
            else: 
                raise ExecutorError('Product arguments not found', 1) 
        except Exception as e:
            raise ExecutorError('Cannot process product arguments: ' + e.message, 1) 


class fuseConnectionHandler: 
    def __init__(self): 
        self.fuseHandler = FuseHandler() 

    def addConnection(self, connectionName, tcpAddress): 
        self.fuseHandler.addConnection(connectionName, tcpAddress) 

    def removeConnections(self): 
        self.fuseHandler.removeConnections() 


class ExecutorError(Exception): 
    message = '' 
    errorCode = 0 
    def __init__(self, message, errorCode): 
        self.message = message 
        self.errorCode = errorCode 


def main(): 

    # Fuse connection handler 
    fuseHandlers = list() 
    exitMessage = 'Success' 
    exitCode = 0 

    try: 
        execution(fuseHandlers) 
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
        for fuseHandler in fuseHandlers: 
            # Remove NoSE connection from Fuse 
            print 'CLEANUP: Removing NoSE connections from Fuse... ' 
            fuseHandler.removeConnections() 

    return exitMessage, exitCode 


def execution(fuseHandlers): 

    # Product list 
    products = list() 

    # Go through arguments
    for arg in sys.argv: 
        if 'main' in arg or 'remote' in arg or 'reference' in arg: 
            newProduct = product(arg) 
            newProduct.showDetails() 
            products.append(newProduct) 

    # Workspace for launch dir 
    workspace = os.getcwd() 
    print 'Workspace directory: ' + workspace 


    # Unpack Data by running 7zip command 
    if ((os.path.exists('data.zip')) or ('*' in 'data.zip')): 
        print 'Unpacking data from data.zip' 

        # Run command 
        print 'Executing command: 7z x "'+os.path.abspath('data.zip')+ '" -y' 
        tool = commandTool(workspace) 
        exitcode = tool.run('7z x "'+os.path.abspath('data.zip')+ '" -y', 'data_extraction.log') 
        print 'data.zip unpacked successfully' 
    else: 
        raise ExecutorError('data.zip does not exist!', 1) 


    # Unpack Data by running 7zip command 
    if ((os.path.exists('flasher.zip')) or ('*' in 'flasher.zip')): 
        print 'Unpacking data from flasher.zip' 

        # Run command 
        print 'Executing command: 7z x "'+os.path.abspath('flasher.zip')+ '" -y' 
        tool = commandTool(workspace) 
        exitcode = tool.run('7z x "'+os.path.abspath('flasher.zip')+ '" -y', 'flasher_extraction.log') 
        print 'flasher.zip unpacked successfully' 
    else: 
        raise ExecutorError('flasher.zip does not exist!', 1) 


    # Launch Flasher 
    tool = commandTool(workspace) 
    tool.runFlasher(products, '--mcusw "rm921_0.1346.0.mcusw.fpsx" --type "usb" --image "rm921_0.1346.0_059S5Z6_ch1.image.fpsx" --rofs "rm921_0.1346.0_059S5Z6_ch1.rofs.fpsx" --adl "4" ', 'flash.log') 


    # Compress results 
    print 'compressing test results to results.zip' 
    zf = zipfile.ZipFile('results.zip', 'a') 
    try: 
        print 'adding flash.log' 
        zf.write('flash.log') 
    finally: 
        zf.close() 


    # Unpack Data by running 7zip command 
    if ((os.path.exists('granite.zip')) or ('*' in 'granite.zip')): 
        print 'Unpacking data from granite.zip' 

        # Run command 
        print 'Executing command: 7z x "'+os.path.abspath('granite.zip')+ '" -y' 
        tool = commandTool(workspace) 
        exitcode = tool.run('7z x "'+os.path.abspath('granite.zip')+ '" -y', 'granite_extraction.log') 
        print 'granite.zip unpacked successfully' 
    else: 
        raise ExecutorError('granite.zip does not exist!', 1) 


    # Change directory 
    print 'Changing to directory: granite/framework' 
    os.chdir("granite/framework") 
    print 'Current directory: ' + os.getcwd() 


    # Launch Granite 

    try: 
        testXmls = glob.glob(workspace + '/tests*.xml') 
        for testXml in testXmls: 
            print 'Processing file ' + os.path.abspath(testXml) 
            sourceXml = XmlDocument() 
            sourceXml.Load(testXml) 

            # search all file nodes 
            for node in sourceXml.SelectNodes('//tests/test'): 
                fileName = node.GetAttribute('path') 
                print 'Old path: ' + fileName 
                newName = workspace + '/' + fileName 
                newName = newName.replace("\\", "/") 
                node.SetAttribute('path', newName) 
                fileName = node.GetAttribute('path') 
                print 'New path: ' + fileName 
            sourceXml.Save(testXml) 
    except Exception as e:  
        raise ExecutorError('Cannot process product arguments: ' + e.message, 1) 

    compiledCommand = '--settings_dir "' + workspace + '/granite/settings/default" --ci_enabled  --test_set "' + workspace + '/granite/test_sets/tool_stability.testset" --pmd "' + workspace + '/rm921_0.1346.0.mcusw.fpsx.pmd" ' 
    modifiedArguments = compiledCommand.replace("\\", "/") 
    tool = commandTool(workspace) 
    tool.runGranite(modifiedArguments, 'granite.log') 


    # Change directory 
    print 'Changing to directory: ../..' 
    os.chdir("../..") 
    print 'Current directory: ' + os.getcwd() 


    # Find matching files 
    print 'Searching for test results...' 
    matches = [] 
    for root, dirnames, filenames in os.walk('granite/framework/test_results'): 
        hits = 0 
        print 'searching for * in %s' % root 
        for filename in fnmatch.filter(filenames, '*'): 
            matches.append(os.path.join(root, filename)) 
            hits += 1 
        print 'matches found: %s' % hits 

    print 'total of %s matches found' % len(matches) 

    # Delete temporary results if exists 
    # Compress results 

    # Compress results 
    print 'compressing test results to results.zip' 
    zf = zipfile.ZipFile('results.zip', 'a') 
    try: 
        for filename in matches: 
            print 'adding %s' % filename 
            zf.write(filename) 
    finally: 
        zf.close() 


if __name__ == '__main__': 
    exitMessage, exitCode = main() 
    print exitMessage + ' [ %d ] ' % exitCode 
    sys.exit(exitCode) 

