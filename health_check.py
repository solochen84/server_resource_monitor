# -*- coding: utf-8 -*-

import telnetlib
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import time
import send_message as sm
from config import health_check_services, health_alarm_policy


def get_health(host, port, timeout):
    """
    Telnet远程测试连接：客户端连接Linux服务器
    """
    try:
        tn = telnetlib.Telnet(host, port=port, timeout=timeout)
        tn.close()
    except:
        return False
    return True


def monitor_health(host, port, service_name, health_alarm_policy):
    frequency = health_alarm_policy['frequency']
    times = health_alarm_policy['times']
    timeout = health_alarm_policy['timeout']
    severity = health_alarm_policy['severity']
    count = 0
    while True:
        # is_healthy = get_health(host, port, timeout)
        is_healthy = get_health('59.110.170.216', 8003, 10)
        if not is_healthy:
            count += 1
        else:
            count = 0
        if count >= times:
            sm.monitor_notify_dingding(
                "[%s] 服务（%s）%s:%d连续%d次无响应。" % (severity.name, service_name, host, port, count))
        time.sleep(frequency * 60)


def start(scheduler):
    for service in health_check_services:
        scheduler.add_job(func=monitor_health, args=(service[0], service[1], service[2], health_alarm_policy),
                          next_run_time=datetime.datetime.now())
    scheduler.start()


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    try:
        start(scheduler)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown(False)
