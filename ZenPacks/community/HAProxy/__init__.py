###########################################################################
#
# Copyright (C) 2012, Jason Harvey
# Based on code by Zenoss, Inc. -- Copyright (C) 2011, Zenoss Inc.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 or (at your
# option) any later version as published by the Free Software Foundation.
#
###########################################################################

"""
Custom ZenPack initialization code. All code defined in this module will be
executed at startup time in all Zope clients.
"""

import logging
log = logging.getLogger('zen.HAProxy')

import Globals

from Products.ZenEvents.EventManagerBase import EventManagerBase
from Products.ZenModel.Device import Device
from Products.ZenModel.ZenPack import ZenPack as ZenPackBase
from Products.ZenRelations.RelSchema import ToManyCont, ToOne
from Products.ZenUtils.Utils import unused

unused(Globals)


ZENPACK_NAME = 'ZenPacks.community.HAProxy'

# Define new device relations.
NEW_DEVICE_RELATIONS = (
    ('haproxy_instances', 'HAProxyInstance'),
    )

# Add new relationships to Device if they don't already exist.
for relname, modname in NEW_DEVICE_RELATIONS:
    if relname not in (x[0] for x in Device._relations):
        Device._relations += (
            (relname, ToManyCont(ToOne,
                '.'.join((ZENPACK_NAME, modname)), 'haproxy_host')),
            )



