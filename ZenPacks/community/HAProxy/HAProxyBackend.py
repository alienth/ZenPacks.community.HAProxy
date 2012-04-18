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


class HAProxyBackend(HAProxyComponent):
    meta_type = portal_type = "HAProxyBackend"

    # Modeled attributes.
    #durable = None
    #auto_delete = None
    #arguments = None

    # Managed attributes.
    threshold_session_rate = None
    threshold_session_active = None

    _properties = HAProxyComponent._properties + (
        {'id': 'threshold_session_rate', 'type': 'int', 'mode': 'w'},
        {'id': 'threshold_session_active', 'type': 'int', 'mode': 'w'},
        )

    _relations = HAProxyComponent._relations + (
        ('haproxy_instance', ToOne(ToManyCont,
            'ZenPacks.community.HAProxy.HAProxyInstance.HAProxyInstance',
            'haproxy_frontends',
            ),),
        )

    def device(self):
        return self.haproxy_instance().device()

