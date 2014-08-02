import datetime
import os
import glob
import re
import shutil
from utils.utils import utilsHelper, IcaseLogger, debug


class AutoToolsHelper():
    def __init__(self):
        self.verifyItems = {}
        
    def parseCmdLine(self):
        import optparse
        usage = "usage: %prog [options] arg"
        parser = optparse.OptionParser(usage)
        parser.add_option('-i', '--icase_path', dest='ICASE_PATH',
                          help='case path')
        parser.add_option('-I', '--icase_index', dest='ICASE_INDEX',
                          help='icase index')
        parser.add_option('-T', '--testtype', dest='TEST_TYPE',
                          help='type of the test eg: marble ...')

        parser.add_option('-R', '--icase_rev', dest='ICASE_REV',
                          help='icase rev')

        # marble params
        parser.add_option('-p', '--product', dest='PRODUCT',
                          help='The product name')
        parser.add_option('-t', '--target_product', dest='TARGET_PRODUCT',
                          help='The target product name')

        parser.add_option('-C', '--icase_split', dest='ICASE_SPLIT',
                          help='icase split parame')
        parser.add_option('-m', '--icase_mode', dest='ICASE_MODE',
                          help='icase mode')
        parser.add_option('-M', '--build_mode', dest='BUILD_MODE',
                          help='build mode')

        # instrument params

        parser.add_option('-g', '--gerrit_project', dest='GERRIT_PROJECT',
                          help='geritt programe path')

        parser.add_option('-b', '--branch', dest='BRANCH',
                          help='branch name')

        parser.add_option('-v', '--iverify', dest='IVERIFY',
                          help='IVERIFY feild')
        parser.add_option('-s', '--submit', dest='SUBMIT', help='submit')
        parser.add_option('-f', '--icase_flash',
                          dest='ICASE_FLASH',
                          help='icase flash')
 
        parser.add_option('-B', '--icase_debug',
                          dest='ICASE_DEBUG',
                          help='icase debug')

        parser.add_option('-o', '--target_build_variant',
                          dest='TARGET_BUILD_VARIANT',
                          help='target build variant')

        parser.add_option('-D', '--date', dest='DATE', help='date')

        parser.add_option('-a', '--icase_device',
                          dest='ICASE_DEVICE',
                          help='icase_device')

        parser.add_option('-d',
                          '--tool_debug',
                          dest='TOOL_DEBUG',
                          help='tool debug')

        parser.add_option('-e', '--tests_proj_filter',
                          dest='TESTS_PROJ_FILTER',
                          help='TESTS_PROJ_FILTER')

        parser.add_option('-c', '--icase_svn_rel',
                          dest='ICASE_SVN_REL',
                          help='ICASE_SVN_REL')

        return parser.parse_args()

    def getTriggerFolder(self, year, month, day):

        d = datetime.date(year, month, day)
        print year, month, day
        isoyear, isoweek, isoday = d.isocalendar()
        triggerFolder = '%d/wk%d' % (isoyear, isoweek)
        keywords = '%s%02d' % (('%d' % year)[2:], month)

        return (triggerFolder, keywords)
    
    def getfiles(self, findKeyWords):
        return glob.glob(findKeyWords)

    def buildDataFromInfofile(self, file):
        data = []
        print 'build %s' % file
        with open(file, 'r') as f:
            for line in f.readlines():
                if line == '\n':
                    debug.info('empty')
                    continue
                line = line[0:-1]
                vars = line.split('=')
                if len(vars) == 2:
                    data.append(vars)
                elif len(vars) == 3:
                    vars = [vars[0], vars[1] + '=' + vars[2]]
                    data.append(vars)
                else:
                    data.append(vars[0])
        return data
    
    def getVerifyItems(self, fileName):
        tempverfy = {}
        with open(fileName, 'r') as f:
            for line in f.readlines():
                line = line[0:-1]
                vars = line.split('=')
                if self.verifyItems.has_key(vars[0]):
                    tempverfy[vars[0]] = vars[1]

        return tempverfy

autoToolsHelper = AutoToolsHelper()


# compare the file modify date
def compare(xfile, yfile):
    stat_x = os.stat(xfile)
    stat_y = os.stat(yfile)
    if stat_x.st_ctime < stat_y.st_ctime:
        return 1
    elif stat_x.st_ctime > stat_y.st_ctime:
        return -1
    else:
        return 0


