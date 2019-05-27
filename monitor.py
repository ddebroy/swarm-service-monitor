#!/usr/bin/env python

import os
import json
import argparse
import sys
import subprocess
from datetime import datetime, timedelta
import time
import docker
import pytz
import maya

failed_service_tasks = {}

def analyze_svc(service, max_rejected_tasks, interval_in_seconds):
    for task in service.tasks():
        task_id = task['ID']
        task_status = task['Status']
        task_state = task_status['State']
        if task_state == 'rejected':
            print "     found rejected task:", task['ID'], "in service:", service.id
            timestamp = maya.parse(task_status['Timestamp']).datetime(to_timezone='UTC')
            task_map = failed_service_tasks[service.id]
            task_map[task_id] = timestamp
    task_map = failed_service_tasks[service.id]
    if len(task_map) == 0:
        del failed_service_tasks[service.id]
        return
    rejections = 0
    current_ts = datetime.utcnow().replace(tzinfo=pytz.utc)
    for task_entry in task_map:
        timedelta = current_ts - task_map[task_entry]
        # print "     timedelta: ", timedelta.total_seconds()
        if timedelta.total_seconds() < interval_in_seconds:
            rejections += 1
    print "     rejected tasks within last", interval_in_seconds, "seconds:", rejections 
    if rejections > max_rejected_tasks:
        # remove task_map entry
        print "     scale down service to zero: ", service.id, ".", max_rejected_tasks, "rejected tasks detected"
        try:
            del failed_service_tasks[service.id]
            service.scale(0)
        except docker.errors.APIError as error:
            print "     ignoring docker API error: ", error
        return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interval_in_seconds', type=int, help='maximum number of seconds elpased since creation of a rejected task for the task to be considered in max_rejected_tasks')
    parser.add_argument('-t', '--max_rejected_tasks', type=int, help='maximum number of tasks rejected within interval_in_seconds before a service is scaled down to zero')
    args = parser.parse_args()

    interval_in_seconds = 90
    if args.interval_in_seconds:
        interval_in_seconds = args.interval_in_seconds

    max_rejected_tasks = 60
    if args.max_rejected_tasks:
        max_rejected_tasks = args.max_rejected_tasks

    while True:
        docker_client = docker.from_env(version="1.39")
        api_client = docker.APIClient(base_url='unix://var/run/docker.sock')
        services = docker_client.services.list()
        for service in services:
            svc_mode = api_client.inspect_service(service.id)['Spec']['Mode']
            if 'Replicated' in svc_mode and svc_mode['Replicated']['Replicas'] == 0:
                # print "Replica count for service", service.id, "is zero. Skipping ..."
                continue
            if not service.id in failed_service_tasks:
                # print "Initializing service entry for ", service.id
                failed_service_tasks[service.id] = {}
            print "Analyzing service:", service.id, "tracking", len(failed_service_tasks[service.id]), "rejected tasks"
            analyze_svc(service, max_rejected_tasks, interval_in_seconds)
        docker_client.close()
        sys.stdout.flush()
        time.sleep(5)

if __name__ == "__main__":
    main()
