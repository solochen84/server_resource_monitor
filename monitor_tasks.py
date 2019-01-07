# -*- coding: utf-8 -*-

from config import host_lists, CPU15_alarm_policy, CPU_alarm_policy, mem_alarm_policy, disk_alarm_policy
from ssh_util import ssh_connect
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
from monitor_server import monitor_cpu_load15, monitor_cpu_use, monitor_disk, monitor_mem
from send_message import monitor_notify_dingding
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
import logging


def start(scheduler, ssh_client_list, msg_list):
    for host in host_lists:
        ssh_client = ssh_connect(*host)
        ssh_client_list.append(ssh_client)
        scheduler.add_job(func=monitor_cpu_use, args=(ssh_client, host[0], host[1], CPU_alarm_policy, msg_list),
                          next_run_time=datetime.datetime.now(), misfire_grace_time=3600)
        scheduler.add_job(func=monitor_cpu_load15, args=(ssh_client, host[0], host[1], CPU15_alarm_policy, msg_list),
                          next_run_time=datetime.datetime.now(), misfire_grace_time=3600)
        scheduler.add_job(func=monitor_mem, args=(ssh_client, host[0], host[1],  mem_alarm_policy, msg_list),
                          next_run_time=datetime.datetime.now(), misfire_grace_time=3600)
        scheduler.add_job(func=monitor_disk, args=(ssh_client, host[0], host[1], disk_alarm_policy, msg_list, ),
                          next_run_time=datetime.datetime.now(), misfire_grace_time=3600)

    # 每隔1分钟将1分钟内的告警一起发一条Markdown消息出去
    scheduler.add_job(func=send_mk_dingding_msg, args=(msg_list,), trigger='interval', seconds=60, misfire_grace_time=3600)

    print(len(scheduler.get_jobs()))
    scheduler.start()


def stop(scheduler, ssh_client_list):
    scheduler.shutdown(False)
    for ssh_client in ssh_client_list:
        ssh_client.close()


def send_mk_dingding_msg(alist):
    if len(alist) > 0:
        monitor_notify_dingding(alist)
        del alist[:]


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', filename='log.txt', filemode='a')

    executors = {
        'default': ThreadPoolExecutor(500),
        'processpool': ProcessPoolExecutor(5)
    }
    scheduler = BlockingScheduler(executors=executors)
    scheduler._logger = logging
    ssh_client_list = []
    msg_list = []

    try:
        start(scheduler, ssh_client_list, msg_list)
    except (KeyboardInterrupt, SystemExit):
        stop(scheduler, ssh_client_list)



