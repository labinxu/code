# -*- coding:utf-8-*-


class CommandLine(object):
    def parseCmdLine(self):
        import optparse
        usage = "usage: %prog [options] arg"
        parser = optparse.OptionParser(usage)
        parser.add_option('-p', '--product', dest='PRODUCT',
                          help='contains product information')
        parser.add_option('-s', '--supplier', dest='SUPPLIER',
                          help='company info  from supplier search page')
        return parser.parse_args()

