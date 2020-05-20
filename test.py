# -*- coding: utf-8 -*-
from db_api.DB import DB


def img_loader(img_dir):
    if isinstance(img_dir, str):
        with open(img_dir, 'rb') as file:
            img = file.read()

    return img


def check_environment(db):
    # check environment fucntions
    db.set_environment(ipv4='127.223.444.443', floor='1', width='3', height='4', depth='2')
    db.get_table(id='1', table='Environment')
    # db.delete_table(id='1', table='Environment')
    db.update_environment(id='1', ipv4='127.223.444.444')
    print('Environment table: ', db.list_table(table='Environment'))
    print('Environment table last id: ', db.last_id_table(table="Environment"))


def check_image(db):
    img_dir = 'img/example.png'
    if isinstance(img_dir, str):
        with open(img_dir, 'rb') as file:
            img = file.read()

    db.set_image(device_id='1', image=img, type='0', check_num='1')
    db.get_table(id='1', table='Image')
    # db.delete_table(id='1', table='Image')
    db.update_image(id='1', device_id='1')
    # print('Image table: ', db.list_table(table='Image'))
    print('Image table last id: ', db.last_id_table(table='Image'))


def check_grid(db):
    db.set_grid(width='3', height='4')
    db.get_table(id='1', table='Grid')
    # db.delete_table(id='1', table='Grid')
    db.update_grid(id='1', width='3')
    print('Grid table: ', db.list_table(table='Grid'))
    print('Grid table last id: ', db.last_id_table(table='Grid'))


def check_location(db):
    db.set_location(grid_id='1', x='3', y='4')
    db.get_table(id='1', table='Location')
    # db.delete_table(id='1', table='Location')
    db.update_location(id='1', x='3')
    print('Location table: ', db.list_table(table='Location'))
    print('Location table last id: ', db.last_id_table(table='Location'))


def check_supercategory(db):
    db.set_supercategory(name='hi')
    db.get_table(id='1', table='SuperCategory')
    # db.delete_table(id='1', table='SuperCategory')
    db.update_supercategory(id='1', name='hi')
    print('SuperCateogry table: ', db.list_table(table='SuperCategory'))
    print('SuperCategory table last id: ', db.last_id_table(table='SuperCategory'))


def check_category(db):
    img_dir = 'img/example.png'
    if isinstance(img_dir, str):
        with open(img_dir, 'rb') as file:
            img = file.read()

    db.set_category(super_id='1', name='hi', width='3', height='4', depth='10', iteration='1', thumbnail=img)
    db.get_table(id='1', table='Category')
    # db.delete_table(id='1', table='Category')
    db.update_category(id='1', name='hi')
    # print('Category table: ', db.list_table(table='Category'))
    print('Category table last id: ', db.last_id_table(table='Category'))


def check_object(db):
    db.set_object(img_id='1', loc_id='1', category_id='1', iteration=2)
    db.get_table(id='1', table='Object')
    # db.delete_table(id='1', table='Object')
    db.update_object(id='1', loc_id='1')
    print('Object table: ', db.list_table(table='Object'))
    print('Object table last id: ', db.last_id_table(table='Object'))


def check_bbox(db):
    db.set_bbox(obj_id='1', x='10', y='10', width='3', height='4')
    db.get_table(id='1', table='Bbox')
    # db.delete_table(id='1', table='Bbox')
    db.update_bbox(id='1', x='15')
    print('Bbox table: ', db.list_table(table='Bbox'))
    print('Bbox table last id: ', db.last_id_table(table='Bbox'))


def check_mask(db):
    db.set_mask(obj_id='1', x='20', y='20')
    db.get_table(id='1', table='Mask')
    # db.delete_table(id='1', table='Mask')
    db.update_mask(id='1', x='3333')
    print('Mask table: ', db.list_table(table='Mask'))
    print('Mask table last id: ', db.last_id_table(table='Mask'))


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


