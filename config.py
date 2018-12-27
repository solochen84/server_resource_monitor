# -*- coding: utf-8 -*-

import paramiko
from enum import Enum


# 通用的cluster private key
common_cluster_pkey = paramiko.RSAKey.from_private_key_file('/Users/chenxiaolu/cloud2go/key/test')

# 通用的infra private key
common_infra_pkey = paramiko.RSAKey.from_private_key_file('/Users/chenxiaolu/cloud2go/key/test')

# host list, 格式为IP、port、username、password（没有时填None）、private_key
host_lists = [('10.10.10.45', 22, 'root', '123456'),
              ('10.10.10.71', 22, 'root', '123456'),
              ('123.58.33.18', 22, 'root', None, common_cluster_pkey)]

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
disk_alarm_policy = {'frequency': 1, "times": 5, 'threshold': 85, 'severity': Severity.WARNING}


health_check_services = [('123.58.33.18', 22, 'ssh服务'),

                         ]

# 健康检查告警策略
health_alarm_policy = {'frequency': 1, "times": 2, 'timeout': 10, 'severity': Severity.WARNING}