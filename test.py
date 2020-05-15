import DB
import os


def create_tables(db):
    db.table_initialize()


def check_Environment(db):
    # check environment fucntions
    db.set_Environment(ipv4='127.223.444.444', floor='2', width='2', height='3', depth='2')
    db.get_table(id='2', table='Environment')
    db.delete_table(id='1', table='Environment')
    db.update_Environment(id='2', ipv4='127.223.444.444')
    print('Environment table: ', db.list_table(table='Environment'))
    print('Environment table last id: ', db.last_id_table(table="Environment"))


def check_Image(db):
    img_dir = './example.png'
    if isinstance(img_dir, str):
        with open(img_dir, 'rb') as file:
            img = file.read()

    db.set_Image(device_id='2', image=img, type='0', check_num='1')
    db.get_table(id='2', table='Image')
    db.delete_table(id='1', table='Image')
    db.update_Image(id='2', device_id='5')
    # print('Image table: ', db.list_table(table='Image'))
    print('Image table last id: ', db.last_id_table(table='Image'))


def check_Grid(db):
    db.set_Grid(width='10', height='10')
    db.get_table(id='2', table='Grid')
    db.delete_table(id='1', table='Grid')
    db.update_Grid(id='2', width='11')
    print('Grid table: ', db.list_table(table='Grid'))
    print('Grid table last id: ', db.last_id_table(table='Grid'))


def check_Location(db):
    db.set_Location(grid_id='2', x='2', y='2')
    db.get_table(id='2', table='Location')
    db.delete_table(id='1', table='Location')
    db.update_Location(id='2', x='22')
    print('Location table: ', db.list_table(table='Location'))
    print('Location table last id: ', db.last_id_table(table='Location'))


def check_SuperCategory(db):
    db.set_SuperCategory(name='물병')
    db.get_table(id='2', table='SuperCategory')
    db.delete_table(id='1', table='SuperCategory')
    db.update_SuperCategory(id='2', name='물병2')
    print('SuperCateogry table: ', db.list_table(table='SuperCategory'))
    print('SuperCategory table last id: ', db.last_id_table(table='SuperCategory'))


def check_Category(db):
    img_dir = './example.png'
    if isinstance(img_dir, str):
        with open(img_dir, 'rb') as file:
            img = file.read()

    db.set_Category(super_id='2', name='삼다수', width='10', height='10', depth='10', iteration='1', thumbnail=img)
    db.get_table(id='2', table='Category')
    db.delete_table(id='1', table='Category')
    db.update_Category(id='2', name='삼다수2')
    # print('Category table: ', db.list_table(table='Category'))
    print('Category table last id: ', db.last_id_table(table='Category'))


def check_Object(db):
    db.set_Object(img_id='2', loc_id='2', category_id='2')
    db.get_table(id='2', table='Object')
    db.delete_table(id='1', table='Object')
    db.update_Object(id='2', loc_id='2')
    print('Object table: ', db.list_table(table='Object'))
    print('Object table last id: ', db.last_id_table(table='Object'))


def check_Bbox(db):
    db.set_Bbox(obj_id='2', x='10', y='10', width='1', height='1')
    db.get_table(id='2', table='Bbox')
    db.delete_table(id='1', table='Bbox')
    db.update_Bbox(id='2', x='15')
    print('Bbox table: ', db.list_table(table='Bbox'))
    print('Bbox table last id: ', db.last_id_table(table='Bbox'))


def check_Mask(db):
    db.set_Mask(obj_id='2', x='20', y='20')
    db.get_table(id='2', table='Mask')
    db.delete_table(id='1', table='Mask')
    db.update_Bbox(id='2', x='3333')
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


def read_img_from_db(db):
    import cv2
    import numpy as np

    im = mydb.get_table(id='2', table='Image')
    img_byte_str = im[0][2]
    img_dir = './output.png'

    nparr = np.frombuffer(img_byte_str, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    cv2.imshow('d', img_np)
    cv2.waitKey(0)

    # byte 타입으로 저장도 가능
    # cv2를 굳이 안써도 되지만, cv2.imshow 불가
    with open(img_dir, 'wb') as file:
        file.write(img_byte_str)


if __name__ == "__main__":
    # cunnect to MYSQL Server
    mydb = DB.DB('192.168.10.69', 3306, 'root', 'return123', 'test')
    # 처음 test를 돌리기 위해선 테이블 생성 먼저 해야함
    try:
        create_tables(mydb)
    except:
        print("db가 이미 생성됨")

    # reset_table(mydb)

    # Environment table test
    check_Environment(mydb)

    # Image table test
    check_Image(mydb)

    # Gird
    check_Grid(mydb)

    # Location
    check_Location(mydb)

    # Super Category
    check_SuperCategory(mydb)

    # Category
    check_Category(mydb)

    # Object
    check_Object(mydb)

    # Bbox
    check_Bbox(mydb)

    # Mask
    check_Mask(mydb)

    # db로 부터 이미지 정보를 가져와 읽는 예
    read_img_from_db(mydb)

    # reset tables
    # reset_table(mydb)