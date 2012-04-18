###########################################################################
#
# Copyright (C) 2012, Jason Harvey
# Based on code by Zenoss, Inc. -- Copyright (C) 2008, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
###########################################################################

__doc__='''HAProxyDataSource.py

Defines datasource for HAProxy
'''

import Products.ZenModel.BasicDataSource as BasicDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import ClassSecurityInfo, Permissions
from Products.ZenUtils.ZenTales import talesCompile, getEngine

import os

class HAProxyDataSource(ZenPackPersistence,
                                BasicDataSource.BasicDataSource):
    SOURCETYPE = 'HAProxy'

    ZENPACKID = 'ZenPacks.community.HAProxy'

    # Mostly for my info; can probably be removed
    DATAPOINTS = ('pxname', 'svname', 'qcur', 'qmax', 'scur', 'smax', 'slim', 'stot', 'bin', 'bout',
                  'dreq', 'dresp', 'ereq', 'econ', 'eresp', 'wretr', 'wredis', 'status', 'weight', 'act',
                  'bck', 'chkfail', 'chkdown', 'lastchg', 'downtime', 'qlimit', 'pid', 'iid', 'sid',
                  'throttle', 'lbtot', 'tracked', 'type', 'rate', 'rate_lim', 'rate_max', 'check_status',
                  'check_code', 'check_duration', 'hrsp_1xx', 'hrsp_2xx', 'hrsp_3xx', 'hrsp_4xx', 'hrsp_5xx',
                  'hrsp_other', 'hanafail', 'req_rate', 'req_rate_max', 'req_tot', 'cli_abrt', 'srv_abrt')

    sourcetypes = (SOURCETYPE,)
    sourcetype = SOURCETYPE

    timeout = 15
    eventClass = '/Status/Web'

    hostname = '${dev/manageIp}'
    server = '${dev/componentId}'
    servertype = 'BACKEND'
    port = '80'
    ssl = False
    url = '/haproxy_stats;csv'

    _properties = BasicDataSource.BasicDataSource._properties + (
            {'id':'timeout', 'type':'int', 'mode':'w'},
            {'id':'eventClass', 'type':'string', 'mode':'w'},
            {'id':'hostname', 'type':'string', 'mode':'w'},
            {'id':'port', 'type':'string', 'mode':'w'},
            {'id':'ssl', 'type':'boolean', 'mode':'w'},
            {'id':'url', 'type':'string', 'mode':'w'},
            {'id':'server', 'type':'string', 'mode':'w'},
            {'id':'servertype', 'type':'string', 'mode':'w'},
            )

    _relations = BasicDataSource.BasicDataSource._relations + (
            )

    factory_type_information = (
        {
            'immediate_view': 'editHAProxyDataSource',
            'actions':
            (
                { 'id': 'edit',
                  'name': 'Data Source',
                  'action': 'editHAProxyDataSource',
                  'permissions': ( Permissions.view ),
                },
            )
        },
    )

    security = ClassSecurityInfo()


    def __init__(self, id, title=None, buildRelations=True):
        BasicDataSource.BasicDataSource.__init__(self, id, title,
                buildRelations)


    def getDescription(self):
        if self.sourcetype == self.SOURCETYPE:
            return self.hostname
        return BasicDataSource.BasicDataSource.getDescription(self)


    def useZenCommand(self):
        return True


    def getCommand(self, context):
        parts = ['check_haproxy.py']
        if self.hostname:
            parts.append('-H %s' % self.hostname)
        if self.port:
            parts.append('-p %s' % self.port)
        if self.ssl:
            parts.append('-s')
        if self.url:
            parts.append("-u '%s'" % self.url)
        if self.server:
            parts.append("-S '%s'" % self.url)
        if self.servertype:
            parts.append("-T '%s'" % self.url)
        cmd = ' '.join(parts)
        cmd = BasicDataSource.BasicDataSource.getCommand(self, context, cmd)
        return cmd

    def checkCommandPrefix(self, context, cmd):
        if self.usessh:
            return os.path.join(context.zCommandPath, cmd)
        zp = self.getZenPack(context)
        return zp.path('libexec', cmd)


    def addDataPoints(self):
        for dpname in ('totalAccesses', 'totalKBytes'):
            dp = self.manage_addRRDDataPoint(dpname)
            dp.rrdtype = 'DERIVE'
            dp.rrdmin = 0

        for dpname in ('bytesPerReq', 'cpuLoad', 'slotDNSLookup',
            'slotKeepAlive', 'slotLogging', 'slotOpen', 'slotReadingRequest',
            'slotSendingReply', 'slotWaiting'):

            dp = self.manage_addRRDDataPoint(dpname)
            dp.rrdtype = 'GAUGE'
            dp.rrdmin = 0


    def zmanage_editProperties(self, REQUEST=None):
        '''validation, etc'''
        if REQUEST:
            self.addDataPoints()
            if not REQUEST.form.get('eventClass', None):
                REQUEST.form['eventClass'] = self.__class__.eventClass
        return BasicDataSource.BasicDataSource.zmanage_editProperties(self,
                REQUEST)

