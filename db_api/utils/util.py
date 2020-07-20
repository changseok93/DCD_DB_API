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


def find_id_name(table):
    if table is 'Environment':
        id_name = 'env_id'
    elif table is 'Grid':
        id_name = 'grid_id'
    elif table is 'SuperCategory':
        id_name = 'super_id'
    elif table is 'Image':
        id_name = 'img_id'
    elif table is 'Location':
        id_name = 'loc_id'
    elif table is 'Category':
        id_name = 'cat_id'
    elif table is 'Object':
        id_name = 'obj_id'
    elif table is 'Bbox':
        id_name = 'bbox_id'
    elif table is 'Mask':
        id_name = 'mask_id'

    return id_name