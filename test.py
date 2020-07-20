# -*- coding: utf-8 -*-
from db_api.DB import DB
from db_api.DB import *
from os import listdir
from os.path import join
from db_api.utils.util import cpu_mem_check
from db_api.utils.img_util import img_loader

import time
import os


class CheckBasic:
    def __init__(self, db):
        self.db = db
        self.db.init_table()

    def check_all(self):
        self._environment()
        self._supercategory()
        self._grid()
        self._image()
        self._location()
        self._category()
        self._object()
        self._bbox()
        self._mask()

    def _environment(self):
        # check environment fucntions
        self.db.set_environment(ipv4='127.223.444.445', floor='1', width='3', height='4', depth='2')
        self.db.get_table(id='20001', table='Environment')
        # self.db.delete_table(id='1', table='Environment')
        self.db.update_environment(env_id='20001', ipv4='127.223.444.444')
        print('Environment table: ', self.db.list_table(table='Environment'))
        print('Environment table last id: ', self.db.get_last_id(table="Environment"))

    def _supercategory(self):
        self.db.set_supercategory(super_name='hi')
        self.db.get_table(id='1', table='SuperCategory')
        # self.db.delete_table(id='1', table='SuperCategory')
        self.db.update_supercategory(super_id='1', super_name='hi')
        print('SuperCateogry table: ', self.db.list_table(table='SuperCategory'))
        print('SuperCategory table last id: ', self.db.get_last_id(table='SuperCategory'))

    def _grid(self):
        self.db.set_grid(width='1', height='1')
        self.db.get_table(id='1', table='Grid')
        # self.db.delete_table(id='1', table='Grid')
        self.db.update_grid(grid_id='1', width='1')
        print('Grid table: ', self.db.list_table(table='Grid'))
        print('Grid table last id: ', self.db.get_last_id(table='Grid'))

    def _image(self):
        self.db.set_image(env_id='20001', img=img, type='0', check_num='1')
        self.db.get_table(id='1', table='Image')
        # self.db.delete_table(id='1', table='Image')
        self.db.update_image(img_id='1', env_id='20001')
        # print('Image table: ', self.db.list_table(table='Image'))
        print('Image table last id: ', self.db.get_last_id(table='Image'))

    def _location(self):
        self.db.set_location(grid_id='1', x='1', y='1')
        self.db.get_table(id='1', table='Location')
        # self.db.delete_table(id='1', table='Location')
        self.db.update_location(loc_id='1', x='1')
        print('Location table: ', self.db.list_table(table='Location'))
        print('Location table last id: ', self.db.get_last_id(table='Location'))

    def _category(self):
        self.db.set_category(super_id='1', cat_name='1', width='1', height='1', depth='1', iteration='1', thumbnail='1')
        self.db.get_table(id='1', table='Category')
        # self.db.delete_table(id='1', table='Category')
        self.db.update_category(cat_id='1', cat_name='1')
        print('Category table: ', self.db.list_table(table='Category'))
        print('Category table last id: ', self.db.get_last_id(table='Category'))

    def _object(self):
        self.db.set_object(img_id='1', loc_id='1', cat_id='1', iteration='1', mix_num='-1')
        self.db.get_table(id='1', table='Object')
        # self.db.delete_table(id='1', table='Object')
        self.db.update_object(obj_id='1', loc_id='1')
        print('Object table: ', self.db.list_table(table='Object'))
        print('Object table last id: ', self.db.get_last_id(table='Object'))

    def _bbox(self):
        self.db.set_bbox(obj_id='1', x='1', y='1', width='1', height='1')
        self.db.get_table(id='1', table='Bbox')
        # self.db.delete_table(id='1', table='Bbox')
        self.db.update_bbox(bbox_id='1', x='1')
        print('Bbox table: ', self.db.list_table(table='Bbox'))
        print('Bbox table last id: ', self.db.get_last_id(table='Bbox'))

    def _mask(self):
        self.db.set_mask(obj_id='1', x='1', y='1')
        self.db.get_table(id='1', table='Mask')
        # self.db.delete_table(id='1', table='Mask')
        self.db.update_mask(mask_id='1', x='1')
        print('Mask table: ', self.db.list_table(table='Mask'))
        print('Mask table last id: ', self.db.get_last_id(table='Mask'))


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
    img_dir = 'img/1.png'
    img = img_loader(img_dir)

    # cunnect to MYSQL Server
    mydb = DB(ip='192.168.10.69',
              port=20000,
              user='root',
              password='return123',
              db_name='test')

    # reset tables
    reset_table(mydb)

    # id를 기반으로 하는 basic 코드 test
    cb = CheckBasic(mydb)
    cb.check_all()

    # get_loc_id_GL test 코드
    # mydb.set_grid(width='1', height='2')
    # mydb.set_grid(width='1', height='3')
    # mydb.set_location(grid_id='1', x='1', y='2')
    # mydb.set_location(grid_id='1', x='1', y='3')
    # mydb.set_location(grid_id='1', x='1', y='4')
    # mydb.set_location(grid_id='1', x='1', y='5')
    # print(mydb.get_loc_id_GL(grid_w_h='1x1', loc_x_y='1x1'))

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
    # print(mydb.set_obj_list(grid_id='1', category_id='1', iteration='3', mix_num='-1'))

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
    # compare_set_bulk_img()

    # # db_to_json test 코드
    # mydb.set_supercategory(name='생수')
    # mydb.set_category(super_id='2', name='삼다수', width='1', height='1', depth='1', iteration='1', thumbnail='1')
    # mydb.set_object(img_id='1', loc_id='1', category_id='2', iteration='2', mix_num='-1')
    # mydb.set_mask(obj_id='2', x='1', y='2')
    # mydb.set_mask(obj_id='2', x='1', y='3')
    # mydb.set_mask(obj_id='2', x='1', y='4')
    # mydb.set_bbox(obj_id='2', x='1', y='1', width='1', height='1')
    #
    # mydb.set_image(device_id='20001', image=img, type='0', check_num='1')
    # mydb.set_image(device_id='20001', image=img, type='0', check_num='1')
    # mydb.set_mask(obj_id='1', x='1', y='2')
    # mydb.set_mask(obj_id='1', x='1', y='3')
    # mydb.set_mask(obj_id='1', x='1', y='4')
    #
    # json_path = "./coco_info.json"
    # img_path = "./img"
    # if not os.path.exists(img_path):
    #     os.makedirs(img_path)
    #
    # print(mydb.db_to_json(json_path=json_path, img_path=img_path))