def get_environment_id(db, ipv4, floor):
    """
    Environment table (ipv4, floor)를 입력 받아
    Environment table의 (id)를 반환

    Args:
        db (DB class): DB class
        ipv4 (str): 냉장고 ipv4 정보
        floor (str): 냉장고 층 정보

    Return:
        env_id (int): Environment table id
        None: 조회 실패
    """
    env_id = db.get_env_id_from_args(ipv4=ipv4, floor=floor)
    return env_id


def get_grid_id(db, grid_w_h):
    """
    Grid table의 (width, height)를 입력 받아
    Grid table의 (id)를 반환하는 함수

    Args:
        db (DB class): DB class
        grid_w_h (str): Grid table의 width height 값 e.g. 3x4

    Return:
        grid_id (str): Grid table id
        None: 조회실패
    """
    w, h = grid_w_h.split('x')
    grid_id = db.get_grid_id_from_args(width=w, height=h)
    return grid_id


def get_supercategory_id(db, super_name):
    """
    SuperCategory table의 (name)을 입력 받아
    SuperCategory table의 (id) 반환하는 함수

    Args:
        db (DB class): DB class
        super_name (str): SuperCategory table의 name

    Return:
        super_id (int): SuperCategory table의 id
        None: 조회실패
    """
    super_id = db.get_supercategory_id_from_args(name=super_name)
    return super_id


def get_location_id(db, grid_w_h, loc_x_y):
    """
    Grid table의 (width, height)와 Location table의 (x, y)를 입력받아
    Location table의 (id) 반환하는 함수

    Args:
        db (DB class): DB class
        grid_w_h (str): Grid table의 width height 정보
        loc_x_y (str): Location table의 x, y 정보

    Return:
        loc_id (int): Location table의 id
        None: 조회실패
    """
    w, h = grid_w_h.split('x')
    grid_id = str(db.get_grid_id_from_args(width=w, height=h))
    if grid_id is None:
        return None

    x, y = loc_x_y.split('x')
    loc_id = db.get_location_id_from_args(grid_id=grid_id, x=x, y=y)
    return loc_id


def get_category_id(db, super_name, category_name):
    """
    SuperCateogry table의 (name)과 Category table의 (name)을 입력받아
    Category table의 (id) 반환하는 함수

    Args:
        db (DB class): DB class
        super_name (str): SuperCategory table의 name
        category_name (str): Category table의 name

    Return:
        category_id (int): Category table의 id
        None: 조회실패
    """
    super_id = str(db.get_supercategory_id_from_args(name=super_name))
    if super_id is None:
        return None

    category_id = db.get_category_id_from_args(super_id=super_id, category_name=category_name)
    return category_id


def get_image_check_num(db, obj_id):
    """
    Object table의 (id)를 입력 받아
    Image table의 (check_num) 반환하는 함수

    Args:
        db (DB class): DB class
        obj_id (str): Object table의 id

    Return:
        check_num (int): Image table의 check_num
        None: 조회 실패
    """
    img_id = str(db.get_img_id_from_args(obj_id=obj_id))
    if img_id is None:
        return None

    img_check_num = db.check_image_check_num(img_id=img_id)
    return img_check_num


def get_object_id(db, loc_id, category_id, iteration):
    """
    Object table의 (loc_id, category_id, iteration)를 입력 받아
    Object table (id) 반환하는 함수

    Args:
        db (DB): DB class
        loc_id (str): Location table의 id
        category_id (str): Category table의 id
        iteration (str): Object table의 iteration

    Return:
        obj_id (int): Object table의 id
        None: 조회 실패
    """

    obj_id = db.get_obj_id_from_args(loc_id=loc_id, category_id=category_id, iteration=iteration)
    return obj_id


