# -*- coding: utf-8 -*-
from db_api.DB import DB
from db_api.DB import *
from os import listdir
from os.path import join
from db_api.utils.util import cpu_mem_check
from db_api.utils.img_util import img_loader
from functools import wraps

import time
import os


# decorator
def print_check(func):
    @wraps(func)
    def show(self, *method_args, **method_kwargs):
        func(self)
        print("{} 결과:".format(func.__name__[1:]), self.ans)
    return show


# decorator
def print_basic(func):
    @wraps(func)
    def show(self, *method_args, **method_kwargs):
        func(self)
        print('{} table: '.format(func.__name__[1:]), self.table)
        print('{} table last id: '.format(func.__name__[1:]), self.last_id)

    return show


class CheckBasic:
    def __init__(self, db):
        self.db = db
        self.db.init_table()
        self.table = None
        self.last_id = None

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

    @print_basic
    def _environment(self):
        # check environment fucntions
        self.db.set_environment(ipv4='127.223.444.445', floor='1', width='3', height='4', depth='2')
        self.db.get_table(id='20001', table='Environment')
        # self.db.delete_table(id='1', table='Environment')
        self.db.update_environment(env_id='20001', ipv4='127.223.444.444')
        self.table = self.db.list_table(table='Environment')
        self.last_id = self.db.get_last_id(table="Environment")

    @print_basic
    def _supercategory(self):
        self.db.set_supercategory(super_name='hi')
        self.db.get_table(id='1', table='SuperCategory')
        # self.db.delete_table(id='1', table='SuperCategory')
        self.db.update_supercategory(super_id='1', super_name='hi')
        self.table = self.db.list_table(table='SuperCategory')
        self. last_id = self.db.get_last_id(table='SuperCategory')

    @print_basic
    def _grid(self):
        self.db.set_grid(width='1', height='1')
        self.db.get_table(id='1', table='Grid')
        # self.db.delete_table(id='1', table='Grid')
        self.db.update_grid(grid_id='1', width='1')
        self.table = self.db.list_table(table='Grid')
        self.last_id = self.db.get_last_id(table='Grid')

    @print_basic
    def _image(self):
        self.db.set_image(env_id='20001', img='1', type='0', check_num='1')
        self.db.get_table(id='1', table='Image')
        # self.db.delete_table(id='1', table='Image')
        self.db.update_image(img_id='1', env_id='20001')
        self.table = self.db.list_table(table='Image')
        self.last_id = self.db.get_last_id(table='Image')

    @print_basic
    def _location(self):
        self.db.set_location(grid_id='1', x='1', y='1')
        self.db.get_table(id='1', table='Location')
        # self.db.delete_table(id='1', table='Location')
        self.db.update_location(loc_id='1', x='1')
        self.table = self.db.list_table(table='Location')
        self.last_id = self.db.get_last_id(table='Location')

    @print_basic
    def _category(self):
        self.db.set_category(super_id='1', cat_name='1', width='1', height='1', depth='1', iteration='1', thumbnail='1')
        self.db.get_table(id='1', table='Category')
        # self.db.delete_table(id='1', table='Category')
        self.db.update_category(cat_id='1', cat_name='1')
        self.table = self.db.list_table(table='Category')
        self.last_id = self.db.get_last_id(table='Category')

    @print_basic
    def _object(self):
        self.db.set_object(img_id='1', loc_id='1', cat_id='1', iteration='1', mix_num='-1')
        self.db.get_table(id='1', table='Object')
        # self.db.delete_table(id='1', table='Object')
        self.db.update_object(obj_id='1', loc_id='1')
        self.table = self.db.list_table(table='Object')
        self.last_id = self.db.get_last_id(table='Object')

    @print_basic
    def _bbox(self):
        self.db.set_bbox(obj_id='1', x='1', y='1', width='1', height='1')
        self.db.get_table(id='1', table='Bbox')
        # self.db.delete_table(id='1', table='Bbox')
        self.db.update_bbox(bbox_id='1', x='1')
        self.table = self.db.list_table(table='Bbox')
        self.last_id = self.db.get_last_id(table='Bbox')

    @print_basic
    def _mask(self):
        self.db.set_mask(obj_id='1', x='1', y='1')
        self.db.get_table(id='1', table='Mask')
        # self.db.delete_table(id='1', table='Mask')
        self.db.update_mask(mask_id='1', x='1')
        self.table = self.db.list_table(table='Mask')
        self.last_id = self.db.get_last_id(table='Mask')


