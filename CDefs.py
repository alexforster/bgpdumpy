# -*- coding: utf-8 -*-
########################################################################################################################
# Copyright © 2019 Alex Forster. All rights reserved.
# This software is licensed under the 3-Clause ("New") BSD license.
# See the LICENSE file for details.
########################################################################################################################

CTypes = '''
typedef void * caddr_t;

typedef unsigned char u_char;
typedef unsigned char u_int8_t;
typedef unsigned short u_int16_t;
typedef unsigned int u_int32_t;
typedef unsigned long time_t;

typedef unsigned int in_addr_t;

struct in_addr {
    in_addr_t s_addr;
};

struct in6_addr
{
    union
    {
        u_int8_t u6_addr8[16];
        u_int16_t u6_addr16[8];
        u_int32_t u6_addr32[4];
    }
    in6_u;
};

// cfile_tools.h //////////////////////////////////////////////////////////////

struct _CFRFILE {
    int format;       // 0 = not open, 1 = uncompressed, 2 = bzip2, 3 = gzip
    int eof;          // 0 = not eof
    int closed;       // indicates whether fclose has been called, 0 = not yet
    int error1;       // errors from the sytem, 0 = no error
    int error2;       // for error messages from the compressor
    FILE * data1;     // for filehandle of the system
    void * data2;     // addtional handle(s) of the compressor
    // compressor specific stuff
    int bz2_stream_end; // True when a bz2 stream has ended. Needed since
    // further reading returns error and not eof.
};

typedef struct _CFRFILE CFRFILE;

// bgpdump_attr.h /////////////////////////////////////////////////////////////

/* BGP Attribute flags. */
#define BGP_ATTR_FLAG_OPTIONAL  0x80	/* Attribute is optional. */
#define BGP_ATTR_FLAG_TRANS     0x40	/* Attribute is transitive. */
#define BGP_ATTR_FLAG_PARTIAL   0x20	/* Attribute is partial. */
#define BGP_ATTR_FLAG_EXTLEN    0x10	/* Extended length flag. */

/* BGP attribute type codes.  */
#define BGP_ATTR_ORIGIN                    1
#define BGP_ATTR_AS_PATH                   2
#define BGP_ATTR_NEXT_HOP                  3
#define BGP_ATTR_MULTI_EXIT_DISC           4
#define BGP_ATTR_LOCAL_PREF                5
#define BGP_ATTR_ATOMIC_AGGREGATE          6
#define BGP_ATTR_AGGREGATOR                7
#define BGP_ATTR_COMMUNITIES               8
#define BGP_ATTR_ORIGINATOR_ID             9
#define BGP_ATTR_CLUSTER_LIST             10
#define BGP_ATTR_DPA                      11
#define BGP_ATTR_ADVERTISER               12
#define BGP_ATTR_RCID_PATH                13
#define BGP_ATTR_MP_REACH_NLRI            14
#define BGP_ATTR_MP_UNREACH_NLRI          15
#define BGP_ATTR_EXT_COMMUNITIES          16
#define BGP_ATTR_NEW_AS_PATH              17
#define BGP_ATTR_NEW_AGGREGATOR           18
#define BGP_ATTR_LARGE_COMMUNITIES        32

/* Flag macro */
//#define ATTR_FLAG_BIT(X)  (1 << ((X) - 1))

/* BGP ASPATH attribute defines */
#define AS_HEADER_SIZE        2

#define AS_SET             1
#define AS_SEQUENCE        2
#define AS_CONFED_SEQUENCE 3
#define AS_CONFED_SET      4

#define AS_SEG_START 0
#define AS_SEG_END 1

#define ASPATH_STR_DEFAULT_LEN 32
//#define ASPATH_STR_ERROR       "! Error !"

/* BGP COMMUNITY attribute defines */

#define COMMUNITY_NO_EXPORT             0xFFFFFF01
#define COMMUNITY_NO_ADVERTISE          0xFFFFFF02
#define COMMUNITY_NO_EXPORT_SUBCONFED   0xFFFFFF03
#define COMMUNITY_LOCAL_AS              0xFFFFFF03

//#define com_nthval(X,n)  ((X)->val + (n))

/* MP-BGP address families */
//#ifdef BGPDUMP_HAVE_IPV6
#define AFI_IP 1
#define AFI_IP6 2
#define BGPDUMP_MAX_AFI 2
//#else
//#define AFI_IP 1
//#define BGPDUMP_MAX_AFI AFI_IP
//#endif

#define SAFI_UNICAST		1
#define SAFI_MULTICAST		2
#define SAFI_UNICAST_MULTICAST	3
#define BGPDUMP_MAX_SAFI 3

struct unknown_attr
{
    int	flag;
    int	type;
    int	len;
    u_char *raw;
};

typedef u_int32_t as_t;
typedef u_int32_t pathid_t;

typedef struct attr attributes_t;
struct attr
{
    /* Flag of attribute is set or not. */
    u_int32_t flag;

    /* Attributes. */
    int                   origin;
    struct in_addr 	nexthop;
    u_int32_t 		med;
    u_int32_t 		local_pref;
    as_t 			aggregator_as;
    struct in_addr 	aggregator_addr;
    u_int32_t 		weight;
    struct in_addr 	originator_id;
    struct cluster_list	*cluster;

    struct aspath 	*aspath;
    struct community 	*community;
    struct ecommunity 	*ecommunity;
    struct lcommunity   *lcommunity;
    struct transit 	*transit;

    /* libbgpdump additions */

    struct mp_info	*mp_info;
    u_int16_t		len;
    caddr_t		data;

    u_int16_t		unknown_num;
    struct unknown_attr	*unknown;

    /* ASN32 support */
    struct aspath 	*new_aspath;
    struct aspath 	*old_aspath;
    as_t			new_aggregator_as;
    as_t			old_aggregator_as;
    struct in_addr 	new_aggregator_addr;
    struct in_addr 	old_aggregator_addr;
};

struct community
{
    int 			size;
    u_int32_t 		*val;
    char			*str;
};

struct lcommunity
{
    int       size;
    u_int32_t *val;
    char      *str;
};

struct cluster_list
{
    int			length;
    struct in_addr 	*list;
};

struct transit
{
    int 			length;
    u_char 		*val;
};

struct aspath
{
    u_int8_t		asn_len;
    int 			length;
    int 			count;
    caddr_t 		data;
    char 			*str;
};

struct assegment
{
    u_char type;
    u_char length;
    char data[0];
};

struct mp_info {
    /* AFI and SAFI start from 1, so the arrays must be 1-based */
    struct mp_nlri	*withdraw[3][4];
    struct mp_nlri	*announce[3][4];
};

//#ifdef BGPDUMP_HAVE_IPV6
//#define MP_IPV6_ANNOUNCE(m) ((m)->announce[AFI_IP6][SAFI_UNICAST])
//#define MP_IPV6_WITHDRAW(m) ((m)->withdraw[AFI_IP6][SAFI_UNICAST])
//#endif

typedef union union_BGPDUMP_IP_ADDRESS {
    struct in_addr	v4_addr;
    struct in6_addr	v6_addr;
} BGPDUMP_IP_ADDRESS;

#define BGPDUMP_ADDRSTRLEN 46

//#define ASN16_LEN sizeof(u_int16_t)
//#define ASN32_LEN sizeof(u_int32_t)

#define AS_TRAN 23456

struct prefix {
    BGPDUMP_IP_ADDRESS	address;
    u_char		len;
    pathid_t    path_id;
};

#define MAX_PREFIXES 2050
struct mp_nlri {
    u_char		nexthop_len;

    BGPDUMP_IP_ADDRESS	nexthop;
    BGPDUMP_IP_ADDRESS 	nexthop_local;

    u_int16_t		prefix_count;
    struct prefix		nlri[MAX_PREFIXES];
};

// bgpdump_formats.h //////////////////////////////////////////////////////////

/* type and subtypes values */
/* RFC6396 */
#define BGPDUMP_TYPE_MRTD_BGP			5
#define BGPDUMP_SUBTYPE_MRTD_BGP_NULL		0
#define BGPDUMP_SUBTYPE_MRTD_BGP_UPDATE		1
#define BGPDUMP_SUBTYPE_MRTD_BGP_PREFUPDATE	2
#define BGPDUMP_SUBTYPE_MRTD_BGP_STATE_CHANGE	3
#define BGPDUMP_SUBTYPE_MRTD_BGP_SYNC		4
#define BGPDUMP_SUBTYPE_MRTD_BGP_OPEN		5
#define BGPDUMP_SUBTYPE_MRTD_BGP_NOTIFICATION	6
#define BGPDUMP_SUBTYPE_MRTD_BGP_KEEPALIVE	7
#define BGPDUMP_SUBTYPE_MRTD_BGP_ROUT_REFRESH	133

#define BGPDUMP_TYPE_MRTD_TABLE_DUMP				12
#define BGPDUMP_SUBTYPE_MRTD_TABLE_DUMP_AFI_IP			1
#define BGPDUMP_SUBTYPE_MRTD_TABLE_DUMP_AFI_IP6			2
#define BGPDUMP_SUBTYPE_MRTD_TABLE_DUMP_AFI_IP_32BIT_AS		3
#define BGPDUMP_SUBTYPE_MRTD_TABLE_DUMP_AFI_IP6_32BIT_AS	4

#define BGPDUMP_TYPE_TABLE_DUMP_V2                       13
#define BGPDUMP_SUBTYPE_TABLE_DUMP_V2_PEER_INDEX_TABLE    1
#define BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_IPV4_UNICAST    2
#define BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_IPV4_MULTICAST  3
#define BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_IPV6_UNICAST    4
#define BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_IPV6_MULTICAST  5
#define BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_GENERIC         6
#define BGPDUMP_PEERTYPE_TABLE_DUMP_V2_AFI_IP             0
#define BGPDUMP_PEERTYPE_TABLE_DUMP_V2_AFI_IP6            1
#define BGPDUMP_PEERTYPE_TABLE_DUMP_V2_AS2                0
#define BGPDUMP_PEERTYPE_TABLE_DUMP_V2_AS4                2
#define BGPDUMP_TYPE_TABLE_DUMP_V2_MAX_VIEWNAME_LEN     255

/* Zebra record types */
#define BGPDUMP_TYPE_ZEBRA_BGP			16 /* MSG_PROTOCOL_BGP4MP */
#define BGPDUMP_TYPE_ZEBRA_BGP_ET       17 /* MSG_PROTOCOL_BGP4MP_ET */
#define BGPDUMP_SUBTYPE_ZEBRA_BGP_STATE_CHANGE	0  /* BGP4MP_STATE_CHANGE */
#define BGPDUMP_SUBTYPE_ZEBRA_BGP_MESSAGE	1  /* BGP4MP_MESSAGE */
#define BGPDUMP_SUBTYPE_ZEBRA_BGP_ENTRY		2  /* BGP4MP_ENTRY */
#define BGPDUMP_SUBTYPE_ZEBRA_BGP_SNAPSHOT	3  /* BGP4MP_SNAPSHOT */
#define BGPDUMP_SUBTYPE_ZEBRA_BGP_MESSAGE_AS4	4  /* BGP4MP_MESSAGE_AS4 */
#define BGPDUMP_SUBTYPE_ZEBRA_BGP_STATE_CHANGE_AS4	5  /* BGP4MP_STATE_CHANGE_AS4 */
#define BGPDUMP_SUBTYPE_ZEBRA_BGP_MESSAGE_LOCAL	6  /* BGP4MP_MESSAGE_LOCAL */
#define BGPDUMP_SUBTYPE_ZEBRA_BGP_MESSAGE_AS4_LOCAL	7  /* BGP4MP_MESSAGE_AS4_LOCAL */

/* RFC8050 add-path extensions */
#define BGPDUMP_SUBTYPE_ZEBRA_BGP_MESSAGE_ADDPATH            8   /* BGP4MP_MESSAGE_ADDPATH */
#define BGPDUMP_SUBTYPE_ZEBRA_BGP_MESSAGE_AS4_ADDPATH        9   /* BGP4MP_MESSAGE_AS4_ADDPATH */
#define BGPDUMP_SUBTYPE_ZEBRA_BGP_MESSAGE_LOCAL_ADDPATH      10  /* BGP4MP_MESSAGE_LOCAL_ADDPATH */
#define BGPDUMP_SUBTYPE_ZEBRA_BGP_MESSAGE_AS4_LOCAL_ADDPATH  11  /* BGP4MP_MESSAGE_AS4_LOCAL */
#define BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_IPV4_UNICAST_ADDPATH    8    /* RIB_IPV4_UNICAST_ADDPATH */
#define BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_IPV4_MULTICAST_ADDPATH  9    /* RIB_IPV4_MULTICAST_ADDPATH */
#define BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_IPV6_UNICAST_ADDPATH    10   /* RIB_IPV6_UNICAST_ADDPATH */
#define BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_IPV6_MULTICAST_ADDPATH  11   /* RIB_IPV6_MULTICAST_ADDPATH */
#define BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_GENERIC_ADDPATH         12   /* RIB_GENERIC_ADDPATH */

/* BGP state - defined in RFC1771 */
#define BGP_STATE_IDLE		1
#define BGP_STATE_CONNECT	2
#define BGP_STATE_ACTIVE	3
#define BGP_STATE_OPENSENT	4
#define BGP_STATE_OPENCONFIRM	5
#define BGP_STATE_ESTABLISHED	6

/* BGP message types */
#define	BGP_MSG_OPEN		           1
#define	BGP_MSG_UPDATE		           2
#define	BGP_MSG_NOTIFY		           3
#define	BGP_MSG_KEEPALIVE	           4
#define BGP_MSG_ROUTE_REFRESH_01           5
#define BGP_MSG_ROUTE_REFRESH	         128

typedef struct struct_BGPDUMP_MRTD_TABLE_DUMP {
    u_int16_t		view;
    u_int16_t		sequence;
    BGPDUMP_IP_ADDRESS	prefix;
    u_char		mask;
    u_char		status;
    time_t		uptime;
    BGPDUMP_IP_ADDRESS	peer_ip;
    as_t		peer_as;
    u_int16_t		attr_len;
} BGPDUMP_MRTD_TABLE_DUMP;


typedef struct struct_BGPDUMP_TABLE_DUMP_V2_PEER_INDEX_TABLE_ENTRY {
    u_char              afi;
    BGPDUMP_IP_ADDRESS  peer_ip;
    struct in_addr      peer_bgp_id;
    as_t                peer_as;
} BGPDUMP_TABLE_DUMP_V2_PEER_INDEX_TABLE_ENTRY;

typedef struct struct_BGPDUMP_TABLE_DUMP_V2_PEER_INDEX_TABLE {
    struct in_addr      local_bgp_id;
    char                view_name[BGPDUMP_TYPE_TABLE_DUMP_V2_MAX_VIEWNAME_LEN];
    uint16_t            peer_count;
    BGPDUMP_TABLE_DUMP_V2_PEER_INDEX_TABLE_ENTRY  *entries;
} BGPDUMP_TABLE_DUMP_V2_PEER_INDEX_TABLE;

typedef struct struct_BGPDUMP_TABLE_DUMP_V2_ROUTE_ENTRY {
    uint16_t            peer_index;
    uint32_t            originated_time;
    pathid_t            path_id;
    BGPDUMP_TABLE_DUMP_V2_PEER_INDEX_TABLE_ENTRY *peer;
    attributes_t        *attr;
} BGPDUMP_TABLE_DUMP_V2_ROUTE_ENTRY;

typedef struct struct_BGPDUMP_TABLE_DUMP_V2_PREFIX {
    uint32_t            seq;
    uint16_t            afi;
    uint8_t             safi;
    u_char              prefix_length;
    BGPDUMP_IP_ADDRESS  prefix;
    uint16_t            entry_count;
    BGPDUMP_TABLE_DUMP_V2_ROUTE_ENTRY *entries;
} BGPDUMP_TABLE_DUMP_V2_PREFIX;

/* For Zebra BGP4MP_STATE_CHANGE */
typedef struct struct_BGPDUMP_ZEBRA_STATE_CHANGE {
    as_t		source_as;
    as_t		destination_as;
    u_int16_t		interface_index;
    u_int16_t		address_family;
    BGPDUMP_IP_ADDRESS	source_ip;
    BGPDUMP_IP_ADDRESS	destination_ip;
    u_int16_t		old_state;
    u_int16_t		new_state;
} BGPDUMP_ZEBRA_STATE_CHANGE;

struct zebra_incomplete {
    u_int16_t afi;
    u_int8_t orig_len;
    struct prefix prefix;
};

/* For Zebra BGP4MP_MESSAGE */
typedef struct struct_BGPDUMP_ZEBRA_MESSAGE {
    /* Zebra header */
    as_t		source_as;
    as_t		destination_as;
    u_int16_t		interface_index;
    u_int16_t		address_family;
    BGPDUMP_IP_ADDRESS	source_ip;
    BGPDUMP_IP_ADDRESS	destination_ip;

    /* BGP packet header fields */
    u_int16_t		size;
    u_char		type;

    /* For OPEN packets */
    u_char	version;
    as_t	my_as;
    u_int16_t	hold_time;
    struct	in_addr bgp_id;
    u_char	opt_len;
    u_char	*opt_data;

    /* For UPDATE packets */
    u_int16_t		withdraw_count;
    u_int16_t		announce_count;
    struct prefix	withdraw[MAX_PREFIXES];
    struct prefix	announce[MAX_PREFIXES];

    /* For corrupt update dumps */
    u_int16_t cut_bytes;
    struct zebra_incomplete incomplete;

    /* For NOTIFY packets */
    u_char error_code;
    u_char sub_error_code;
    u_int16_t notify_len;
    u_char *notify_data;

} BGPDUMP_ZEBRA_MESSAGE;

/* For Zebra BGP4MP_ENTRY */
typedef struct struct_BGPDUMP_ZEBRA_ENTRY {
    u_int16_t	view;
    u_int16_t	status;
    time_t	time_last_change;
    u_int16_t	address_family;
    u_char	SAFI;
    u_char	next_hop_len;
    u_char	prefix_length;
    u_char	*address_prefix;
    u_int16_t	empty;
    u_char	*bgp_atribute;
} BGPDUMP_ZEBRA_ENTRY;

/* For Zebra BGP4MP_SNAPSHOT */
typedef struct struct_BGPDUMP_ZEBRA_SNAPSHOT {
    u_int16_t	view;
    u_int16_t	file;
} BGPDUMP_ZEBRA_SNAPSHOT;

typedef struct struct_BGPDUMP_MRTD_MESSAGE {
    u_int16_t		source_as;
    struct in_addr	source_ip;
    u_int16_t		destination_as;
    struct in_addr	destination_ip;

    u_int16_t		withdraw_count;
    u_int16_t		announce_count;
    struct prefix	withdraw[MAX_PREFIXES];
    struct prefix	announce[MAX_PREFIXES];

    /* For corrupt update dumps */
    struct zebra_incomplete incomplete;
} BGPDUMP_MRTD_MESSAGE;

typedef struct struct_BGPDUMP_MRTD_STATE_CHANGE {
    u_int16_t           destination_as;
    struct in_addr      destination_ip;
    u_int16_t           old_state;
    u_int16_t           new_state;
} BGPDUMP_MRTD_STATE_CHANGE;

typedef union union_BGPDUMP_BODY {
    BGPDUMP_MRTD_MESSAGE		mrtd_message;
    BGPDUMP_MRTD_STATE_CHANGE       mrtd_state_change;
    BGPDUMP_MRTD_TABLE_DUMP		mrtd_table_dump;
    BGPDUMP_TABLE_DUMP_V2_PEER_INDEX_TABLE		mrtd_table_dump_v2_peer_table;
    BGPDUMP_TABLE_DUMP_V2_PREFIX		mrtd_table_dump_v2_prefix;
    BGPDUMP_ZEBRA_STATE_CHANGE	zebra_state_change;
    BGPDUMP_ZEBRA_MESSAGE		zebra_message;
    BGPDUMP_ZEBRA_ENTRY		zebra_entry;
    BGPDUMP_ZEBRA_SNAPSHOT		zebra_snapshot;
} BGPDUMP_BODY;

/* The MRT header. Common to all records. */
typedef struct struct_BGPDUMP_ENTRY {
    time_t		time;
    long		ms;
    u_int16_t		type;
    u_int16_t		subtype;
    u_int32_t		length;
    attributes_t       *attr;
    BGPDUMP_BODY 	body;
} BGPDUMP_ENTRY;

// bgpdump_lib.h //////////////////////////////////////////////////////////////

#define BGPDUMP_MAX_FILE_LEN	1024
#define BGPDUMP_MAX_AS_PATH_LEN	2000

// if you include cfile_tools.h, include it first
//#ifndef _CFILE_TOOLS_DEFINES
//typedef struct _CFRFILE CFRFILE;
//#endif

typedef struct struct_BGPDUMP {
    CFRFILE	*f;
    int		f_type;
    int		eof;
    char	filename[BGPDUMP_MAX_FILE_LEN];
    int		parsed;
    int		parsed_ok;
    BGPDUMP_TABLE_DUMP_V2_PEER_INDEX_TABLE *table_dump_v2_peer_index_table;
} BGPDUMP;

/* prototypes */

BGPDUMP *bgpdump_open_dump(const char *filename);
void	bgpdump_close_dump(BGPDUMP *dump);
BGPDUMP_ENTRY*	bgpdump_read_next(BGPDUMP *dump);
void	bgpdump_free_mem(BGPDUMP_ENTRY *entry);
char    *bgpdump_version(void);
int     is_addpath(BGPDUMP_ENTRY *entry);
'''


