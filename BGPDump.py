# -*- coding: utf-8 -*-
########################################################################################################################
# Copyright © 2019 Alex Forster. All rights reserved.
# This software is licensed under the 3-Clause ("New") BSD license.
# See the LICENSE file for details.
########################################################################################################################

import os
from datetime import datetime
from socket import inet_ntop, AF_INET, AF_INET6

from cffi import FFI
from pkg_resources import resource_filename

from .CDefs import CTypes, CConst


class BGPAttributes:

    def __init__(self, bgp, attributes):

        self.bgp = bgp
        self.attributes = attributes
        self._cluster = None

    @property
    def flag(self):

        return self.attributes.flag

    @property
    def origin(self):

        return self.attributes.origin

    @property
    def nexthop(self):

        return inet_ntop(AF_INET, self.bgp.ffi.buffer(self.bgp.ffi.addressof(self.attributes.nexthop))[:])

    @property
    def med(self):

        return self.attributes.med

    @property
    def localPref(self):

        return self.attributes.local_pref

    @property
    def aggregatorAS(self):

        return self.attributes.aggregator_as

    @property
    def aggregatorAddr(self):

        return inet_ntop(AF_INET, self.bgp.ffi.buffer(self.bgp.ffi.addressof(self.attributes.aggregator_addr))[:])

    @property
    def weight(self):

        return self.attributes.weight

    @property
    def originatorID(self):

        return inet_ntop(AF_INET, self.bgp.ffi.buffer(self.bgp.ffi.addressof(self.attributes.originator_id))[:])

    @property
    def cluster(self):

        if self._cluster is not None:
            return self._cluster
        self._cluster = []
        for i in range(0, self.attributes.cluster.length):
            self._cluster.append(
                inet_ntop(AF_INET, self.bgp.ffi.buffer(self.bgp.ffi.addressof(self.attributes.cluster.list[i]))[:]))
        return self._cluster

    @property
    def asPath(self):

        return self.bgp.ffi.string(self.attributes.aspath.str).decode() if self.attributes.aspath != self.bgp.ffi.NULL else None

    @property
    def community(self):

        return self.bgp.ffi.string(self.attributes.community.str).decode() if self.attributes.community != self.bgp.ffi.NULL else None

    @property
    def ecommunity(self):

        return self.bgp.ffi.string(self.attributes.ecommunity.str).decode() if self.attributes.ecommunity != self.bgp.ffi.NULL else None

    @property
    def transit(self):

        return self.attributes.transit

    @property
    def newASPath(self):

        return self.bgp.ffi.string(self.attributes.new_aspath.str).decode() if self.attributes.new_aspath != self.bgp.ffi.NULL else None

    @property
    def oldASPath(self):

        return self.bgp.ffi.string(self.attributes.old_aspath.str).decode() if self.attributes.old_aspath != self.bgp.ffi.NULL else None

    @property
    def newAggregatorAS(self):

        return self.attributes.new_aggregator_as

    @property
    def oldAggregatorAS(self):

        return self.attributes.old_aggregator_as

    @property
    def newAggregatorAddr(self):

        return self.attributes.new_aggregator_addr

    @property
    def oldAggregatorAddr(self):

        return self.attributes.old_aggregator_addr


class TableDumpV1:

    def __init__(self, bgp, subtype, body):

        self.bgp = bgp
        self.subtype = subtype
        self.body = body

    @property
    def view(self):

        return self.body.view

    @property
    def sequence(self):

        return self.body.sequence

    @property
    def prefix(self):

        if self.subtype == CConst.BGPDUMP_SUBTYPE_MRTD_TABLE_DUMP_AFI_IP \
                or self.subtype == CConst.BGPDUMP_SUBTYPE_MRTD_TABLE_DUMP_AFI_IP_32BIT_AS:
            return inet_ntop(AF_INET, self.bgp.ffi.buffer(self.bgp.ffi.addressof(self.body.prefix.v4_addr))[:])

        if self.subtype == CConst.BGPDUMP_SUBTYPE_MRTD_TABLE_DUMP_AFI_IP6 \
                or self.subtype == CConst.BGPDUMP_SUBTYPE_MRTD_TABLE_DUMP_AFI_IP6_32BIT_AS:
            return inet_ntop(AF_INET6, self.bgp.ffi.buffer(self.bgp.ffi.addressof(self.body.prefix.v6_addr))[:])

    @property
    def mask(self):

        return self.body.mask

    @property
    def status(self):

        return self.body.status

    @property
    def uptime(self):

        return datetime.fromtimestamp(self.body.uptime)

    @property
    def peerIP(self):

        if self.subtype == CConst.BGPDUMP_SUBTYPE_MRTD_TABLE_DUMP_AFI_IP \
                or self.subtype == CConst.BGPDUMP_SUBTYPE_MRTD_TABLE_DUMP_AFI_IP_32BIT_AS:
            return inet_ntop(AF_INET, self.bgp.ffi.buffer(self.bgp.ffi.addressof(self.body.prefix.v4_addr))[:])

        if self.subtype == CConst.BGPDUMP_SUBTYPE_MRTD_TABLE_DUMP_AFI_IP6 \
                or self.subtype == CConst.BGPDUMP_SUBTYPE_MRTD_TABLE_DUMP_AFI_IP6_32BIT_AS:
            return inet_ntop(AF_INET6, self.bgp.ffi.buffer(self.bgp.ffi.addressof(self.body.prefix.v6_addr))[:])

    @property
    def peerAS(self):

        return self.body.peer_as

    @property
    def attrLength(self):

        return self.body.attr_len