def check_object_id(db, loc_id, category_id, iteration):
    """
    Object table의 (loc_id, category_id, iteration)를 입력 받아
    Object table의 특정 (id)를 check 하는 함수

       Args:
           db (DB): DB class
           loc_id (str): Location table의 id
           category_id (str): Category table의 id
           iteration (str): Object table의 iteration

       Return:
           Bool: True or False
       """
    obj_id = db.get_obj_id_from_args(loc_id=loc_id, category_id=category_id, iteration=iteration)
    if obj_id is not None:
        return True
    else:
        return False


def check_category_id(db, super_name, category_name):
    """
    SuperCateogry table의 (name)과 Category table의 (name)을 입력받아
    Category table의 특정 (id)가 존재하는지 check하는 함수


    Args:
        db (DB class): DB class
        super_name (str): SuperCategory table의 name
        category_name (str): Category table의 name

    Return:
        Bool: Category table에 해당 id가 존재하면 True or False
    """
    category_id = get_category_id(db=db, super_name=super_name, category_name=category_name)
    if category_id is not None:
        return True
    else:
        return False


def update_image_check_num(db, obj_id, check_num):
    """
    Object table의 (id)를 입력 받아
    Image table의 (check_num)을 update 하는 함수

    Args:
        db (DB class): DB class
        obj_id (str): Object table의 id
        check_num (str): Image table의 check_num

    Return:
        Bool: True or False
    """
    img_id = str(db.get_img_id_from_args(obj_id=obj_id))
    if img_id is None:
        return False

    flag = db.update_image_check_num(img_id=img_id, check_num=check_num)
    if flag is False:
        return False
    else:
        return True


def update_image_image(db, obj_id, img):
    """
    Object table의 (id)를 입력 받아
    Image table의 (image) update 하는 함수

    Args:
        db (DB class): DB class
        obj_id (str): Object table의 id
        img (Image): update image 정보

    Return:
        Bool: True or False
    """
    img_id = str(db.get_img_id_from_args(obj_id=obj_id))
    if img_id is None:
        return False

    flag = db.update_image_img(img_id=img_id, img=img)
    if flag is False:
        return False
    else:
        return True


def set_object_list(db, category_id, grid_id):
    """
    """


if __name__ == "__main__":
    img = img_loader('img/example.png')

    # cunnect to MYSQL Server
    mydb = DB(ip='192.168.10.69',
              port=3306,
              user='root',
              password='return123',
              db_name='test')

    # table 초기화
    mydb.init_table()

    # Environment table test
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

    a = get_environment_id(db=mydb, ipv4='127.223.444.444', floor='1')
    print('get_env_id: ', a)

    a_1 = get_grid_id(db=mydb, grid_w_h='3x4')
    print('get_grid_id: ', a_1)

    a_2 = get_supercategory_id(db=mydb, super_name='hi')
    print('get_supercategory_id: ', a_2)

    a_3 = get_location_id(db=mydb, grid_w_h='3x4', loc_x_y='3x4')
    print('get_location_id: ', a_3)

    a_4 = get_category_id(db=mydb, super_name='hi', category_name='hi')
    print('get_category_id: ', a_4)

    a_5 = check_category_id(db=mydb, super_name='hi', category_name='hi')
    print('check_category_id: ', a_5)

    a_6 = get_image_check_num(db=mydb, obj_id='1')
    print('get_image_check_num: ', a_6)

    a_7 = update_image_check_num(db=mydb, obj_id='1', check_num='100')
    print('update_image_check_num: ', a_7)

    read_img_from_db(db=mydb, img_id='1', table='Image')
    img_tmp = img_loader('img/puffine.jpg')
    a_8 = update_image_image(db=mydb, obj_id='1', img=img_tmp)
    print('update_image_image: ', a_8)
    read_img_from_db(db=mydb, img_id='1', table='Image')

    a_9 = get_object_id(db=mydb, loc_id='1', category_id='1', iteration='2')
    print(a_9)

    # reset tables
    # reset_table(mydb)