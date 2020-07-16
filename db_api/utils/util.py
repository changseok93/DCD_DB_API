import json
import psutil
import os


def save_json(json_path, coco_format):
    # json type file write -> utf-8 encoding
    with open(json_path, 'w', encoding='UTF-8') as json_file:
        json.dump(coco_format, json_file, ensure_ascii=False)


def cpu_mem_check():
    pid = os.getpid()
    py = psutil.Process(pid)
    cpu_usage = os.popen("ps aux | grep " + str(pid) + " | grep -v grep | awk '{print $3}'").read()
    cpu_usage = cpu_usage.replace("\n", "")
    memory_usage = round(py.memory_info()[0] / 2. ** 30, 2)
    print("cpu usage:", cpu_usage, "%")
    print("memory usage:", memory_usage, "%")
