# -*- coding: utf-8 -*-
import pymysql
from db_api import querys
import inspect


class DB:
    """
    MySQL server와 정보를 주고받는 class 입니다.
    """
    def __init__(self, ip, port, user, password, db_name, charset='utf8mb4'):
        """
        DB class를 초기화하는 함수

        pymysql.connect()를 이용해 MySQL과 연결

        database 생성7
        mysql 서버의 변수 설정
            wait_timeout: 활동하지 않는 커넥션을 끊을때까지 서버가 대기하는 시간

            interactive_timeout: 활동중인 커넥션이 닫히기 전까지 서버가 대기하는 시간

            max_connections: 한번에 mysql 서버에 접속할 수 있는 클라이언트 수

        Args:
            ip (str): MySQL 서버에 로그인하기위한 ip 주소
            port (int): 포트 포워딩을 위한 포트
            user (str): MySQL 서버에 로그인을 위한 아이디
            password (str): MySQL 서버에 로그인을 위한 비밀번호
            db_name (str): 데이터베이스 네임
            charset (str): 문자 인코딩 방식

        Examples:

        .. code-block:: python

            mydb = DB(ip='192.168.10.69',
                      port=3306,
                      user='root',
                      password='return123',
                      db_name='test')
        """
        try:
            self.db = pymysql.connect(host=ip, port=port, user=user, passwd=password, charset=charset)
            print("setting on")

            with self.db.cursor() as cursor:
                query = 'CREATE DATABASE ' + db_name
                cursor.execute(query)

                query = 'SET GLOBAL wait_timeout=31536000'
                cursor.execute(query)

                query = 'SET GLOBAL interactive_timeout=31536000'
                cursor.execute(query)

                query = 'SET GLOBAL max_connections=100000'
                cursor.execute(query)

                query = 'SET GLOBAL max_connections=100000'
                cursor.execute(query)

                query = 'SET GLOBAL max_error_count=65535'
                cursor.execute(query)

                query = 'SET GLOBAL max_connect_errors=	4294967295'
                cursor.execute(query)

        except Exception as e:
            print('already init DB')
            print(e)

        finally:
            # select databases, 'use [database]'와 동일
            self.db.select_db(db_name)
            self.db.commit()

    def set_environment(self, ipv4, floor, width, height, depth):
        """
        Environment table에 row 추가

        Args:
            ipv4 (str): 연결된 냉장고의 ip
            floor (str) : 냉장고 층
            width (str): 냉장고 층 가로길이
            height (str): 냉장고 층 세로길이
            depth (str): 냉장고 층 높이

        Return:
            Bool: True or False

        Examples:

        .. code-block:: python

            db.set_environment(ipv4='127.223.444.443', floor='1', width='2', height='3', depth='2')
        """
        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO Environment(ipv4, floor, width, height, depth) VALUES(%s, %s, %s, %s, %s)'
                values = (ipv4, floor, width, height, depth)
                cursor.execute(query, values)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def update_environment(self, id, ipv4=None, floor=None, width=None, height=None, depth=None):
        """
        Enviroment table의 특정 id의 row 값 갱신

        Args:
            id (str): Enviroment table의 특정 id(primary key)
            ipv4 (str): 냉장고 ip 주소
            floor (str): 냉 장고 층
            width (str): 냉장고 층 가로 길이
            height (str): 냉장고 층 세로 길이
            depth (str): 냉장고 층 높이

        Return:
            Bool: True or False

        Examples:

        .. code-block:: python

            mydb.update_environment(id='1', ipv4='127.223.444.444')
        """
        try:
            with self.db.cursor() as cursor:
                query_head = 'UPDATE Environment SET '
                query_tail = ' WHERE id={}'.format(id)
                if ipv4 != None:
                    query_head += "ipv4='{}', ".format(ipv4)
                if floor != None:
                    query_head += 'floor={}, '.format(floor)
                if width != None:
                    query_head += 'width={}, '.format(width)
                if height != None:
                    query_head += 'height={}, '.format(height)
                if depth != None:
                    query_head += 'depth={}, '.format(depth)
                query = query_head[:-2]
                query += query_tail

                cursor.execute(query)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def set_image(self, device_id, image, type, check_num):
        """
        Image table에 row 추가

        Args:
            device_id (str): Environment table의 id(foreigner key)
            image (image): image data
            type (str): 합성된 이미지인지 아닌지
            check_num (str): 검수표시할 check 컬럼

        Return:
            Bool: True or False

        Example:

        .. code-block:: python

            mydb.set_image(device_id='1', image=img, type='0', check_num='1')
        """
        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO Image(env_id, data, type, check_num) VALUES(%s, %s, %s, %s)'
                values = (device_id, image, type, check_num)

                cursor.execute(query, values)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def update_image(self, id, device_id=None, image=None, type=None, check_num=None):
        """
        Image table의 특정 id의 row 값 갱신

        Args:
            id (str): Image table의 특정 id(primary key)
            device_id (str): Image table의 env_id(foreigner key)
            image (image): image 정보
            type (str): 합성된 이미지 인지 아닌지
            check_num (str): 검수표시할 check 컬럼

        Return:
            Bool: True or False

        Example:

        .. code-block:: python

            mydb.update_image(id='1', device_id='5')
        """
        try:
            with self.db.cursor() as cursor:
                query_head = 'UPDATE Image SET '
                query_tail = ' WHERE id={}'.format(id)
                if device_id != None:
                    query_head += 'env_id={}, '.format(device_id)
                if image != None:
                    query_head += "data=x'{}' , ".format(image.hex())
                if type != None:
                    query_head += 'type={}, '.format(type)
                if check_num != None:
                    check_num += 'check={}, '.format(check_num)

                query = query_head[:-2]
                query += query_tail
                cursor.execute(query)

                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def set_grid(self, width, height):
        """
        Grid table row 추가

        Args:
            width (str): grid 가로 칸 개수
            height (str): grid 세로 칸 개수

        Return:
            Bool: True or False

        Example:

        .. code-block:: python

            mydb.set_grid(width='3', height='3')

        """
        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO Grid(width, height) VALUES(%s, %s)'
                values = (width, height)
                cursor.execute(query, values)

                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def update_grid(self, id, width=None, height=None):
        """
        Grid table의 특정 id row 값 갱신

        Args:
            id (str): Grid table의 특정 id(primary key)
            width (str): grid 가로 칸 수
            height (str): grid 세로 칸 수

        Return:
            Bool: True or False

        Example:

        .. code-block:: python

            mydb.update_grid(id='1', width='11')
        """
        try:
            with self.db.cursor() as cursor:
                query_head = 'UPDATE Grid SET '
                query_tail = ' WHERE id={}'.format(id)
                if width != None:
                    query_head += 'width={}, '.format(width)
                if height != None:
                    query_head += 'height={}, '.format(height)
                query = query_head[:-2]
                query += query_tail
                cursor.execute(query)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def set_location(self, grid_id, x, y):
        """
        Location table에 row 추가

        Args:
            grid_id (str): Grid table의 id(foreigner key)
            x (str): 물체의 가로 좌표
            y (str): 물체의 세로 좌표

        Return:
            Bool: True or False

        Example:

        .. code-block:: python

            mydb.set_location(grid_id='1', x='2', y='2')
        """
        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO Location(grid_id, x, y) VALUES(%s, %s, %s)'
                values = (grid_id, x, y)
                cursor.execute(query, values)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def update_location(self, id, grid_id=None, x=None, y=None):
        """
        Location table의 특정 id 값 갱신

        Args:
            id (str): Location table의 특정 id(primary key)
            grid_id (str): Grid table의 특정 id(foreigner key)
            x (str): 물체의 x 좌표
            y (str): 물체의 y 좌표

        Return:
            Bool: True or False

        Example:

        .. code-block:: python

            mydb.update_location(id='1', x='22')
        """
        try:
            with self.db.cursor() as cursor:
                query_head = 'UPDATE Location SET '
                query_tail = ' WHERE id={}'.format(id)
                if grid_id != None:
                    query_head += 'Grid_id={}, '.format(grid_id)
                if x != None:
                    query_head += 'x={}, '.format(x)
                if y != None:
                    query_head += 'y={}, '.format(y)
                query = query_head[:-2]
                query += query_tail

                cursor.execute(query)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def set_supercategory(self, name):
        """
        SuperCategory table에 row 추가

        Arg:
            name (str): 물체의 이름(종류)

        Return:
            Bool: True or False

        Example:

        .. code-block:: python

            mydb.set_supercategory(name='hi4')
        """
        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO SuperCategory(name) VALUES(%s)'
                values = (name)
                cursor.execute(query, values)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def update_supercategory(self, id, name=None):
        """
        SuperCategory table의 특정 id의 row 값 갱신

        Args:
            id (str): SuperCategory table의 특정 id(primary key)
            name (str): 물체의 이름(종류)

        Return:
            Bool: True or False

        Example:

        .. code-block:: python

            mydb.update_supercategory(id='1', name='hi3')
        """
        try:
            with self.db.cursor() as cursor:
                query_head = 'UPDATE SuperCategory SET '
                query_tail = ' WHERE id={}'.format(id)
                if name != None:
                    query_head += "name='{}', ".format(name)
                query = query_head[:-2]
                query += query_tail
                cursor.execute(query)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def set_category(self, super_id, name, width, height, depth, iteration, thumbnail):
        """
        Category table에 row 추가

        Args:
            super_id (str): SuperCategory table의 특정 id(foreigner key)
            name (str): 물품의 이름
            width (str): 물체의 가로 크기
            height (str): 물체의 세로 크기
            depth (str): 물체의 높이
            iteration (str): 물체 촬영 횟수
            thumbnail (image): 썸네일 이미지

        Return:
            Bool: True or False

        Example:

        .. code-block:: python

            mydb.set_category(super_id='1', name='삼다수', width='10', height='10', depth='10', iteration='1', thumbnail=img)
        """
        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO Category(super_id, name, width, height, depth, iteration, thumbnail) VALUES(%s, %s, %s, %s, %s, %s, %s)'
                values = (super_id, name, width, height, depth, iteration, thumbnail)
                cursor.execute(query, values)

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)

        finally:
            self.db.commit()

    def update_category(self, id, super_id=None, name=None, width=None, height=None, depth=None, iteration=None, thumbnail=None):
        """
        Category table의 특정 id의 row 정보 갱신

        Args:
            id (str): Category table의 특정 id(primary key)
            super_id (str): superCategory의 id(foreigner key)
            name (str): 물품의 이름
            width (str): 물체의 가로 크기
            height (str): 물체의 세로 크기
            depth (str): 물체의 높이
            iteration (str): 물체 촬영 횟수
            thumbnail (image): 썸네일 이미지

        Return:
            Bool: True or False

        Example:

        .. code-block:: python

            mydb.update_category(id='1', name='삼다수2')
        """
        try:
            with self.db.cursor() as cursor:
                query_head = 'UPDATE Category SET '
                query_tail = ' WHERE id={}'.format(id)
                if super_id != None:
                    query_head += 'super_id={}, '.format(super_id)
                if name != None:
                    query_head += "name='{}', ".format(name)
                if width != None:
                    query_head += 'width={}, '.format(width)
                if height != None:
                    query_head += 'height={}, '.format(height)
                if depth != None:
                    query_head += 'depth={}, '.format(depth)
                if iteration != None:
                    query_head += 'iteration={}, '.format(iteration)
                if thumbnail != None:
                    query_head += "thumbnail=x'{}' , ".format(thumbnail.hex())

                query = query_head[:-2]
                query += query_tail
                cursor.execute(query)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def set_object(self, img_id, loc_id, category_id, iteration):
        """
        Object table에 row 추가

        Args:
            img_id (str or None): Image table의 id(foreigner key)
            loc_id (str): Location table의 id(foreigner key)
            category_id (str): Category table의 id(foreigner key)
            iteration (str): 물체를 방향 별로 찍어야하는 횟수

        Return:
            Bool: True or False

        Example:

        .. code-block:: python

            mydb.set_object(img_id='1', loc_id='1', category_id='1', iteration=2)
        """
        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO Object(img_id, loc_id, category_id, iteration) VALUES(%s, %s, %s, %s)'
                values = (img_id, loc_id, category_id, iteration)
                cursor.execute(query, values)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def update_object(self, id, img_id=None, loc_id=None, category_id=None, iteration=None):
        """
        Object table의 특정 id 정보 갱신

        Args:
            id (str): Object table의 특정 id(primary key)
            img_id (str or None): Image talbe의 특정 id(foreigner key)
            loc_id (str): Location table의 특정 id(foreigner key)
            category_id (str): Category table의 특정 id(foreigner key)
            iteration (str): 물체를 방향 별로 찍어야하는 횟수

        Return:
            Bool: True or False

        Example:

        .. code-block:: python

            mydb.update_object(id='1', loc_id='2')
        """
        try:
            with self.db.cursor() as cursor:
                query_head = 'UPDATE Object SET '
                query_tail = ' WHERE id={}'.format(id)
                if img_id != None:
                    query_head += 'img_id={}, '.format(img_id)
                if loc_id != None:
                    query_head += 'loc_id={}, '.format(loc_id)
                if category_id != None:
                    query_head += 'Category_id={}, '.format(category_id)
                if category_id != None:
                    query_head += 'Category_id={}, '.format(iteration)

                query = query_head[:-2]
                query += query_tail

                cursor.execute(query)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def set_bbox(self, obj_id, x, y, width, height):
        """
        Bbox table에 row 추가

        Args:
            obj_id (str): Object table의 id(foreigner key)
            x (str): Bbox의 왼쪽 시작 점 x 좌표
            y (str): Bbox의 왼쪽 시작 점 y 좌표
            width (str): Bbox의 가로 크기
            height (str): Bbox의 세로 크기

        Return:
            Bool: True or False

        Example:

        .. code-block:: python

            mydb.set_bbox(obj_id='1', x='10', y='10', width='1', height='1')
        """
        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO Bbox(obj_id, x, y, width, height) VALUES(%s, %s, %s, %s, %s)'
                values = (obj_id, x, y, width, height)
                cursor.execute(query, values)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def update_bbox(self, id, x=None, y=None, width=None, height=None):
        """
        Bbox table의 특정 id 정보 갱

        Args:
            id (str): Bbox table의 특정 id(primary key)
            x (str): Bbox의 왼쪽 시작점 x 좌표
            y (str): Bbox의 왼쪽 시작점 y 좌표
            width (str): Bbox의 가로 크기
            height (str): Bboxm의 세로 크기

        Return:
            Bool: True or False

        Example:

        .. code-block:: python

            mydb.update_bbox(id='1', x='15')
        """
        try:
            with self.db.cursor() as cursor:
                query_head = 'UPDATE Bbox SET '
                query_tail = ' WHERE id={}'.format(id)
                if x != None:
                    query_head += 'x={}, '.format(x)
                if y != None:
                    query_head += 'y={}, '.format(y)
                if width != None:
                    query_head += 'width={}, '.format(width)
                if height != None:
                    query_head += 'height={}, '.format(height)
                query = query_head[:-2]
                query += query_tail

                cursor.execute(query)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def set_mask(self, obj_id, x, y):
        """
        Mask table의 id row 추가

        Args:
            obj_id (str): Object table의 id(foreigner key)
            x: Mask 점의 x 좌표
            y: Mask 점의 y 좌표

        Return:
            Bool: True or False

        Example:

        .. code-block:: python

            mydb.set_mask(obj_id='1', x='20', y='20')
        """
        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO Mask(obj_id, x, y) VALUES(%s, %s, %s)'
                values = (obj_id, x, y)
                cursor.execute(query, values)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def update_mask(self, id, obj_id=None, x=None, y=None):
        """
        Mask table의 특정 id의 row 갱신

        Args:
            id: Mask table의 id(primary key)
            obj_id (str): Object table의 id(foreigner key)
            x: Mask 점의 x 좌표
            y: Mask 점의 y 좌표

        Return:
            Bool: True or False

        Example:

        .. code-block:: python

            mydb.update_mask(id='1', x='3333')
        """
        try:
            with self.db.cursor() as cursor:
                query_head = 'UPDATE Mask SET '
                query_tail = ' WHERE id={}'.format(id)
                if obj_id != None:
                    query_head += 'obj_id={}, '.format(obj_id)
                if x != None:
                    query_head += 'x={}, '.format(x)
                if y != None:
                    query_head += 'y={}, '.format(y)

                query = query_head[:-2]
                query += query_tail

                cursor.execute(query)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def get_table(self, id, table):
        """
        mysql databse에 있는 특정 table의 특정 id의 row를 가져옵니다.

        Args:
            id (str): table의 id 값
            table (str): 조회하기 원하는 table 이름

        Return:
            tuple(): 해당 id의 row 값

            None: 조회 실패

        Example:

        .. code-block:: python

            mydb.get_table(id='1', table='Bbox')
        """
        try:
            with self.db.cursor() as cursor:
                query = 'SELECT * FROM ' + table + ' WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return sum(cursor.fetchall(), ())

        except Exception as e:
            print('Error function:', inspect.stack()[0][3], '_', table)
            print(e)
            return None

    def delete_table(self, id, table):
        """
        mysql databse에 있는 특정 table의 특정 id의 row를 지웁니다..

        Args:
            id (str): table의 id 값
            table (str): 조회하기 원하는 table 이름

        Return:
            Bool: True or False

        Example:

        .. code-block:: python

            mydb.delete_table(id='1', table='Bbox')
        """
        try:
            with self.db.cursor() as cursor:
                query = 'DELETE FROM ' + table + ' WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3], table)
            print(e)
            return False

        finally:
            self.db.commit()

    def list_table(self, table):
        """
        mysql databse에 있는 특정 table의 모든 값을 가져옵니다.

        Args:
            table (str): 조회하기 원하는 table 이름

        Return:
            tuple()(): 특정 table의 모든 값

            None: 조회 실패

        Example:

        .. code-block:: python

            mydb.list_table(table='Mask')
        """
        try:
            with self.db.cursor() as cursor:
                query = 'SELECT * FROM ' + table
                cursor.execute(query)
                return cursor.fetchall()

        except Exception as e:
            print('Error function:', inspect.stack()[0][3], '_', table)
            print(e)
            return None

    def init_table(self):
        """
        table을 생성합니다.
        """
        try:
            with self.db.cursor() as cursor:
                for i, sql in enumerate(querys.initial_queries):
                    print('{} 번째 sql 실행중...'.format(i + 1))
                    cursor.execute(sql)

                cursor.execute("SHOW TABLES")
                for line in cursor.fetchall():
                    print(line)

        except Exception as e:
            print('table is already exist')
            print(e)

        finally:
            self.db.commit()

    def drop_table(self, table):
        """
        mysql databse에 있는 특정 table을 지웁니다.

        Args:
            table (str): 지우고자하는 table

        Return:
            Bool: True or False
        """
        try:
            with self.db.cursor() as cursor:
                query = 'DROP TABLE '
                query += table
                cursor.execute(query)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def get_last_id(self, table):
        """
        table의 마지막 id 조회

        Args:
            table (str): table 이름

        Return:
            list[][]: 마지막 id 값

            None: 조회 실패

        Example:

        .. code-block:: python

            mydb.last_id_table(table='Mask')
        """
        try:
            with self.db.cursor() as cursor:
                query = 'SELECT MAX(id) FROM ' + table
                cursor.execute(query)
                return list(cursor.fetchall())

        except Exception as e:
            print('Error function:', inspect.stack()[0][3], '_', table)
            print(e)
            return None

    def get_env_id_from_args(self, ipv4, floor):
        """
        Environment table의 id 반환

        Args:
            ipv4 (str): Environment table ipv4 정보
            floor (str): Environment table floor 정보

        Return:
            int: Environment table id

            None: 조회 실패

        Example:

        .. code-block:: python

            mydb.get_env_id_from_args(ipv4='127.223.444.443', floor='1')

        .. code-block:: sql

            SELECT * FROM Environment WHERE ipv4='123.123.12.12' AND floor=2
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT id FROM Environment WHERE ipv4='" + ipv4 + "' AND floor=" + floor
                cursor.execute(query)
                return sum(cursor.fetchall(), ())[0]

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return None

    def get_grid_id_from_args(self, width, height):
        """
        Grid table의 id 반환

        Args:
            width (str): gird 가로 칸 수
            height (str): grid 세로 칸 수

        Return:
            int: Grid table id

            None: 조회 실패

        Example:

        .. code-block:: python

            mydb.get_grid_id_from_args(width='3', height='3')

        .. code-block:: SQL

            SELECT id FROM Grid WHERE width=3 AND height=3
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT id FROM Grid WHERE width=" + width + " AND height=" + height
                cursor.execute(query)
                return sum(cursor.fetchall(), ())[0]

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return None

        finally:
            self.db.commit()

    def get_supercategory_id_from_args(self, name):
        """
        SuperCategory table의 id 반환

        Args:
            name (str): SuperCategory table의 name 정보

        Return:
            int: name에 해당하는 id

            None: 조회 실패

        Example:

        .. code-block:: python

            mydb.supercategory_id_from_args(name='스낵')

        .. code-block:: SQL

            SELECT id FROM SuperCategory WHERE name='스낵'
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT id FROM SuperCategory WHERE name='" + name + "'"
                cursor.execute(query)
                return sum(cursor.fetchall(), ())[0]

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return None

    def get_location_id_from_args(self, grid_id, x, y):
        """
        Location table의 id 반환

        Args:
            grid_id (str): grid_id 값(foreigner key)
            x (str): location table의 width 값
            y (str): location table의 height 값

        Return:
            int: 해당 location의 id

            None: 조회 실패

        Example:

        .. code-block:: python

            mydb.get_location_id_from_args(grid_id=grid_id, x='22', y='2')

        .. code-block:: SQL

            SELECT id FROM Lcation WHERE grid_id=1 AND x=22 AND y=2
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT id FROM Location WHERE grid_id=" + grid_id + " AND x=" + x + " AND y=" + y
                cursor.execute(query)
                return sum(cursor.fetchall(), ())[0]

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return None

    def get_category_id_from_args(self, super_id, category_name):
        """
        Category table의 id를 반환

        Args:
            super_id (str): 조회하기 원하는 category의 상위 super_category
            category_name (str): 조회하기 원하는 category의 name

        Return:
            int: 해당 category의 id

            None: 조회 실패

        Example:

        .. code-block:: python

            mydb.get_category_id_from_args(super_id=super_id, category_name='ee2')

        .. code-block:: SQL

            SELECT id FROM Category WHERE super_id=1 AND name='hi3'
        """
        try:
            with self.db.cursor() as cursor:
                query = 'SELECT id FROM Category WHERE super_id=' + super_id + " AND name='" + category_name + "'"
                cursor.execute(query)
                return sum(cursor.fetchall(), ())[0]

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return None

    def get_img_id_from_args(self, obj_id):
        """
        Object table의 img_id를 반환

        Args:
            obj_id (str): 조회하기 원하는 Object table의 id

        Return:
            int: 해당하는 Object table의 image id

            None: 조회 실패

        Example:

        .. code-block:: python

            mydb.check_img_check_num(img_id=img_id)

        .. code-block:: SQL

            SELECT img_id FROM Object WEHRE id=1
        """
        try:
            with self.db.cursor() as cursor:
                query = 'SELECT img_id FROM Object WHERE id=' + obj_id
                cursor.execute(query)
                return sum(cursor.fetchall(), ())[0]

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return None

    def get_obj_id_from_args(self, loc_id, category_id, iteration):
        """
        Object table의 id를 반환

        Args:
            loc_id (str): Object table의 loc_id
            category_id (str): Object table의 category_id
            iteration (str): Object table의 iteration

        Return:
            int: Object table의 id

            None: 조회 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT id FROM Object WHERE loc_id=%s AND category_id=%s AND iteration=%s"
                value = (loc_id, category_id, iteration)
                cursor.execute(query, value)
                return sum(cursor.fetchall(), ())[0]

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return None

    def check_image_check_num(self, img_id):
        """
        Image table의 이미지의 check_num을 반환

        Args:
            img_id (str): 조회하기 원하는 Object table의 id

        Return:
            int (0, 1, 2): 해당 object의 이미지 검수여부 반환

            None: 조회 실패

        Example:
        .. code-block:: python

            mydb.check_img_check_num(img_id=img_id)

        .. code-block:: SQL

            SELECT check_num FROM Image WHERE id=1
        """
        try:
            with self.db.cursor() as cursor:
                query = 'SELECT check_num FROM Image WHERE id=' + img_id
                cursor.execute(query)
                # print('function: {}, query: {}'.format(inspect.stack()[0][3], query))
                return sum(cursor.fetchall(), ())[0]

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return None

    def update_image_check_num(self, img_id, check_num):
        """
        Image table의 check_num 갱신

        Args:
            img_id (str): 수정하기 원하는 Object table의 id
            check_num (str): 수정하기 원하는 Image table의 check_num

        Return:
            Bool: True or False

        Example:

        .. code-block:: python

            mydb.update_img_check_num(img_id=img_id, check_num=check_num)

        .. code-block:: SQL

            UPDATE Image SET check_num=100 WHERE id=1
        """
        try:
            with self.db.cursor() as cursor:
                query = "UPDATE Image SET check_num=" + check_num + " WHERE id=" + img_id
                cursor.execute(query)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def update_image_img(self, img_id, img):
        """
        Image table의 image 갱신

        Args:
            img_id (str): Image table의 id
            img (Image): update할 image 데이터

        Return:
            Bool: True or False

        Example:

        .. code-block:: python

            db.update_image_img(img_id=img_id, img=img)

        .. code-block:: SQL

            UPDATE Image SET data=image WHERE id=1
        """
        try:
            with self.db.cursor() as cursor:
                query = "UPDATE Image SET data=%s WHERE id=%s"
                value = (img, img_id)
                cursor.execute(query, value)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def get_obj_from_args(self, category_id, loc_ids):
        """
        Object table의 (category_id, loc_ids)를 입력 받아
        해당되는 Object table의 row들을 반환하는 함수

        Args:
            category_id (str): Object table의 category_id
            loc_ids (tuple): Object table의 loc_id들

        Return:
            tuple()(): Location table의 id

            None: 조회 실패
        """
        try:
            with self.db.cursor() as cursor:
                query_head = 'SELECT img_id FROM Object WHERE (category_id=' + category_id + ') AND ('
                for loc_id in loc_ids:
                    query_head += 'loc_id={} OR '.format(loc_id[0])

                query = query_head[:-4] + ')'
                print(query)
                cursor.execute(query)
                # print('function: {}, query: {}'.format(inspect.stack()[0][3], query))

                return cursor.fetchall()

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return None

    def get_obj_from_img_id(self, img_id):
        """
        Object table의 (img_id)를 입력 받아
        Object table의 row를 반환하는 함수

        Args:
            img_id (str): Object table의 img_id

        Return:
            obj_id (str): Object table의 row
        """
        try:
            with self.db.cursor() as cursor:
                query = 'SELECT * FROM Object WHERE img_id=' + img_id
                cursor.execute(query)
                # print('function: {}, query: {}'.format(inspect.stack()[0][3], query))

                return cursor.fetchall()

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return None

    def get_location_from_grid_id(self, grid_id):
        """
        Location table의 (grid_id)를 입력 받아
        (grid_id)를 값으로 가지는 Location table의 모든 row의 개수 반환하는 함수

        Args:
            grid_id (str): Location table의 grid_id

        Return:
            tuple()(): Location table의 id

            None: 조회 실패

        """
        try:
            with self.db.cursor() as cursor:
                query = 'SELECT id FROM Location WHERE grid_id=' + grid_id
                # print('function: {}, query: {}'.format(inspect.stack()[0][3], query))
                cursor.execute(query)

                return cursor.fetchall()

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return None

    def bbox_info(self, object_id):
        """
        입력받은 object [id]를 가지는 Bbox table의
        [x, y, width, height]들을 2차원 리스트로 반환

        Args:
            object_id (str): 조회하기 원하는 Bbox table의 object id

        Return:
            tuple [][]: 입력받은 object [id]를 가지는
            Bbox table의 [x, y, width, height]값으로 이루어진
            2차원 튜플

            None: 조회 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT x, y, width, height from Bbox WHERE obj_id=" + object_id
                cursor.execute(query)

                return cursor.fetchall(), ()

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return None


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

    Example:

        .. code-block:: python

            get_environment_id(db=mydb, ipv4='127.223.444.444', floor='1')
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

    Example:

        .. code-block:: python

            get_grid_id(db=mydb, grid_w_h='3x4')

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

    Example:

        .. code-block:: python

            get_supercategory_id(db=mydb, super_name='hi')
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

    Example:

        .. code-block:: python

            get_location_id(db=mydb, grid_w_h='3x4', loc_x_y='3x4')

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

    Example:

        .. code-block:: python

            get_category_id(db=mydb, super_name='hi', category_name='hi')

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

    Example:

        .. code-block:: python

            get_image_check_num(db=mydb, obj_id='1')
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

    Example:

        .. code-block:: python

            get_object_id(db=mydb, loc_id='1', category_id='1', iteration='1')
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

    Example:

        .. code-block:: python

            check_object_id(db=mydb, loc_id='1', category_id='1', iteration='1')
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
        Bool: True or False

    Example:

        .. code-block:: python

            check_category_id(db=mydb, super_name='hi', category_name='hi')
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

    Example:

        .. code-block:: python

            update_image_check_num(db=mydb, obj_id='1', check_num='100')

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

    Example:

        .. code-block:: python

            update_image_image(db=mydb, obj_id='1', img=img_tmp)

    """
    img_id = str(db.get_img_id_from_args(obj_id=obj_id))
    if img_id is None:
        return False

    flag = db.update_image_img(img_id=img_id, img=img)
    if flag is False:
        return False
    else:
        return True


def set_object_list(db, category_id, grid_id, iterations):
    """
    Location table의 특정 (grid_id)를 가진 row와 Category table의 특정 (id)를 가진 row를 통해
    [Location table의 특정 grid_id를 가진 row 수 X category table의 특정 category_id를 가진 row 수]만큼
    Object table에 row 생성

    Args:
        db (DB): DB class
        category_id (str): Category table의 id
        grid_id (str): Location table의 grid_id
        iterations (list): Object table의 iteration

    Return:
        Bool: True or False

    Example:

        .. code-block:: python

            set_object_list(db=mydb, category_id='1', grid_id='1', iterations=['3', '4', '5'])
    """
    # 특정 grid_id에 해당하는 row만 조사
    loc_ids = db.get_location_from_grid_id(grid_id=grid_id)

    for loc_id in loc_ids:
        for iteration in iterations:
            # 초기화를 위해 NULL(None)을 넣어줌
            img_id = None
            loc_id = loc_id
            flag = db.set_object(img_id=img_id, loc_id=loc_id, category_id=category_id, iteration=iteration)
            if flag is False:
                return False

    return True


def list_object_check_num(db, category_id, grid_id, check_num_state):
    """
    Object table의 (category_id) Location table의 (grid_id)를 입력 받아
    Image table의 (check_num)이 check_state와 같으면 Object table의 row를 반환하는 함수

    Args:
        db (DB): DB class
        category_id (str): Object table의 (category_id)
        grid_id(str): Location table의 (grid_id)
        check_num_state(str): Image table의 (check_num) 값과 비교될 값
                          (0 : 검수 미진행, 1 : 완료, 2 : 거절)

    Return:
        tuple [object][row]: Object table의 row 값들

    Example:

        .. code-block:: python

            list_object_check_num(db=mydb, category_id='1', grid_id='2', check_num_state='100')
    """
    loc_ids = db.get_location_from_grid_id(grid_id=grid_id)
    img_ids = db.get_obj_from_args(category_id=category_id, loc_ids=loc_ids)

    print('loc_ids: ', loc_ids)
    print('img_ids: ', img_ids)
    obj_list = []
    for img_id in img_ids:
        img_id = str(img_id[0])
        img_check_num = db.check_image_check_num(img_id=img_id)
        if str(img_check_num) == check_num_state:
            obj = db.get_obj_from_img_id(img_id=img_id)
            obj_list.append(obj)

    return sum(obj_list, ())