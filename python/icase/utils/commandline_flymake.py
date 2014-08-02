# coding -*- utf-8 _8-
import copy


def buildList(input_items, input_index=0, result=None):
    if not result and input_index < len(input_items):
        result = []
        for subitem in input_items[input_index][1]:
            result.append({input_items[input_index][0]: subitem})
        return buildList(input_items, input_index+1, result)

    if input_index < len(input_items):
        tempresult = result
        result = []
        for subitem in input_items[input_index][1]:
            copiedresult = copy.deepcopy(tempresult)
            for index, item in enumerate(tempresult):
                copiedresult[index][input_items[input_index][0]] = subitem
            result.extend(copiedresult)
        return buildList(input_items, input_index+1, result)
    return result


class CommandLine(object):
    """Deal with commandline
    """
    def __init__(self, utilsHelper):
        self.utilsHelper = utilsHelper

    def parseCmdLine(self):

        import optparse
        usage = "usage: %prog [options] arg"
        parser = optparse.OptionParser(usage)
        parser.add_option('-p', '--product', dest='product',
                          help='contains product information')
        parser.add_option('-f', '--flash', dest='flash',
                          help='flash tool name and path: adb or delta')
        parser.add_option('-F', '--flash_args', dest='flash_args',
                          help='specify the flash file ')

        parser.add_option('-T', '--testtype', dest='testtype',
                          help='type of the test eg: \
marble,instrument,Monkey...')

        # marble params
        parser.add_option('-A', '--marbletool', dest='marbletool',
                          help='marble tools name eg: ../marble.py')

        parser.add_option('-t', '--testset', dest='testset',
                          help='test case configure contains test case')

        # instrument params
        parser.add_option('-a', '--apk', dest='apk', help='apk name')
        parser.add_option('-k', '--package', dest='package',
                          help='package name')
        parser.add_option('-e', '--testapk', dest='testapk',
                          help='testapk name')
        parser.add_option('-c', '--testpackage', dest='testpackage',
                          help='testpackage name')
        parser.add_option('-r', '--runner', dest='runner', help='runner name')

        # Monkey command
        parser.add_option('-O', '--Monkey', dest='Monkey', help='Monkey test')

        parser.add_option('-P', '--parameters', dest='parameters',
                          help='marble tools name eg: ../marble.py')
        parser.add_option('-R', '--result', dest='result',
                          help='result zip name')

        return parser.parse_args()

    def buildExtflashArgs(self, args):
        '''
        parse the flash_args 'custom='1.img,2.img;boot='boot.img'
        '''
        results = []
        if not args:
            return results

        partitions_files = args.split(';')
        for pAndf in partitions_files:
            # partition and file
            p_f = pAndf.split('=')
            if len(p_f) == 2:
                fs = p_f[1].split(',')
                fs = [subfs for subfs in fs if subfs]
                item = (p_f[0], fs)
                results.append(item)
                self.utilsHelper.debug.info(str(item))
    
        return results

    def getFlashArgs(self, args):
        '''
        args = [('',[]),('',[])...]
        return : [{}],{}]
        '''
        ret = self.buildExtflashArgs(args)
        return buildList(ret, 0, [])
