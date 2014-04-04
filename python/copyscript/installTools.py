#coding -*- utf-8 -*-
import os, re
import environment as ENV
import debug

class SetUptools(object):
    def __init__(self):
        self.environ = ENV.CreateEnvhelper()

    def getAppdir(self, paths, appname):

        #replace the path reference
        for dir in paths:
            ret = re.match('%.*%', dir)
            if ret:
                refer = self.environ.getenv(ret.group(0)[1:-1])
                if refer:
                    dir = dir.replace(ret.group(0),refer)
                else:
                    debug.debug('%s not found in environment' % ret.group(0)[1:-1])
                    return None
                    
            for root, dirs, files in os.walk(dir, topdown = True):
                for file in files:
                    if file in [appname+'.exe', appname, appname+'.sh']:
                        debug.debug('Found %s in %s' % (appname, root))
                        return root
        return None
    
    def checkEnv(self, name):
        assert len(name) > 0
        ret = self.environ.getenv(name)
        if ret:
            debug.debug("%s is %s" % (name, ret))
            return True
        debug.debug('%s is not found' % name)
        return False
    
    def checkAppPath(self, appname,dirName=None, path='path'):

        assert appname
        paths = self.environ.getenv(path)
        if not paths:
            return None
        if not dirName:
            paths = [dir for dir in paths.split(self.environ.envPathSeparate) \
                 if appname.lower() in dir.lower()]
        else:
             paths = [dir for dir in paths.split(self.environ.envPathSeparate) \
                    if dirName.lower() in dir.lower()]

        return self.getAppdir(paths,appname)
