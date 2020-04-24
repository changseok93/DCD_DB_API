import DB
import os


def create_tables(db):
    db.table_initialize()


def check_environment():
    # check environment fucntions
    mydb.set_environment(ipv4='127.223.444.444', floor=2, width=2, height=3, depth=2)
    mydb.get_environment(id=1)
    mydb.delete_environment(id=1)
    mydb.update_environment(id=2, ipv4='127.223.444.444')
    print('Environment table:', mydb.list_environment())


def check_image():
    # 자료형이 이미지(longblob)일 경우엔 이미지 경로를 지정해줘야 합니다.
    # 예시에선 그냥 인트형으로 넣었는데 됨
    mydb.set_image(device_id=2, image=10, type=0, check_num=1)
    mydb.get_image(id=1)
    mydb.delete_image(id=1)
    mydb.update_image(id=2, device_id=5)
    print('Image table:', mydb.list_image())


def check_grid():
    mydb.set_grid(width=10, height=10)
    mydb.get_grid(id=1)
    mydb.delete_grid(id=1)
    mydb.update_grid(id=2, width=11)
    print('Grid table:', mydb.list_grid())


def check_location():
    mydb.set_location(grid_id=2, x=2, y=2)
    mydb.get_location(id=1)
    mydb.delete_location(id=1)
    mydb.update_location(id=2, x=22)
    print('Location table:', mydb.list_location())


def check_superCategory():
    mydb.set_superCategory(name='물병')
    mydb.get_superCategory(id=1)
    mydb.delete_superCategory(id=1)
    mydb.update_superCategory(id=2, name='물병2')
    print('SuperCateogry table:', mydb.list_superCategory())


def check_category():
    mydb.set_category(super_id=2, name='삼다수', width=10, height=10, depth=10, iteration=1, thumbnail=11)
    mydb.get_category(id=1)
    mydb.delete_category(id=1)
    mydb.update_category(id=2, name='삼다수2')
    print('Category table:', mydb.list_category())


def check_object():
    mydb.set_object(img_id=2, loc_id=2, category_id=2)
    mydb.get_object(id=1)
    mydb.delete_object(id=1)
    mydb.update_object(id=2, loc_id=2)
    print('Object table:', mydb.list_object())


def check_bbox():
    mydb.set_bbox(obj_id=2, x=10, y=10, width=1, height=1)
    mydb.get_bbox(id=1)
    mydb.delete_bbox(id=1)
    mydb.update_bbox(id=2, x=15)
    print('Bbox table:', mydb.list_bbox())


def check_mask():
    mydb.set_mask(obj_id=2, x=20, y=20)
    mydb.get_mask(id=1)
    mydb.delete_bbox(id=1)
    mydb.update_bbox(id=2, x=3333)
    print('Mask table:', mydb.list_mask())


if __name__ == "__main__":
    # cunnect to MYSQL Server
    mydb = DB.DB('192.168.10.69', 3306, 'root', 'return123', 'test')

    # 처음 test를 돌리기 위해선 테이블 생성 먼저 해야함
    create_tables(mydb)

    # Environment table test
    check_environment()

    # Image table test
    check_image()

    # Gird
    check_grid()

    # Location
    check_location()

    # Super Category
    check_superCategory()

    # Category
    check_category()

    # Object
    check_object()

    # Bbox
    check_bbox()

    # Mask
    check_mask()
