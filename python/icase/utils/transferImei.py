# coding -*- utf-8 _8-
import sys
import os
if '../' not in sys.path:
    sys.path.append('../')


def transImei(imei):
    if 'A' in imei:
        imei = list(imei)
        size = len(imei)
        for i in range(0, size, 2):
            if i+1 < size:
                imei[i], imei[i+1] = imei[i+1], imei[i]
    return ''.join(imei[1:])


def transferIMEI(conf):
    import xml.etree.ElementTree as ET
    doc = ET.parse(conf)
    root = doc.getroot()
    propertys = []
    for devices in root.findall('devices'):
        for device in devices.findall('device'):
            port = device.get('port')
            imei = device.get('imei')
            propertys.append((port, imei))
    devicesEle = root.find('devices')
    for port, imei in propertys:
        device = ET.SubElement(devicesEle, 'device')
        device.set('port', port)
        device.set('imei', transImei(imei))
    doc.write(conf)

if os.path.exists('config.xml'):
    transferIMEI('config.xml')
