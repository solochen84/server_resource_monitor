# -*- coding: utf-8 -*-

import paramiko
import time
import send_message as sm
from ssh_util import get_disk_used_percentage, get_mem_info, get_cpu_info, get_cpu15, ssh_connect, get_cpu_cores


# CPU使用率监控
def monitor_cpu_use(ssh_client, host, alarm_policy, msg_list):
    """
    :param ssh_client:
    :param host_ip:
    :param frequency:检查评率，数值类型，单位是分钟
    :param times:次数
    :param threshold:阈值，传整数
    :param severity:严重级别
    :return:
    """
    frequency = alarm_policy['frequency']
    times = alarm_policy['times']
    threshold = alarm_policy['threshold']
    severity = alarm_policy['severity']
    host_ip = host[0]
    host_port = host[1]

    count = 0
    while True:
        if ssh_client is None:
            try:
                ssh_client = ssh_connect(*host)
            except Exception as d:
                print(str(d))
                msg_list.append("IP为%s、端口为%s的机器ssh连接不上" % (host_ip, str(host_port)))
                time.sleep(10)
                continue

        try:
            target_value = get_cpu_info(ssh_client)
        except Exception as e:
            print(str(e))
            msg_list.append("IP为%s、端口为%s的机器获取CPU使用率失败，错误信息为：%s" % (host_ip, str(host_port), str(e)))
            try:
                ssh_client.close()
            except Exception as f:
                pass
            ssh_client = None
            time.sleep(10)
            continue

        # print(id(ssh_client))
        if target_value >= threshold:
            count += 1
        else:
            count = 0
        if count >= times:
            alarm_msg = "[%s] IP为%s、端口为%s的机器cpu使用率连续%d次超过%d%%，当前值为%d%%" % (severity.name, host_ip, str(host_port), count, threshold, target_value)
            msg_list.append(alarm_msg)
        time.sleep(frequency*60)


# CPU load15监控
def monitor_cpu_load15(ssh_client, host, alarm_policy, msg_list):
    """
    :param ssh_client:
    :param host_ip:
    :param frequency:检查评率，数值类型，单位是分钟
    :param times:次数
    :param threshold:阈值，传整数，此函数中阈值从主机中动态获取
    :param severity:严重级别
    :return:
    """
    frequency = alarm_policy['frequency']
    times = alarm_policy['times']
    alarm_threshold = alarm_policy['threshold']
    threshold = get_cpu_cores(ssh_client)*alarm_threshold
    severity = alarm_policy['severity']
    count = 0
    host_ip = host[0]
    host_port = host[1]
    while True:
        if ssh_client is None:
            try:
                ssh_client = ssh_connect(*host)
            except Exception as d:
                print(str(d))
                msg_list.append("IP为%s、端口为%s的机器ssh连接不上" % (host_ip, str(host_port)))
                time.sleep(10)
                continue

        try:
            target_value = get_cpu15(ssh_client)
        except Exception as e:
            print(str(e))
            msg_list.append("IP为%s、端口为%s的机器获取CPU load15失败，错误信息为：%s" % (host_ip, str(host_port), str(e)))
            try:
                ssh_client.close()
            except Exception as f:
                pass
            ssh_client = None
            time.sleep(10)
            continue


        if target_value > threshold:
            count += 1
        else:
            count = 0
        if count >= times:
            alarm_msg = "[%s] IP为%s、端口为%s的机器cpu load15连续%d次超过%.2f，当前值为%.2f" % (severity.name, host_ip, str(host_port), count, threshold, target_value)
            msg_list.append(alarm_msg)
            # sm.monitor_notify_dingding("[%s] IP为%s、端口为%s的机器cpu load15连续%d次超过%d%%，当前值为%d%%" % (severity.name, host_ip, str(host_port), count, threshold, target_value))
        time.sleep(frequency*60)