class TableDumpV2PeerIndexTableEntry:

    def __init__(self, bgp, entry):
        self.bgp = bgp
        self.entry = entry

    @property
    def afi(self):
        return AF_INET if self.entry.afi == CConst.AFI_IP else AF_INET6 if self.entry.afi == CConst.AFI_IP6 else None

    @property
    def peerIP(self):

        if self.afi == AF_INET:
            return inet_ntop(AF_INET, self.bgp.ffi.buffer(self.bgp.ffi.addressof(self.entry.peer_ip.v4_addr))[:])

        if self.afi == AF_INET6:
            return inet_ntop(AF_INET6, self.bgp.ffi.buffer(self.bgp.ffi.addressof(self.entry.peer_ip.v6_addr))[:])

    @property
    def peerRouterID(self):
        return inet_ntop(AF_INET, self.bgp.ffi.buffer(self.bgp.ffi.addressof(self.entry.peer_bgp_id))[:])

    @property
    def peerAS(self):
        return self.entry.peer_as


class TableDumpV2RouteEntry:

    def __init__(self, bgp, entry):
        self.bgp = bgp
        self.entry = entry
        self._attr = None

    @property
    def peerIndex(self):
        return self.entry.peer_index

    @property
    def originatedTime(self):
        return datetime.fromtimestamp(self.entry.originated_time)

    @property
    def peer(self):
        return TableDumpV2PeerIndexTableEntry(self.bgp, self.entry.peer)

    @property
    def attr(self):
        if self._attr is not None:
            return self._attr
        self._attr = BGPAttributes(self.bgp, self.entry.attr) if self.entry.attr != self.bgp.ffi.NULL else None
        return self._attr


class TableDumpV2:

    def __init__(self, bgp, subtype, body):

        self.bgp = bgp
        self.subtype = subtype
        self.body = body
        self._routeEntries = None

    @property
    def seq(self):

        return self.body.seq

    @property
    def afi(self):

        return AF_INET if self.body.afi == CConst.AFI_IP else AF_INET6 if self.body.afi == CConst.AFI_IP6 else None

    @property
    def safi(self):

        return AF_INET if self.body.safi == CConst.AFI_IP else AF_INET6 if self.body.safi == CConst.AFI_IP6 else None

    @property
    def prefixLength(self):

        return self.body.prefix_length

    @property
    def prefix(self):

        if self.afi == AF_INET:
            return inet_ntop(AF_INET, self.bgp.ffi.buffer(self.bgp.ffi.addressof(self.body.prefix.v4_addr))[:])

        if self.afi == AF_INET6:
            return inet_ntop(AF_INET6, self.bgp.ffi.buffer(self.bgp.ffi.addressof(self.body.prefix.v6_addr))[:])

    @property
    def routeEntries(self):

        if self._routeEntries is not None:
            return self._routeEntries
        self._routeEntries = []
        for i in range(0, self.body.entry_count):
            self._routeEntries.append(TableDumpV2RouteEntry(self.bgp, self.body.entries[i]))
        return self._routeEntries


class BGPEntry:

    def __init__(self, bgp, entry):

        self.bgp = bgp
        self.entry = entry
        self._body = None
        self._attr = None

    @property
    def time(self):

        return datetime.fromtimestamp(self.entry.time)

    @property
    def length(self):

        return self.entry.length

    @property
    def attr(self):

        if self._attr is not None:
            return self._attr
        self._attr = BGPAttributes(self.bgp, self.entry.attr) if self.entry.attr != self.bgp.ffi.NULL else None
        return self._attr

    @property
    def body(self):

        if self._body is not None:
            return self._body

        if self.entry.type == CConst.BGPDUMP_TYPE_MRTD_TABLE_DUMP:
            self._body = TableDumpV1(self.bgp, self.entry.subtype, self.entry.body.mrtd_table_dump)

        if self.entry.type == CConst.BGPDUMP_TYPE_TABLE_DUMP_V2:
            if self.entry.subtype == CConst.BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_IPV4_UNICAST \
                    or self.entry.subtype == CConst.BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_IPV6_UNICAST:
                self._body = TableDumpV2(self.bgp, self.entry.subtype, self.entry.body.mrtd_table_dump_v2_prefix)

        return self._body


class BGPDump:

    def __init__(self, filename, libbgpdump_path=None):

        self.filename = filename
        self.libbgpdump_path = libbgpdump_path
        self.ffi = None
        self.libc = None
        self.libbgpdump = None
        self.handle = None

    def __enter__(self):

        self.ffi = FFI()

        libdir = resource_filename('bgpdumpy', 'lib') or ''

        self.libc = self.ffi.dlopen(None)
        if self.libbgpdump_path is not None:
            self.libbgpdump = self.ffi.dlopen(os.path.abspath(os.path.expanduser(self.libbgpdump_path)))
        else:
            self.libbgpdump = self.ffi.dlopen(os.path.join(libdir, 'libbgpdump.so'))

        self.ffi.cdef(CTypes)

        self.handle = self.libbgpdump.bgpdump_open_dump(str(self.filename).encode())

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.libbgpdump.bgpdump_close_dump(self.handle)

        del self.libbgpdump
        self.libbgpdump = None
        del self.libc
        self.libc = None
        del self.ffi
        self.ffi = None

    def __iter__(self):

        while True:

            if self.handle.eof == 1:
                break

            currentEntry = self.libbgpdump.bgpdump_read_next(self.handle)

            if currentEntry == self.ffi.NULL:
                continue  # sometimes we get NULL back for no apparent reason

            try:
                yield BGPEntry(self, currentEntry)
            finally:
                self.libbgpdump.bgpdump_free_mem(currentEntry)

    @property
    def version(self):

        return self.ffi.string(self.libbgpdump.bgpdump_version()).decode()
