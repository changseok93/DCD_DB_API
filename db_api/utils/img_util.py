import cv2
import numpy as np
import inspect


def read_img_from_db(db, img_id, table):
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


def save_img(byte_img, img_dir):
    """
    DB에서 가져온 byte_img를 img_dir에 저장

    Args:
        byte_img (byte string): DB에서 가져온 byte img 정보(PNG 압축)
        img_dir (str): img를 저장할 directory

    Return:
        Bool: True or False
    """
    try:
        with open(img_dir, 'wb') as file:
            file.write(byte_img)
    except Exception as e:
        print('Error function:', inspect.stack()[0][3])
        print(e)
        return False
    else:
        return True


def img_loader(img_dir):
    if isinstance(img_dir, str):
        with open(img_dir, 'rb') as file:
            img = file.read()

    return img
