# coding -*- utf-8 _8-

import json


class JsonData(object):
    '''
    store the json file object
    '''
    def __init__(self, utilsHelper):
        self.utilsHelper = utilsHelper

    def displayAttributes(self):
        print 'displayAttributes'
        for name, value in vars(self).items():
            self.utilsHelper.debug('%s = %s' % (name, value))


class Device(JsonData):
    """
    store the devices.json data
    """
    def __init__(self, utilsHelper):
        JsonData.__init__(self, utilsHelper)


class DeviceParser(object):
    def __init__(self, utilsHelper, jsonfile):

        self.utilsHelper = utilsHelper
        self.devices = []
        # transfer jsonitem attributes field into device object
        with open(jsonfile) as f:
            try:
                decodeJson = json.loads(f.read())
                for jsonitem in decodeJson:
                    device = Device(self.utilsHelper)
                    for member, value in jsonitem['attributes'].items():
                        device.__setattr__(member, value)
                    self.devices.append(device)

            except KeyError, e:
                utilsHelper.debug.error("KeyError %s" % e)
                self.devices = []

    def getDevices(self):
        return self.devices
