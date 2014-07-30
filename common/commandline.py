# -*- coding:utf-8-*-


class CommandLine(object):
    def parseCmdLine(self):
        import optparse
        usage = "usage: %prog [options] arg"
        parser = optparse.OptionParser(usage)
        parser.add_option('-p', '--product', dest='product',
                          help='contains product information')
        return parser.parse_args()

