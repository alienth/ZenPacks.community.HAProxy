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

from Products.ZenRelations.RelSchema import ToManyCont, ToOne

from .HAProxyComponent import HAProxyComponent


class HAProxyInstance(HAProxyComponent):
    meta_type = portal_type = "HAProxyInstance"

    _relations = HAProxyComponent._relations + (
        ('haproxy_host', ToOne(ToManyCont,
            'Products.ZenModel.Device.Device',
            'haproxy_instance',
            ),),
        ('haproxy_frontends', ToManyCont(ToOne,
            'ZenPacks.community.HAProxy.HAProxyFrontend.HAProxyFrontend',
            'haproxy_instance',
            ),),
        ('haproxy_backends', ToManyCont(ToOne,
            'ZenPacks.community.HAProxy.HAProxyBackend.HAProxyBackend',
            'haproxy_instance',
            ),),
        )

    def device(self):
        return self.haproxy_host()

