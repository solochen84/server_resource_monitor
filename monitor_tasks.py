# -*- coding: utf-8 -*-

from config import host_lists, CPU15_alarm_policy, CPU_alarm_policy, mem_alarm_policy, disk_alarm_policy
from ssh_util import ssh_connect
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
from monitor_server import monitor_cpu_load15, monitor_cpu_use, monitor_disk, monitor_mem


def start(scheduler, ssh_client_list):
    for host in host_lists:
        ssh_client = ssh_connect(*host)
        ssh_client_list.append(ssh_client)
        scheduler.add_job(func=monitor_cpu_use, args=(ssh_client, host[0], CPU_alarm_policy),
                          next_run_time=datetime.datetime.now())
        scheduler.add_job(func=monitor_cpu_load15, args=(ssh_client, host[0], CPU15_alarm_policy),
                          next_run_time=datetime.datetime.now())
        scheduler.add_job(func=monitor_mem, args=(ssh_client, host[0], mem_alarm_policy),
                          next_run_time=datetime.datetime.now())
        scheduler.add_job(func=monitor_disk, args=(ssh_client, host[0], disk_alarm_policy),
                          next_run_time=datetime.datetime.now())
    scheduler.start()


def stop(scheduler, ssh_client_list):
    scheduler.shutdown(False)
    for ssh_client in ssh_client_list:
        ssh_client.close()


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    ssh_client_list = []
    try:
        start(scheduler, ssh_client_list)
    except (KeyboardInterrupt, SystemExit):
        stop(scheduler, ssh_client_list)