class CConst:
    # type and subtypes values - defined in RFC6396
    BGPDUMP_TYPE_MRTD_BGP = 5
    BGPDUMP_SUBTYPE_MRTD_BGP_NULL = 0
    BGPDUMP_SUBTYPE_MRTD_BGP_UPDATE = 1
    BGPDUMP_SUBTYPE_MRTD_BGP_PREFUPDATE = 2
    BGPDUMP_SUBTYPE_MRTD_BGP_STATE_CHANGE = 3
    BGPDUMP_SUBTYPE_MRTD_BGP_SYNC = 4
    BGPDUMP_SUBTYPE_MRTD_BGP_OPEN = 5
    BGPDUMP_SUBTYPE_MRTD_BGP_NOTIFICATION = 6
    BGPDUMP_SUBTYPE_MRTD_BGP_KEEPALIVE = 7
    BGPDUMP_SUBTYPE_MRTD_BGP_ROUT_REFRESH = 133
    BGPDUMP_TYPE_MRTD_TABLE_DUMP = 12
    BGPDUMP_SUBTYPE_MRTD_TABLE_DUMP_AFI_IP = 1
    BGPDUMP_SUBTYPE_MRTD_TABLE_DUMP_AFI_IP6 = 2
    BGPDUMP_SUBTYPE_MRTD_TABLE_DUMP_AFI_IP_32BIT_AS = 3
    BGPDUMP_SUBTYPE_MRTD_TABLE_DUMP_AFI_IP6_32BIT_AS = 4
    BGPDUMP_TYPE_TABLE_DUMP_V2 = 13
    BGPDUMP_SUBTYPE_TABLE_DUMP_V2_PEER_INDEX_TABLE = 1
    BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_IPV4_UNICAST = 2
    BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_IPV4_MULTICAST = 3
    BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_IPV6_UNICAST = 4
    BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_IPV6_MULTICAST = 5
    BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_GENERIC = 6
    BGPDUMP_PEERTYPE_TABLE_DUMP_V2_AFI_IP = 0
    BGPDUMP_PEERTYPE_TABLE_DUMP_V2_AFI_IP6 = 1
    BGPDUMP_PEERTYPE_TABLE_DUMP_V2_AS2 = 0
    BGPDUMP_PEERTYPE_TABLE_DUMP_V2_AS4 = 2
    BGPDUMP_TYPE_TABLE_DUMP_V2_MAX_VIEWNAME_LEN = 255

    # Zebra record types
    BGPDUMP_TYPE_ZEBRA_BGP = 16
    BGPDUMP_TYPE_ZEBRA_BGP_ET = 17
    BGPDUMP_SUBTYPE_ZEBRA_BGP_STATE_CHANGE = 0
    BGPDUMP_SUBTYPE_ZEBRA_BGP_MESSAGE = 1
    BGPDUMP_SUBTYPE_ZEBRA_BGP_ENTRY = 2
    BGPDUMP_SUBTYPE_ZEBRA_BGP_SNAPSHOT = 3
    BGPDUMP_SUBTYPE_ZEBRA_BGP_MESSAGE_AS4 = 4
    BGPDUMP_SUBTYPE_ZEBRA_BGP_STATE_CHANGE_AS4 = 5
    BGPDUMP_SUBTYPE_ZEBRA_BGP_MESSAGE_LOCAL = 6
    BGPDUMP_SUBTYPE_ZEBRA_BGP_MESSAGE_AS4_LOCAL = 7
    BGPDUMP_SUBTYPE_ZEBRA_BGP_MESSAGE_ADDPATH = 8
    BGPDUMP_SUBTYPE_ZEBRA_BGP_MESSAGE_AS4_ADDPATH = 9
    BGPDUMP_SUBTYPE_ZEBRA_BGP_MESSAGE_LOCAL_ADDPATH = 10
    BGPDUMP_SUBTYPE_ZEBRA_BGP_MESSAGE_AS4_LOCAL_ADDPATH = 11
    BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_IPV4_UNICAST_ADDPATH = 8
    BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_IPV4_MULTICAST_ADDPATH = 9
    BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_IPV6_UNICAST_ADDPATH = 10
    BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_IPV6_MULTICAST_ADDPATH = 11
    BGPDUMP_SUBTYPE_TABLE_DUMP_V2_RIB_GENERIC_ADDPATH = 12

    # BGP state - defined in RFC1771
    BGP_STATE_IDLE = 1
    BGP_STATE_CONNECT = 2
    BGP_STATE_ACTIVE = 3
    BGP_STATE_OPENSENT = 4
    BGP_STATE_OPENCONFIRM = 5
    BGP_STATE_ESTABLISHED = 6

    # BGP message types */
    BGP_MSG_OPEN = 1
    BGP_MSG_UPDATE = 2
    BGP_MSG_NOTIFY = 3
    BGP_MSG_KEEPALIVE = 4
    BGP_MSG_ROUTE_REFRESH_01 = 5
    BGP_MSG_ROUTE_REFRESH = 128

    # BGP Attribute flags
    BGP_ATTR_FLAG_OPTIONAL = 0x80
    BGP_ATTR_FLAG_TRANS = 0x40
    BGP_ATTR_FLAG_PARTIAL = 0x20
    BGP_ATTR_FLAG_EXTLEN = 0x10

    # BGP attribute type codes.
    BGP_ATTR_ORIGIN = 1
    BGP_ATTR_AS_PATH = 2
    BGP_ATTR_NEXT_HOP = 3
    BGP_ATTR_MULTI_EXIT_DISC = 4
    BGP_ATTR_LOCAL_PREF = 5
    BGP_ATTR_ATOMIC_AGGREGATE = 6
    BGP_ATTR_AGGREGATOR = 7
    BGP_ATTR_COMMUNITIES = 8
    BGP_ATTR_ORIGINATOR_ID = 9
    BGP_ATTR_CLUSTER_LIST = 10
    BGP_ATTR_DPA = 11
    BGP_ATTR_ADVERTISER = 12
    BGP_ATTR_RCID_PATH = 13
    BGP_ATTR_MP_REACH_NLRI = 14
    BGP_ATTR_MP_UNREACH_NLRI = 15
    BGP_ATTR_EXT_COMMUNITIES = 16
    BGP_ATTR_NEW_AS_PATH = 17
    BGP_ATTR_NEW_AGGREGATOR = 18
    BGP_ATTR_LARGE_COMMUNITIES = 32

    # Flag macro
    ATTR_FLAG_BIT = lambda X: (1 << ((X) - 1))

    # BGP ASPATH attribute defines
    AS_HEADER_SIZE = 2
    AS_SET = 1
    AS_SEQUENCE = 2
    AS_CONFED_SEQUENCE = 3
    AS_CONFED_SET = 4
    AS_SEG_START = 0
    AS_SEG_END = 1

    # BGP COMMUNITY attribute defines
    COMMUNITY_NO_EXPORT = 0xFFFFFF01
    COMMUNITY_NO_ADVERTISE = 0xFFFFFF02
    COMMUNITY_NO_EXPORT_SUBCONFED = 0xFFFFFF03
    COMMUNITY_LOCAL_AS = 0xFFFFFF03

    COM_NTHVAL = lambda X, n: (X.val + (n))

    # MP-BGP address families
    AFI_IP = 1
    AFI_IP6 = 2

    SAFI_UNICAST = 1
    SAFI_MULTICAST = 2
    SAFI_UNICAST_MULTICAST = 3

    AS_TRAN = 23456
    MAX_PREFIXES = 2050
    BGPDUMP_MAX_FILE_LEN = 1024
    BGPDUMP_MAX_AS_PATH_LEN = 2000
    BGPDUMP_ADDRSTRLEN = 46
