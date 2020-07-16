import json


def save_json(json_path, coco_format):
    # json type file write -> utf-8 encoding
    with open(json_path, 'w', encoding='UTF-8') as json_file:
        json.dump(coco_format, json_file, ensure_ascii=False)
