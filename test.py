import DB
import os


def create_tables(db):
    db.table_initialize()


def check_environment(db):
    # check environment fucntions
    db.set_environment(ipv4='127.223.444.444', floor=2, width=2, height=3, depth=2)
    db.get_environment(id=1)
    db.delete_environment(id=1)
    db.update_environment(id=2, ipv4='127.223.444.444')
    print('Environment table:', db.list_environment())


def check_image(db):
    db.set_image(device_id=2, image=10, type=0, check_num=1)
    db.get_image(id=1)
    db.delete_image(id=1)
    db.update_image(id=2, device_id=5)
    print('Image table:', db.list_image())


def check_grid(db):
    db.set_grid(width=10, height=10)
    db.get_grid(id=1)
    db.delete_grid(id=1)
    db.update_grid(id=2, width=11)
    print('Grid table:', db.list_grid())


def check_location(db):
    db.set_location(grid_id=2, x=2, y=2)
    db.get_location(id=1)
    db.delete_location(id=1)
    db.update_location(id=2, x=22)
    print('Location table:', db.list_location())


def check_superCategory(db):
    db.set_superCategory(name='물병')
    db.get_superCategory(id=1)
    db.delete_superCategory(id=1)
    db.update_superCategory(id=2, name='물병2')
    print('SuperCateogry table:', db.list_superCategory())


def check_category(db):
    db.set_category(super_id=2, name='삼다수', width=10, height=10, depth=10, iteration=1, thumbnail=11)
    db.get_category(id=1)
    db.delete_category(id=1)
    db.update_category(id=2, name='삼다수2')
    print('Category table:', db.list_category())


def check_object(db):
    db.set_object(img_id=2, loc_id=2, category_id=2)
    db.get_object(id=1)
    db.delete_object(id=1)
    db.update_object(id=2, loc_id=2)
    print('Object table:', db.list_object())


def check_bbox(db):
    db.set_bbox(obj_id=2, x=10, y=10, width=1, height=1)
    db.get_bbox(id=1)
    db.delete_bbox(id=1)
    db.update_bbox(id=2, x=15)
    print('Bbox table:', db.list_bbox())


def check_mask(db):
    db.set_mask(obj_id=2, x=20, y=20)
    db.get_mask(id=1)
    db.delete_bbox(id=1)
    db.update_bbox(id=2, x=3333)
    print('Mask table:', db.list_mask())


def reset_table(db):
    db.drop_table('Bbox')
    db.drop_table('Mask')
    db.drop_table('Object')
    db.drop_table('Image')
    db.drop_table('Location')
    db.drop_table('Category')
    db.drop_table('Environment')
    db.drop_table('Grid')
    db.drop_table('SuperCategory')


if __name__ == "__main__":
    # cunnect to MYSQL Server
    mydb = DB.DB('192.168.10.69', 3306, 'root', 'return123', 'test')

    # 처음 test를 돌리기 위해선 테이블 생성 먼저 해야함
    try:
        create_tables(mydb)
    except:
        print("db가 이미 생성됨")

    # Environment table test
    check_environment(mydb)

    # Image table test
    check_image(mydb)

    # Gird
    check_grid(mydb)

    # Location
    check_location(mydb)

    # Super Category
    check_superCategory(mydb)

    # Category
    check_category(mydb)

    # Object
    check_object(mydb)

    # Bbox
    check_bbox(mydb)

    # Mask
    check_mask(mydb)

    # reset tables
    # reset_table(mydb)
