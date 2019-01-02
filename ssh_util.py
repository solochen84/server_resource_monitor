# -*- coding: utf-8 -*-

import paramiko
import re


def ssh_connect(hostname, port, username='root', password='123456', pkey=None):
    """
    连接ssh
    :param hostname:
    :param port:
    :param username:
    :param password:
    :param pkey:
    :return:
    """
    # paramiko.util.log_to_file('paramiko_log')
    try:
        sshClient = paramiko.SSHClient()
        sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if pkey:
            sshClient.connect(hostname, port, username, pkey=pkey)
        else:
            sshClient.connect(hostname, port, username, password)
    except Exception as e:
        print(e.with_traceback())
        print(e)
        print('SSH连接失败')
        exit()
    return sshClient


def ssh_exec_cmd(sshClient, command):
    """
    执行shell命令
    :param sshClient:
    :param command:
    :return:
    """
    stdin, stdout, stderr = sshClient.exec_command(command)
    filesystem_usage = stdout.readlines()
    return filesystem_usage


def ssh_close(sshClient):
    sshClient.close()


# 获取CPU使用率
def get_cpu_info(ssh_client):
    command = 'vmstat 1 1 | tail -n 1'
    ssh_res = ssh_exec_cmd(ssh_client, command)
    resource_info_list = list(ssh_res[0].split())
    cpu_us = int(resource_info_list[12])
    cpu_sy = int(resource_info_list[13])
    # cpu_id = resource_info_list[14]
    cpu_use = cpu_us+cpu_sy
    return cpu_use


# 获取CPU的15分钟load值
def get_cpu15(ssh_client):
    command = 'uptime'
    ssh_res = ssh_exec_cmd(ssh_client, command)
    alist = list(ssh_res[0].split(','))
    cpu15 = float(alist[-1].strip('\n'))
    return cpu15


# 获取主机内存占用百分比
def get_mem_info(ssh_client):
    command = 'cat /proc/meminfo'
    ssh_res = ssh_exec_cmd(ssh_client, command)
    # print(ssh_res)
    mem_values = re.findall("(\d+)\ kB", ",".join(ssh_res))
    mem_total = mem_values[0]
    mem_free = mem_values[1]
    mem_buffers = mem_values[3]
    mem_cached = mem_values[4]
    act_free_mem = int(mem_free) + int(mem_buffers) + int(mem_cached)
    act_used_mem = int(mem_total) - act_free_mem
    act_used_mem_percentage = 100*act_used_mem/float(mem_total)
    return act_used_mem_percentage


# 获取主机磁盘占用百分比
def get_disk_used_percentage(ssh_client):
    command = 'df -h'
    ssh_res = ssh_exec_cmd(ssh_client, command)
    ssh_res_str = ''.join(ssh_res)
    res_list = ssh_res_str.strip().split('\n')
    del(res_list[0])
    disk_list = []
    for element in res_list:
        disk_list.append(tuple(element.split()))
    return disk_list


# 获取CPU核数
def get_cpu_cores(ssh_client):
    command = 'cat /proc/cpuinfo| grep processor | wc -l'
    ssh_res = ssh_exec_cmd(ssh_client, command)
    cores_num = int(ssh_res[0])
    print(cores_num)
    return cores_num


if __name__ == '__main__':
    common_pkey = paramiko.RSAKey.from_private_key_file('/Users/chenxiaolu/cloud2go/key/test')
    host = ('123.58.33.18', 22, 'root', None, common_pkey)
    ssh_client = ssh_connect(*host)
    get_cpu_cores(ssh_client)