def compareFileName(xfile, yfile):
    xfile = xfile.replace('\\', '/')
    yfile = yfile.replace('\\', '/')
    xfileKey = re.match(".*wk\d{2}/(\d{12})", xfile).group(1)
    yfileKey = re.match(".*wk\d{2}/(\d{12})", yfile).group(1)

    if xfileKey < yfileKey:
        return 1
    elif xfileKey > yfileKey:
        return -1
    return 0


def buildCmdpara(cmdparams):
    cmdparams.DATE = cmdparams.DATE and cmdparams.DATE or str(datetime.date.today())
    cmdparams.PRODUCT =cmdparams.PRODUCT and cmdparams.PRODUCT or 'athena'
    cmdparams.TARGET_PRODUCT = cmdparams.TARGET_PRODUCT and cmdparams.TARGET_PRODUCT or cmdparams.PRODUCT

    cmdparams.TARGET_BUILD_VARIANT = cmdparams.TARGET_BUILD_VARIANT and cmdparams.TARGET_BUILD_VARIANT or 'user'

    ###########################
    # cmdparams.BRANCH = cmdparams.BRANCH and cmdparams.BRANCH or 'master'
    cmdparams.ICASE_PATH = cmdparams.ICASE_PATH and cmdparams.ICASE_PATH or ''
    cmdparams.IVERIFY = cmdparams.IVERIFY and cmdparams.IVERIFY or 'icase'
    cmdparams.ICASE_INDEX = cmdparams.ICASE_INDEX and cmdparams.ICASE_INDEX or ''
    cmdparams.TEST_TYPE = cmdparams.TEST_TYPE and cmdparams.TEST_TYPE or 'autotrigger'
    cmdparams.ICASE_SPLIT = cmdparams.ICASE_SPLIT and cmdparams.ICASE_SPLIT or ''
    cmdparams.BUILD_MODE = cmdparams.BUILD_MODE and cmdparams.BUILD_MODE or 'normal'
    cmdparams.ICASE_MODE = cmdparams.ICASE_MODE and cmdparams.ICASE_MODE or ''
    # cmdparams.TESTS_PROJ_FILTER = cmdparams.TESTS_PROJ_FILTER and cmdparams.TESTS_PROJ_FILTER or ''
    # more detail
    cmdparams.ICASE_DEVICE = cmdparams.ICASE_DEVICE and cmdparams.ICASE_DEVICE or 'DS.properties'
    # cmdparams.GERRIT_PROJECT = cmdparams.GERRIT_PROJECT and cmdparams.GERRIT_PROJECT or cmdparams.ICASE_PATH
    # cmdparams.TOOL_DEBUG = cmdparams.TOOL_DEBUG and cmdparams.TOOL_DEBUG or ''
    cmdparams.ICASE_DEBUG = cmdparams.ICASE_DEBUG and cmdparams.ICASE_DEBUG or None
    cmdparams.ICASE_FLASH = cmdparams.ICASE_FLASH and cmdparams.ICASE_PATH or ''
    cmdparams.ICASE_REV = cmdparams.ICASE_REV and cmdparams.ICASE_REV or 'HEAD'
    return cmdparams


def getNewestInfoTemplate(files, inputItems):
    for file in files:
        # debug.debug('check %s'%file)
        verifyItems = autoToolsHelper.getVerifyItems(file)
        if inputItems == verifyItems:
            return file
        
    return None


def buildCreateInfo(cmdparams):
    '''These keys will insert into result file
    '''
    createInfo = {}
    # createInfo['BRANCH'] = cmdparams.BRANCH
    createInfo['ICASE_PATH'] = cmdparams.ICASE_PATH
    if cmdparams.TESTS_PROJ_FILTER:
        createInfo['TESTS_PROJ_FILTER'] = cmdparams.TESTS_PROJ_FILTER
    createInfo['ICASE_DEVICE'] = cmdparams.ICASE_DEVICE
    createInfo['ICASE_INDEX'] = cmdparams.ICASE_INDEX
    createInfo['TEST_TYPE'] = cmdparams.TEST_TYPE
    createInfo['ICASE_SPLIT'] = cmdparams.ICASE_SPLIT
    createInfo['ICASE_SVN_REL'] = cmdparams.ICASE_SVN_REL
    createInfo['ICASE_MODE'] = cmdparams.ICASE_MODE
    createInfo['ICASE_DEBUG'] = cmdparams.ICASE_DEBUG
    createInfo['ICASE_REV'] = cmdparams.ICASE_REV
    createInfo['GERRIT_PROJECT'] = cmdparams.GERRIT_PROJECT
    # createInfo['TOOL_DEBUG']=cmdparams.TOOL_DEBUG
    return createInfo


