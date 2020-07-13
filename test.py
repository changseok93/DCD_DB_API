# -*- coding: utf-8 -*-
from db_api.DB import DB
from db_api.DB import *
from os import listdir
from os.path import join
from utils.memory import cpu_mem_check

import time


def img_loader(img_dir):
    if isinstance(img_dir, str):
        with open(img_dir, 'rb') as file:
            img = file.read()

    return img


def check_environment(db):
    # check environment fucntions
    db.set_environment(ipv4='127.223.444.445', floor='1', width='3', height='4', depth='2')
    db.get_table(id='20001', table='Environment')
    # db.delete_table(id='1', table='Environment')
    db.update_environment(id='20001', ipv4='127.223.444.444')
    print('Environment table: ', db.list_table(table='Environment'))
    print('Environment table last id: ', db.get_last_id(table="Environment"))


def check_image(db):
    db.set_image(device_id='20001', image=img, type='0', check_num='1')
    db.get_table(id='1', table='Image')
    # db.delete_table(id='1', table='Image')
    db.update_image(id='1', device_id='20001')
    # print('Image table: ', db.list_table(table='Image'))
    print('Image table last id: ', db.get_last_id(table='Image'))


def check_grid(db):
    db.set_grid(width='1', height='1')
    db.get_table(id='1', table='Grid')
    # db.delete_table(id='1', table='Grid')
    db.update_grid(id='1', width='1')
    print('Grid table: ', db.list_table(table='Grid'))
    print('Grid table last id: ', db.get_last_id(table='Grid'))


def check_location(db):
    db.set_location(grid_id='1', x='1', y='1')
    db.get_table(id='1', table='Location')
    # db.delete_table(id='1', table='Location')
    db.update_location(id='1', x='1')
    print('Location table: ', db.list_table(table='Location'))
    print('Location table last id: ', db.get_last_id(table='Location'))


def check_supercategory(db):
    db.set_supercategory(name='hi')
    db.get_table(id='1', table='SuperCategory')
    # db.delete_table(id='1', table='SuperCategory')
    db.update_supercategory(id='1', name='hi')
    print('SuperCateogry table: ', db.list_table(table='SuperCategory'))
    print('SuperCategory table last id: ', db.get_last_id(table='SuperCategory'))


def check_category(db):
    db.set_category(super_id='1', name='1', width='1', height='1', depth='1', iteration='1', thumbnail='1')
    db.get_table(id='1', table='Category')
    # db.delete_table(id='1', table='Category')
    db.update_category(id='1', name='1')
    # print('Category table: ', db.list_table(table='Category'))
    print('Category table last id: ', db.get_last_id(table='Category'))


def check_object(db):
    db.set_object(img_id='1', loc_id='1', category_id='1', iteration='1', mix_num='-1')
    db.get_table(id='1', table='Object')
    # db.delete_table(id='1', table='Object')
    db.update_object(id='1', loc_id='1')
    print('Object table: ', db.list_table(table='Object'))
    print('Object table last id: ', db.get_last_id(table='Object'))


def check_bbox(db):
    db.set_bbox(obj_id='1', x='10', y='10', width='3', height='4')
    db.get_table(id='1', table='Bbox')
    # db.delete_table(id='1', table='Bbox')
    db.update_bbox(id='1', x='15')
    print('Bbox table: ', db.list_table(table='Bbox'))
    print('Bbox table last id: ', db.get_last_id(table='Bbox'))


def check_mask(db):
    db.set_mask(obj_id='1', x='1', y='1')
    db.get_table(id='1', table='Mask')
    # db.delete_table(id='1', table='Mask')
    db.update_mask(id='1', x='1')
    print('Mask table: ', db.list_table(table='Mask'))
    print('Mask table last id: ', db.get_last_id(table='Mask'))


def reset_table(db):
    db.drop_table(table='Bbox')
    db.drop_table(table='Mask')
    db.drop_table(table='Object')
    db.drop_table(table='Image')
    db.drop_table(table='Location')
    db.drop_table(table='Category')
    db.drop_table(table='Environment')
    db.drop_table(table='Grid')
    db.drop_table(table='SuperCategory')


