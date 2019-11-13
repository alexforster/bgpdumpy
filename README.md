## bgpdumpy

### Overview

`bgpdumpy` is a [libbgpdump](https://bitbucket.org/ripencc/bgpdump) Python CFFI wrapper for analyzing MRT and MRTv2 BGP table dump files.

### Build Requirements

#### Debian/Ubuntu

 * `ca-certificates`
 * `gcc`
 * `make`
 * `autoconf`
 * `python-setuptools`
 * `python-dev`
 * `libbz2-dev`
 * `zlib1g-dev`
 * `libffi-dev`

### Example

```python
from bgpdumpy import BGPDump, TableDumpV2

with BGPDump('latest-bview.gz') as bgp:
    for entry in bgp:

        # entry.body can be either be TableDumpV1 or TableDumpV2
        if not isinstance(entry.body, TableDumpV2):
            continue  # I expect an MRT v2 table dump file

        # get a string representation of this prefix
        prefix = '%s/%d' % (entry.body.prefix, entry.body.prefixLength)

        # get a list of each unique originating ASN for this prefix
        originatingASs = set([
            route.attr.asPath.split()[-1]
            for route
            in entry.body.routeEntries])

        # just print it for demonstration purposes
        print('%s -> %s' % (prefix, '/'.join(originatingASs)))

# 1.0.0.0/24 -> 15169
# 1.0.4.0/24 -> 56203
# 1.0.5.0/24 -> 56203
# 1.0.6.0/24 -> 56203
# 1.0.7.0/24 -> 38803
# 1.0.38.0/24 -> 24155
# 1.0.64.0/18 -> 18144
# 1.0.128.0/17 -> 9737
# 1.0.128.0/18 -> 9737
# 1.0.128.0/19 -> 9737
# ...
# 2001::/32 -> 6939
# 2001:4:112::/48 -> 112
# 2001:200::/32 -> 2500
# 2001:200:900::/40 -> 7660
# 2001:200:c000::/35 -> 23634
```