def generateInfoFile(file, createInfo):

    filedata = autoToolsHelper.buildDataFromInfofile(file)
    file = file.replace('\\', '/')
    lfile = file.split('/')
    newfile = 'job.%s.%s' % (createInfo['TEST_TYPE'], lfile[-1])
    del createInfo['TEST_TYPE']
    with open(newfile, 'wb') as f:
        if filedata[0][0][0] == '#':
            f.write(filedata[0]+'\n')
        for key, var in filedata[1:]:
            if key in createInfo.keys():
                temvar = createInfo[key]
                print key
                if temvar and temvar != '':
                    var = createInfo[key]
                    debug.info('Set %s=%s' % (key, var))
                    f.write('%s=%s\n' % (key, var))
                else:
                    debug.info('Set %s=' % key)
                    f.write('%s=\n' % key)
                del createInfo[key]
            else:
                f.write('%s=%s\n' % (key, var))
        # write the other field
        for key, var in createInfo.items():
            debug.info('add new item %s=%s' % (key, var))
            f.write('%s=%s\n' % (key, var))

    return newfile


def getCopyableFile(destdir, newfile):
    while os.path.exists(os.path.join(destdir, newfile)):
        debug.info('%s is exists will make a new name' % newfile)
        m = re.match("(\S+)(\d{12})(\S+)", newfile)
        key = m.group(2)
        key = int(key)+1
        newfile = '%s%s%s' % (m.group(1), str(key), m.group(3))
        debug.info('new filename %s' % newfile)

    return newfile


def CommitToSVN(file):
    if os.path.exists(file):
        cmd = 'svn add %s' % file
        utilsHelper.runCommand(None, cmd)

        cmd = 'svn ci %s -m "%s"' % (file, 'trigger test')
        utilsHelper.runCommand(None, cmd)


def main():

    cmdparams, vars = autoToolsHelper.parseCmdLine()

    # find the week of
    cmdparams = buildCmdpara(cmdparams)

    inputItems = {
        'RESULT': 'SUCCESS',
        'TARGET_PRODUCT': cmdparams.PRODUCT,
        # 'TARGET_PRODUCT': cmdparams.TARGET_PRODUCT,
        # 'ICASE_DEBUG': cmdparams.ICASE_DEBUG,
        'ICASE_FLASH': cmdparams.ICASE_FLASH,
        'TARGET_BUILD_VARIANT': cmdparams.TARGET_BUILD_VARIANT,
        'BUILD_MODE': cmdparams.BUILD_MODE,
        # 'ICASE_MODE': cmdparams.ICASE_MODE
    }
    autoToolsHelper.verifyItems = inputItems
    print autoToolsHelper.verifyItems

    mydate = cmdparams.DATE.split('-')
    workspace = os.path.abspath(os.getcwd())
    triggerFolder, keywords = autoToolsHelper.getTriggerFolder(int(mydate[0]),
                                                               int(mydate[1]),
                                                               int(mydate[2]))
    destdir = '../%s' % triggerFolder
    # get the last update info files
    logger = IcaseLogger('autotrigger.log')
    utilsHelper.setLogger(logger)
    if os.path.exists(destdir):
        debug.info('cd in %s' % destdir)
        os.chdir(destdir)
        cmd = 'svn cleanup'
        utilsHelper.runCommand(logger, cmd)
        cmd = 'svn up'
        utilsHelper.runCommand(logger, cmd)
        debug.info('restore workspace %s' % workspace)
        os.chdir(workspace)
    else:
        print 'not exists %s' % destdir

    cmdparams.BRANCH = 'master'
    if cmdparams.BRANCH:
        findKeyWords = '../%s/%s*%s.info' % (triggerFolder,
                                             keywords, cmdparams.BRANCH)
        print findKeyWords

    files = autoToolsHelper.getfiles(findKeyWords)
    files.sort(compareFileName)
    resFile = getNewestInfoTemplate(files, inputItems)
    if resFile:
        createInfo = buildCreateInfo(cmdparams)
        print createInfo
        newfile = generateInfoFile(resFile, createInfo)

        tempfile = getCopyableFile(destdir, newfile)
        debug.debug('Move %s to %s' % (tempfile,
                                       os.path.join(destdir, tempfile)))
        if cmdparams.SUBMIT:
            #shutil.copy(newfile, os.path.join(destdir, tempfile))
            shutil.move(newfile, os.path.join(destdir, tempfile))
            CommitToSVN(os.path.join(destdir, tempfile))
    else:
        debug.info('No template found')


if __name__ == "__main__":
    main()