class CheckGet:
    def __init__(self, db):
        self.db = db
        self.ans = None

    def check_all(self):
        self._get_env_id()
        self._get_grid_id()
        self._get_super_id_SN()
        self._get_super_id_CI()
        self._get_super_name()
        self._get_loc_id()
        self._get_loc_id_GL()
        self._get_loc()
        self._get_cat_id_SI()
        self._get_cat_id_SN()
        self._get_img_id()
        self._get_cat_id_obj()
        self._get_obj_id_img()
        self._get_obj_id()
        self._get_mix_num()
        self._get_bbox_id()
        self._get_bbox()
        self._get_bbox_img()
        self._get_mask_id()

    @print_check
    def _get_env_id(self):
        self.ans = self.db.get_env_id(ipv4='127.223.444.444', floor='1')

    @print_check
    def _get_grid_id(self):
        self.ans = self.db.get_grid_id(grid_w_h='1x1')

    @print_check
    def _get_super_id_SN(self):
        self.ans = self.db.get_super_id_SN(super_name='hi')

    @print_check
    def _get_super_id_CI(self):
        self.ans = self.db.get_super_id_CI(cat_id='1')

    @print_check
    def _get_super_name(self):
        self.ans = self.db.get_super_name(super_id='1')

    @print_check
    def _get_loc_id(self):
        self.ans = self.db.get_loc_id(grid_id='1', loc_x_y='1x1')

    @print_check
    def _get_loc_id_GL(self):
        self.ans = self.db.get_loc_id_GL(grid_w_h='1x1', loc_x_y='1x1')

    @print_check
    def _get_loc(self):
        self.ans = self.db.get_loc(grid_id='1')

    @print_check
    def _get_cat_id_SI(self):
        self.ans = self.db.get_cat_id_SI(super_id='1', cat_name='1')

    @print_check
    def _get_cat_id_SN(self):
        self.ans = self.db.get_cat_id_SN(super_name='hi', cat_name='1')

    @print_check
    def _get_img_id(self):
        self.ans = self.db.get_img_id(obj_id='1')

    @print_check
    def _get_cat_id_obj(self):
        self.ans = self.db.get_cat_id_obj(obj_id='1')

    @print_check
    def _get_obj_id_img(self):
        self.ans = self.db.get_obj_id_img(img_id='1')

    @print_check
    def _get_obj_id(self):
        self.ans = self.db.get_obj_id(cat_id='1')

    @print_check
    def _get_mix_num(self):
        self.ans = self.db.get_mix_num(loc_id='1', cat_id='1', iteration='1')

    @print_check
    def _get_bbox_id(self):
        self.ans = self.db.get_bbox_id(obj_id='1')

    @print_check
    def _get_bbox(self):
        self.ans = self.db.get_bbox(obj_id='1')

    @print_check
    def _get_bbox_img(self):
        self.ans = self.db.get_bbox_img(img_id='1')

    @print_check
    def _get_mask_id(self):
        self.ans = self.db.get_mask_id(obj_id='1')


class CheckList:
    def __init__(self, db):
        self.db = db
        self.ans = None

    def check_all(self):
        self._list_bbox()
        self._list_obj()
        self._list_obj_CN()

    @print_check
    def _list_bbox(self):
        self.ans = self.db.list_bbox(obj_id='1')

    @print_check
    def _list_obj(self):
        self.ans = self.db.list_obj(cat_id='1', loc_ids='1')

    @print_check
    def _list_obj_CN(self):
        self.ans = self.db.list_obj_CN(grid_id='1', cat_id='1', check_num='-1')


class CheckCheck:
    def __init__(self, db):
        self.db = db
        self.ans = None

    def check_all(self):
        self._check_obj_id()
        self._check_nomix_OBM()
        self._check_cat_id()

    @print_check
    def _check_obj_id(self):
        self.ans = self.db.check_obj_id(loc_id='1', cat_id='1', iteration='1', mix_num='1')

    @print_check
    def _check_nomix_OBM(self):
        self.ans = self.db.check_nomix_OBM(cat_id='1')

    @print_check
    def _check_cat_id(self):
        self.ans = self.db.check_cat_id(super_name='1', cat_name='1')