def read_img_from_db(db, img_id, table):
    import cv2
    import numpy as np

    im = db.get_table(id=img_id, table=table)
    img_byte_str = im[2]
    img_dir = 'img/output.png'

    nparr = np.frombuffer(img_byte_str, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    cv2.imshow('d', img_np)
    cv2.waitKey(0)

    # byte 타입으로 저장도 가능
    # cv2를 굳이 안써도 되지만, cv2.imshow 불가
    with open(img_dir, 'wb') as file:
        file.write(img_byte_str)


def compare_set_bulk_bbox():
    # (obj_id, x, y, width, height)
    ex_table = ([('1', '1', "{}".format(i), '1', '1') for i in range(4, 10)])

    start_time = time.time()
    mydb.set_bulk_bbox(datas=ex_table)
    cpu_mem_check()
    end_time = time.time()
    print('total_time: ', end_time - start_time)


def compare_set_bulk_obj():
    # (img_id, loc_id, category_id, iteration, mix_num)
    ex_table = ([('1', '1', "1", "{}".format(i), '1') for i in range(4, 65533)])

    print('no execute many')
    start_time = time.time()
    print(mydb.set_bulk_obj(datas=ex_table))
    cpu_mem_check()
    end_time = time.time()
    print('total_time: ', end_time - start_time)


def compare_set_bulk_img():
    img_path = '/home/cha/DB/img/aug_img'

    # list case
    # (env_id, data, type, check_num)
    # start_time = time.time()
    # ex_table = [['20001', img_loader(join(img_path, img_p)), '1', '1'] for img_p in sorted(listdir(img_path))]
    # cpu_mem_check()

    # generator case
    # (env_id, data, type, check_num)
    start_time = time.time()
    ex_table = (['20001', img_loader(join(img_path, img_p)), '1', '1'] for img_p in sorted(listdir(img_path)))
    cpu_mem_check()

    print(mydb.set_bulk_img(datas=ex_table))
    cpu_mem_check()
    end_time = time.time()
    print('total_time: ', end_time - start_time)


if __name__ == "__main__":
    img_path = '/home/cha/DB/img/example.jpg'
    img = img_loader(img_path)

    # cunnect to MYSQL Server
    mydb = DB(ip='192.168.10.69',
              port=20000,
              user='root',
              password='return123',
              db_name='test')

    # reset tables
    reset_table(mydb)

    # table 초기화
    mydb.init_table()

    # # Environment table test
    check_environment(mydb)

    # SuperCategory table test
    check_supercategory(mydb)

    # Gird table test
    check_grid(mydb)

    # Image table test
    check_image(mydb)

    # Location table test
    check_location(mydb)

    # Category table test
    check_category(mydb)

    # Object table test
    check_object(mydb)

    # Bbox table test
    check_bbox(mydb)

    # Mask table test
    check_mask(mydb)

    # # get_mix_num test 코드
    # mydb.set_location(grid_id='1', x='1', y='2')
    # mydb.set_location(grid_id='1', x='1', y='3')
    # mydb.set_location(grid_id='1', x='1', y='4')
    # mydb.set_location(grid_id='1', x='1', y='5')
    # mydb.set_category(super_id='1', name='22', width='1', height='1', depth='22', iteration='2', thumbnail='1')
    # mydb.set_object(img_id='1', loc_id='5', category_id='2', iteration='1', mix_num='-1')
    # mydb.set_object(img_id='1', loc_id='5', category_id='2', iteration='1', mix_num='0')
    # mydb.set_object(img_id='1', loc_id='5', category_id='2', iteration='1', mix_num='1')
    # print(mydb.get_mix_num(loc_id='5', category_id='2', iteration='1'))

    # # list_obj_check_num test 코드
    # mydb.set_environment(ipv4='127.223.444.445', floor='1', width='3', height='5', depth='2')
    # mydb.set_image(device_id='20002', image='1ddd', type='2', check_num='3')
    # mydb.set_location(grid_id='1', x='1', y='2')
    # mydb.set_object(img_id='1', loc_id='2', category_id='1', iteration='1', mix_num='-1')
    # mydb.set_object(img_id='2', loc_id='2', category_id='1', iteration='3', mix_num='-1')
    # print(mydb.list_obj_check_num(grid_id='1', category_id='1', check_num='1'))

    # # delete_bbox_img test 코드
    # mydb.set_bbox(obj_id='1', x='1', y='2', width='1', height='1')
    # mydb.set_bbox(obj_id='1', x='1', y='3', width='1', height='1')
    # mydb.set_bbox(obj_id='1', x='1', y='3', width='1', height='1')
    # print(mydb.delete_bbox_img(img_id='1'))

    # # delete_nomix_img test 코드
    # mydb.set_supercategory(name='mix')
    # mydb.set_category(super_id='2', name='hi', width='1', height='1', depth='1', iteration='1', thumbnail='1')
    # mydb.set_object(img_id='1', loc_id='1', category_id='1', iteration='2', mix_num='-1')
    # mydb.set_object(img_id='1', loc_id='1', category_id='1', iteration='3', mix_num='-1')
    # mydb.set_object(img_id='1', loc_id='1', category_id='1', iteration='4', mix_num='-1')
    # mydb.set_object(img_id='1', loc_id='1', category_id='2', iteration='5', mix_num='-1')
    # mydb.set_object(img_id='1', loc_id='1', category_id='2', iteration='6', mix_num='-1')
    # mydb.set_object(img_id='1', loc_id='1', category_id='2', iteration='7', mix_num='-1')
    # mydb.set_object(img_id='1', loc_id='1', category_id='2', iteration='8', mix_num='-1')
    # # img_id=1이면 mix, img_id=2이면 mix 아님
    # print(mydb.delete_nomix_img(img_id='1'))

    # # list_obj_check_num test 코드
    # mydb.set_environment(ipv4='127.223.444.445', floor='1', width='3', height='5', depth='2')
    # mydb.set_image(device_id='20002', image='1ddd', type='2', check_num='1')
    # mydb.set_location(grid_id='1', x='1', y='2')
    # mydb.set_object(img_id='1', loc_id='2', category_id='1', iteration='1', mix_num='-1')
    # mydb.set_object(img_id='2', loc_id='2', category_id='1', iteration='3', mix_num='-1')
    # print(mydb.list_obj_check_num(grid_id='1', category_id='1', check_num='1'))

    # set_obj_list test 코드
    # mydb.delete_table(id='1', table='Object')
    # mydb.set_location(grid_id='1', x='1', y='2')
    # mydb.set_location(grid_id='1', x='1', y='3')
    # mydb.set_location(grid_id='1', x='1', y='4')
    # print(mydb.set_obj_list(grid_id='1', category_id='1', iteration='1', mix_num='1'))
    # print(mydb.set_obj_list(grid_id='1', category_id='1', iteration='2', mix_num='1'))
    # print(mydb.set_obj_list(grid_id='1', category_id='1', iteration='3', mix_num='1'))

    # get_aug_mask test 코드
    # mydb.set_location(grid_id='1', x='1', y='2')
    # mydb.set_object(img_id='1', loc_id='2', category_id='1', iteration='1', mix_num='-1')
    # mydb.set_mask(obj_id='1', x='1', y='2')
    # mydb.set_mask(obj_id='2', x='1', y='1')
    # mydb.set_mask(obj_id='2', x='1', y='2')
    # print(mydb.get_aug_mask(grid_id='1', category_id='1'))

    # # get_aug_img test 코드
    # mydb.set_environment(ipv4='127.223.444.445', floor='1', width='3', height='5', depth='2')
    # mydb.set_image(device_id='20002', image='1ddd', type='2', check_num='3')
    # mydb.set_location(grid_id='1', x='1', y='2')
    # mydb.set_object(img_id='1', loc_id='2', category_id='1', iteration='1', mix_num='-1')
    # mydb.set_object(img_id='2', loc_id='2', category_id='1', iteration='3', mix_num='-1')
    # print(mydb.get_aug_img(grid_id='1', category_id='1'))

    # get_aug_loc_id test 코드
    # mydb.set_location(grid_id='1', x='1', y='2')
    # mydb.set_location(grid_id='1', x='2', y='1')
    # mydb.set_location(grid_id='1', x='2', y='2')
    # print(mydb.get_aug_loc_id(grid_id='1'))

    # # set_bulk_obj test 코드
    # compare_set_bulk_obj()

    # set_bulk_bbox test 코드
    # compare_set_bulk_bbox()

    # set_bulk_img test 코드
    compare_set_bulk_img()