# 内存使用率监控
def monitor_mem(ssh_client, host, alarm_policy, msg_list):
    """
    :param ssh_client:
    :param host_ip:
    :param frequency:检查评率，数值类型，单位是分钟
    :param times:次数
    :param threshold:阈值，传整数
    :param severity:严重级别
    :return:
    """
    frequency = alarm_policy['frequency']
    times = alarm_policy['times']
    threshold = alarm_policy['threshold']
    severity = alarm_policy['severity']
    count = 0
    host_ip = host[0]
    host_port = host[1]
    while True:
        if ssh_client is None:
            try:
                ssh_client = ssh_connect(*host)
            except Exception as d:
                print(str(d))
                msg_list.append("IP为%s、端口为%s的机器ssh连接不上" % (host_ip, str(host_port)))
                time.sleep(10)
                continue

        try:
            target_value = get_mem_info(ssh_client)
        except Exception as e:
            print(str(e))
            msg_list.append("IP为%s、端口为%s的机器获取内存使用率失败，错误信息为：%s" % (host_ip, str(host_port), str(e)))
            try:
                ssh_client.close()
            except Exception as f:
                pass
            ssh_client = None
            time.sleep(10)
            continue

        if target_value >= threshold:
            count += 1
        else:
            count = 0
        if count >= times:
            alarm_msg = "[%s] IP为%s、端口为%s的机器内存使用率连续%d次超过%d%%，当前值为%d%%" % (severity.name, host_ip, str(host_port), count, threshold, target_value)
            msg_list.append(alarm_msg)
            # sm.monitor_notify_dingding("[%s] IP为%s、端口为%s的机器内存使用率连续%d次超过%d%%，当前值为%d%%" % (severity.name, host_ip, str(host_port), count, threshold, target_value))
        time.sleep(frequency*60)


# 磁盘占用监控
def monitor_disk(ssh_client, host, alarm_policy, msg_list):
    """
    :param ssh_client:
    :param host_ip:
    :param frequency:检查评率，数值类型，单位是分钟
    :param times:次数
    :param threshold:阈值，传整数
    :param severity:严重级别
    :return:
    """
    frequency = alarm_policy['frequency']
    times = alarm_policy['times']
    threshold = alarm_policy['threshold']
    severity = alarm_policy['severity']
    times = 1
    host_ip = host[0]
    host_port = host[1]
    while True:
        if ssh_client is None:
            try:
                ssh_client = ssh_connect(*host)
            except Exception as d:
                print(str(d))
                msg_list.append("IP为%s、端口为%s的机器ssh连接不上" % (host_ip, str(host_port)))
                time.sleep(10)
                continue

        try:
            disk_list = get_disk_used_percentage(ssh_client)
        except Exception as e:
            print(str(e))
            msg_list.append("IP为%s、端口为%s的机器获取磁盘占用失败，错误信息为：%s" % (host_ip, str(host_port), str(e)))
            try:
                ssh_client.close()
            except Exception as f:
                pass
            ssh_client = None
            time.sleep(10)
            continue

        for element in disk_list:
            int_use = int(element[4].strip("%"))
            if int_use >= threshold:
                count += 1
            else:
                count = 0
            if count >= times:
                alarm_msg = "[%s] IP为%s、端口为%s的机器，文件系统%s、挂载点%s的磁盘使用率超过%d%%，当前值为%d%%" % (severity.name, host_ip, str(host_port), element[0], element[5], threshold, int_use)
                msg_list.append(alarm_msg)
                # sm.monitor_notify_dingding("[%s] IP为%s、端口为%s的机器，文件系统%s、挂载点%s的磁盘使用率超过%d%%，当前值为%d%%" % (severity.name, host_ip, str(host_port), element[0], element[5], threshold, int_use))
        time.sleep(frequency*60)


def main():
    common_pkey = paramiko.RSAKey.from_private_key_file('/Users/chenxiaolu/cloud2go/key/test')
    host = ('123.58.33.18', 22, 'root', None, common_pkey)
    # host = ('10.10.10.45', 22, 'root', '123456')

    ssh_client = ssh_connect(*host)
    print(get_disk_used_percentage(ssh_client))
    # monitor_cpu_use(ssh_client, host[0], 1, 1, 2, 1)
    # monitor_disk(ssh_client, host[0], 1, 1, 1, 1)


if __name__ == '__main__':
    main()