class CheckUpdate:
    def __init__(self, db):
        self.db = db
        self.ans = None

    def check_all(self):
        self._update_img_CN_OI()
        self._update_img_CN_II()
        self._update_img_img_OI()
        self._update_img_img_II()

    @print_check
    def _update_img_CN_OI(self):
        self.ans = self.db.update_img_CN_OI(obj_id='1', check_num='1')

    @print_check
    def _update_img_CN_II(self):
        self.ans = self.db.update_img_CN_II(img_id='1', check_num='1')

    @print_check
    def _update_img_img_OI(self):
        self.ans = self.db.update_img_img_OI(obj_id='1', img='1')

    @print_check
    def _update_img_img_II(self):
        self.ans = self.db.update_img_img_II(img_id='1', img='1')


class CheckDelete:
    def __init__(self, db):
        self.db = db
        self.ans = None

    def check_all(self):
        self._delete_object()
        self._delete_bbox()
        self._delete_mask()
        self._delete_bbox_img()
        self._delete_nomix_img()

    @print_check
    def _delete_object(self):
        self.ans = self.db.delete_object(img_id='1')

    @print_check
    def _delete_bbox(self):
        self.ans = self.db.delete_bbox(obj_id='1')

    @print_check
    def _delete_mask(self):
        self.ans = self.db.delete_mask(obj_id='1')

    @print_check
    def _delete_bbox_img(self):
        self.ans = self.db.delete_bbox_img(img_id='1')

    @print_check
    def _delete_nomix_img(self):
        self.ans = self.db.delete_nomix_img(img_id='1')


class CheckAug:
    def __init__(self, db):
        self.db = db
        self.ans = None

    def check_all(self):
        self._get_aug_mask()
        self._get_aug_img()
        self._get_aug_loc_id()

    def _get_aug_mask(self):
        self.ans = self.db.get_aug_mask(grid_id='1', cat_id='1')

    def _get_aug_img(self):
        self.ans = self.db.get_aug_img(grid_id='1', cat_id='1')

    def _get_aug_loc_id(self):
        self.ans = self.db.get_aug_loc_id(grid_id='1')


class CheckSet:
    def __init__(self, db):
        self.db = db
        self.ans = None

    def check_all(self):
        self._set_obj_list()
        self._set_bulk_obj()
        self._set_bulk_bbox()
        self._set_bulk_img()

    def _set_obj_list(self):
        self.ans = self.db.set_obj_list(grid_id='1', cat_id='1', iteration='1', mix_num='1')

    def _set_bulk_obj(self):
        # self.ans = self.db.set_bulk_obj(datas=)
        pass

    def _set_bulk_bbox(self):
        ex_table = ([('1', '1', "{}".format(i), '1', '1') for i in range(4, 10)])
        self.ans = self.db.set_bulk_bbox(datas=ex_table)

    def _set_bulk_img(self):
        # img_path = '/home/cha/DB/img/aug_img'
        # ex_table = (['20001', img_loader(join(img_path, img_p)), '1', '1'] for img_p in sorted(listdir(img_path)))
        # self.ans = self.db.set_bulk_img(datas=ex_table)
        pass


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


def set_bulk_bbox():
    # (obj_id, x, y, width, height)

    start_time = time.time()
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
    cpu_mem_check()

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

    # get 함수 test
    cg = CheckGet(mydb)
    cg.check_all()

    # list 함수 test
    cl = CheckList(mydb)
    cl.check_all()

    # check 함수 test
    ct = CheckCheck(mydb)
    ct.check_all()

    # update 함수 test
    cu = CheckUpdate(mydb)
    cu.check_all()

    # delete 함수 test
    cd = CheckDelete(mydb)
    cd.check_all()

    # aug 함수 test
    ca = CheckAug(mydb)
    ca.check_all()

    # set 함수 test
    # cs = CheckSet(mydb)
    # cs.check_all()


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
    # mydb.set_image(env_id='20002', img='1ddd', type='2', check_num='3')
    # mydb.set_location(grid_id='1', x='1', y='2')
    # mydb.set_object(img_id='1', loc_id='2', cat_id='1', iteration='1', mix_num='-1')
    # mydb.set_object(img_id='2', loc_id='2', cat_id='1', iteration='3', mix_num='-1')
    # print(mydb.get_aug_img(grid_id='1', cat_id='1'))

    # get_aug_loc_id test 코드
    # mydb.set_location(grid_id='1', x='1', y='2')
    # mydb.set_location(grid_id='1', x='2', y='1')
    # mydb.set_location(grid_id='1', x='2', y='2')
    # print(mydb.get_aug_loc_id(grid_id='1'))

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