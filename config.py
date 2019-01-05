# -*- coding: utf-8 -*-

import paramiko
from enum import Enum


# 通用的cluster private key
common_cluster_pkey = paramiko.RSAKey.from_private_key_file('/Users/chenxiaolu/cloud2go/key/test')

# 通用的infra private key
common_infra_pkey = paramiko.RSAKey.from_private_key_file('/Users/chenxiaolu/cloud2go/key/test1')

# host list, 格式为IP、port、username、password（没有时填None）、private_key
host_lists = [
                ('123.58.33.18', 1314, 'root', None, common_cluster_pkey),
                ('59.110.170.216', 22, 'root', None, common_infra_pkey),
                ('39.107.106.224', 822, 'root', None, common_infra_pkey),
                ('59.110.174.190', 22, 'root', None, common_infra_pkey),
                ('106.75.145.94', 22, 'root', None, common_cluster_pkey),
                ('106.75.145.94', 1301, 'root', None, common_cluster_pkey),
                ('106.75.145.94', 1302, 'root', None, common_cluster_pkey),
                ('106.75.145.94', 1303, 'root', None, common_cluster_pkey),
                ('106.75.145.94', 1304, 'root', None, common_cluster_pkey),
                ('106.75.145.94', 1305, 'root', None, common_cluster_pkey),
                ('106.75.145.94', 1306, 'root', None, common_cluster_pkey),
                ('106.75.145.94', 1307, 'root', None, common_cluster_pkey),
                ('106.75.145.94', 1308, 'root', None, common_cluster_pkey),
                ('106.75.145.94', 1309, 'root', None, common_cluster_pkey),
                ('106.75.145.94', 1310, 'root', None, common_cluster_pkey),
                ('123.58.33.18', 22, 'root', None, common_cluster_pkey),
                ('123.58.33.18', 1300, 'root', None, common_cluster_pkey),
                ('123.58.33.18', 1301, 'root', None, common_cluster_pkey),
                ('123.58.33.18', 1302, 'root', None, common_cluster_pkey),
                ('123.58.33.18', 1303, 'root', None, common_cluster_pkey),
                ('123.58.33.18', 1304, 'root', None, common_cluster_pkey),
                ('123.58.33.18', 1305, 'root', None, common_cluster_pkey),
                ('123.58.33.18', 1306, 'root', None, common_cluster_pkey),
                ('123.58.33.18', 1307, 'root', None, common_cluster_pkey),
                # ('123.58.33.18', 1308, 'root', None, common_cluster_pkey),
                ('123.58.33.18', 1309, 'root', None, common_cluster_pkey),
                ('123.58.33.18', 1310, 'root', None, common_cluster_pkey),
                ('123.58.33.18', 1311, 'root', None, common_cluster_pkey),
                ('123.58.33.18', 1312, 'root', None, common_cluster_pkey),
                ('123.58.33.18', 1313, 'root', None, common_cluster_pkey),
                ('123.58.33.18', 1314, 'root', None, common_cluster_pkey)
]

# 告警钉钉通知机器人webhook列表
notify_dingding_webhooks = ['https://oapi.dingtalk.com/robot/send?access_token=bbd9fe6590f980153c9f929e66c2037fe42cc8b2b46c4323c12273451c96b015',

                            ]


class Severity(Enum):
    WARNING = 1
    CRITICAL = 2


# 告警策略, frequency是监控频率，单位是分钟。times是监控次数。threshold是告警阈值，整型。
CPU_alarm_policy = {'frequency': 1, "times": 5, 'threshold': 85, 'severity': Severity.WARNING}
mem_alarm_policy = {'frequency': 1, "times": 5, 'threshold': 85, 'severity': Severity.WARNING}
CPU15_alarm_policy = {'frequency': 1, "times": 5, 'threshold': 2, 'severity': Severity.WARNING}
disk_alarm_policy = {'frequency': 1, "times": 5, 'threshold': 90, 'severity': Severity.WARNING}


health_check_services = [('59.110.170.216', 8003, 'factory服务'),

                         ]

# 健康检查告警策略
health_alarm_policy = {'frequency': 1, "times": 1, 'timeout': 10, 'severity': Severity.WARNING}