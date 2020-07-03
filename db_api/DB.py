# -*- coding: utf-8 -*-
from db_api import querys
import pymysql
import inspect


class DB():
    """
    MySQL server와 정보를 주고받는 class 입니다.
    """
    def __init__(self, ip, port, user, password, db_name, charset='utf8mb4'):
        """
        DB class를 초기화하는 함수

        pymysql.connect()를 이용해 MySQL과 연결

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

    def set_environment(self, ipv4, floor, width, height, depth) -> bool:
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

    def update_environment(self, id, ipv4=None, floor=None, width=None, height=None, depth=None) -> bool:
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

    def set_image(self, device_id, image, type, check_num) -> bool:
        """
        Image table에 row 추가

        Args:
            device_id (str): Environment table의 id(foreigner key)
            image (image): image data
            type (str): 합성된 이미지인지 아닌지
            check_num (str): 검수표시할 check 컬럼

        Return:
            Bool: True or False
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

    def update_image(self, id, device_id=None, image=None, type=None, check_num=None) -> bool:
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

    def set_grid(self, width, height) -> bool:
        """
        Grid table row 추가

        Args:
            width (str): grid 가로 칸 개수
            height (str): grid 세로 칸 개수

        Return:
            Bool: True or False
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

    def update_grid(self, id, width=None, height=None) -> bool:
        """
        Grid table의 특정 id row 값 갱신

        Args:
            id (str): Grid table의 특정 id(primary key)
            width (str): grid 가로 칸 수
            height (str): grid 세로 칸 수

        Return:
            Bool: True or False
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

    def set_location(self, grid_id, x, y) -> bool:
        """
        Location table에 row 추가

        Args:
            grid_id (str): Grid table의 id(foreigner key)
            x (str): 물체의 가로 좌표
            y (str): 물체의 세로 좌표

        Return:
            Bool: True or False
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

    def update_location(self, id, grid_id=None, x=None, y=None) -> bool:
        """
        Location table의 특정 id 값 갱신

        Args:
            id (str): Location table의 특정 id(primary key)
            grid_id (str): Grid table의 특정 id(foreigner key)
            x (str): 물체의 x 좌표
            y (str): 물체의 y 좌표

        Return:
            Bool: True or False
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

    def set_supercategory(self, name) -> bool:
        """
        SuperCategory table에 row 추가

        Arg:
            name (str): 물체의 이름(종류)

        Return:
            Bool: True or False
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

    def update_supercategory(self, id, name=None) -> bool:
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

    def set_category(self, super_id, name, width, height, depth, iteration, thumbnail) -> bool:
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

    def update_category(self, id, super_id=None, name=None, width=None,
                        height=None, depth=None, iteration=None, thumbnail=None) -> bool:
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

    def set_object(self, img_id, loc_id, category_id, iteration, mix_num) -> bool:
        """
        Object table에 row 추가

        Args:
            img_id (str or None): Image table의 id(foreigner key)
            loc_id (str): Location table의 id(foreigner key)
            category_id (str): Category table의 id(foreigner key)
            iteration (str): 물체를 방향 별로 찍어야하는 횟수
            mix_num (str): mix 이미지에 대한 정보

        Return:
            Bool: True or False
        """
        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO Object(img_id, loc_id, category_id, iteration, mix_num) VALUES(%s, %s, %s, %s, %s)'
                values = (img_id, loc_id, category_id, iteration, mix_num)
                cursor.execute(query, values)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def update_object(self, id, img_id=None, loc_id=None, category_id=None, iteration=None, mix_num=None) -> bool:
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
                    query_head += 'iteration={}, '.format(iteration)
                if mix_num != None:
                    query_head += 'mix_num={}, '.format(mix_num)

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

    def set_bbox(self, obj_id, x, y, width, height) -> bool:
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

    def update_bbox(self, id, x=None, y=None, width=None, height=None) -> bool:
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

    def set_mask(self, obj_id, x, y) -> bool:
        """
        Mask table의 id row 추가

        Args:
            obj_id (str): Object table의 id(foreigner key)
            x: Mask 점의 x 좌표
            y: Mask 점의 y 좌표

        Return:
            Bool: True or False
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

    def update_mask(self, id, obj_id=None, x=None, y=None) -> bool:
        """
        Mask table의 특정 id의 row 갱신

        Args:
            id: Mask table의 id(primary key)
            obj_id (str): Object table의 id(foreigner key)
            x: Mask 점의 x 좌표
            y: Mask 점의 y 좌표

        Return:
            Bool: True or False
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
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = 'SELECT * FROM ' + table + ' WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                v = sum(cursor.fetchall(), ())
                if v:
                    return v
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3], '_', table)
            print(e)
            return False

    def delete_table(self, id, table) -> bool:
        """
        mysql databse에 있는 특정 table의 특정 id의 row를 지웁니다..

        Args:
            id (str): table의 id 값
            table (str): 조회하기 원하는 table 이름

        Return:
            Bool: True or False
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
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = 'SELECT * FROM ' + table
                cursor.execute(query)
                v = cursor.fetchall()
                if v:
                    return v
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3], '_', table)
            print(e)
            return False

    def init_table(self) -> bool:
        """
        table을 생성합니다.

        Return:
            Bool: True or False
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
            return False

        finally:
            self.db.commit()
            return True

    def drop_table(self, table) -> bool:
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
            int: 마지막 id 값
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = 'SELECT MAX(id) FROM ' + table
                cursor.execute(query)
                v = sum(cursor.fetchall(), ())
                if v:
                    return v[0]
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3], '_', table)
            print(e)
            return False

    def get_env_id(self, ipv4, floor):
        """
        Environment table의 id 반환

        Args:
            ipv4 (str): Environment table ipv4 정보
            floor (str): Environment table floor 정보

        Return:
            int: Environment table (id)
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT id FROM Environment WHERE ipv4='" + ipv4 + "' AND floor=" + floor
                cursor.execute(query)
                v = sum(cursor.fetchall(), ())
                if v:
                    return v[0]
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def get_grid_id(self, grid_w_h):
        """
        Grid table의 (id) 반환

        Args:
            grid_w_h (str): Grid table의 (width), (height)

        Return:
            tuple (): Grid table (id)
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            w, h = grid_w_h.split('x')
            with self.db.cursor() as cursor:
                query = "SELECT id FROM Grid WHERE width=" + w + " AND height=" + h
                cursor.execute(query)
                v = sum(cursor.fetchall(), ())
                if v:
                    return v
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return None

    def get_supercategory_id(self, name):
        """
        SuperCategory table의 id 반환

        Args:
            name (str): SuperCategory table의 name 정보

        Return:
            tuple (): SuperCategory table의 name에 해당하는 (id)
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT id FROM SuperCategory WHERE name='" + name + "'"
                cursor.execute(query)
                v = sum(cursor.fetchall(), ())
                if v:
                    return v
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def get_loc_id(self, grid_id, loc_x_y):
        """
        Location table의 id 반환

        Args:
            grid_id (str): Grid table의 (grid_id)
            loc_x_y (str): Location table의 (x), (y)

        Return:
            int: 해당 location의 id
            None: 값 없음
            False: 쿼리 실패
        """
        x, y = loc_x_y.split('x')
        try:
            with self.db.cursor() as cursor:
                query = "SELECT id FROM Location WHERE grid_id=" + grid_id + " AND x=" + x + " AND y=" + y
                cursor.execute(query)
                v = sum(cursor.fetchall(), ())
                if v:
                    return v[0]
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def get_loc_id_GL(self, grid_w_h, loc_x_y):
        """
        Grid table의 (width, height)와 Location table의 (x, y)를 입력받아
        Location table의 (id) 반환하는 함수

        Args:
            grid_w_h (str): Grid table의 width height 정보
            loc_x_y (str): Location table의 x, y 정보

        Return:
            tuple (): Location table의 id
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            w, h = grid_w_h.split('x')
            x, y = loc_x_y.split('x')
            with self.db.cursor() as cursor:
                query = "SELECT id FROM Location WHERE x=%s AND y=%s " \
                        "AND grid_id=(SELECT id FROM Grid WHERE width=%s AND height=%s)"
                value = (x, y, w, h)
                cursor.execute(query, value)
                v = sum(cursor.fetchall(), ())
                if v:
                    return v
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def get_category_id(self, super_id, category_name):
        """
        Category table의 id를 반환

        Args:
            super_id (str): 조회하기 원하는 category의 상위 super_category
            category_name (str): 조회하기 원하는 category의 name

        Return:
            int: 해당 category의 id
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = 'SELECT id FROM Category WHERE super_id=' + super_id + " AND name='" + category_name + "'"
                cursor.execute(query)
                v = sum(cursor.fetchall(), ())
                if v:
                    return v[0]
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def get_category_id_obj(self, obj_id):
        """
        Object table의 (obj_id)를 받아 (category_id)를 얻음

        Args:
            obj_id (str): Object table의 id

        Return:
            int: (category_id)
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT category_id FROM Object WHERE id=" + obj_id
                cursor.execute(query)
                v = sum(cursor.fetchall(), ())
                if v:
                    return v[0]
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def get_img_id(self, obj_id):
        """
        Object table의 img_id를 반환

        Args:
            obj_id (str): 조회하기 원하는 Object table의 id

        Return:
            int: 해당하는 Object table의 image id
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = 'SELECT img_id FROM Object WHERE id=' + obj_id
                cursor.execute(query)
                v = sum(cursor.fetchall(), ())
                if v:
                    return v[0]
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def get_location(self, grid_id):
        """
        Location table의 (grid_id)를 입력 받아
        (grid_id)를 값으로 가지는 Location table의 row 반환 함수

        Args:
            grid_id (str): Location table의 grid_id

        Return:
            tuple()(): Location table의 id
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = 'SELECT id FROM Location WHERE grid_id=' + grid_id
                cursor.execute(query)
                v = cursor.fetchall()
                if v:
                    return v
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def get_bbox_info(self, object_id):
        """
        입력받은 object [id]를 가지는 Bbox table의
        [x, y, width, height]들을 2차원 리스트로 반환

        Args:
            object_id (str): 조회하기 원하는 Bbox table의 object id

        Return:
            tuple ()(): 입력받은 object [id]를 가지는 Bbox table의 [x, y, width, height]값으로 이루어진 2차원 튜플
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT x, y, width, height from Bbox WHERE obj_id=" + object_id
                cursor.execute(query)
                v = cursor.fetchall()
                if v:
                    return v
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def get_obj_id_img(self, img_id):
        """
        Object table의 (img_id)를 받아 (obj_id)들을 얻음

        Args:
            img_id (str): Object table의 (img_id)

        Return:
            tuple (): (obj_id) 정보들
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT id FROM Object WHERE img_id=" + img_id
                cursor.execute(query)
                v = sum(cursor.fetchall(), ())
                if v:
                    return v
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def get_obj_id(self, category_id):
        """
        Object table의 (category id)를 입력 받아
        Object table의 (obj id)들 반환

        Args:
            category_id (str): Object table의 (category id)

        Return:
            tuple () : Object_table의 (obj id) 값들
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT id FROM Object WHERE category_id=" + category_id + " AND mix_num=" + "-1"
                cursor.execute(query)
                v = sum(cursor.fetchall(), ())
                if v:
                    return v
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def get_super_id(self, category_id):
        """
        Category table의 (id)를 받아
        Category table의 (super_id)를 반환

        Args:
            category_id (str): Category table의 id

        Return:
            int: (super_id)
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT super_id FROM Category WHERE id=" + category_id
                cursor.execute(query)
                v = sum(cursor.fetchall(), ())
                if v:
                    return v[0]
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def get_super_name(self, super_id):
        """
        SuperCategory table의 (id)를 받아
        SuperCategory table의 (name)을 반환함

        Args:
            super_id (str): SuperCategory table의 (id)

        Return:
            int: (name)
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT name FROM SuperCategory WHERE id=" + super_id
                cursor.execute(query)
                v = sum(cursor.fetchall(), ())
                if v:
                    return v[0]
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def get_mix_num(self, loc_id, category_id, iteration):
        """
        Object table의 (loc_id, category_id, iteration)를 입력받아
        Object table의 가장 큰 mix_num을 가진 (mix_num) 반환

        Args:
            loc_id (str): Object table의 (loc_id)
            category_id (str): Object table의 (category_id)
            iteration (str): Object table의 (iteration)

        Return:
            tuple () : Object_table의 (mix_num) 값들
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT mix_num FROM Object WHERE loc_id=%s AND category_id=%s AND iteration=%s"
                value = (loc_id, category_id, iteration)
                cursor.execute(query, value)
                mix_nums = sum(cursor.fetchall(), ())
                if mix_nums:
                    return None

                return sorted(mix_nums, reverse=True)[0]

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def get_bbox_id(self, obj_id):
        """
        Object table의 (id)를 받아
        Bbox table의 (id) 반환

        Args:
            obj_id (str): Object table의 (id)

        Return:
            tuple (): Bbox table의 (id)
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT id FROM Bbox WHERE obj_id=" + obj_id
                cursor.execute(query)
                v = sum(cursor.fetchall(), ())
                if v:
                    return v
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def get_mask_id(self, obj_id):
        """
        Object table의 (id)를 받아
        Mask table의 (id) 반환

        Args:
            object_id (str): Object table의 (id)

        Return:
            tuple (): Mask table의 (id)
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT id FROM Mask WHERE obj_id=" + obj_id
                cursor.execute(query)
                v = sum(cursor.fetchall(), ())
                if v:
                    return v
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def get_img_check_num(self, obj_id):
        """
        Object table의 (id)를 입력 받아
        Image table의 (check_num) 반환

        Args:
            obj_id (str): Object table의 id

        Return:
            check_num (int): Image table의 check_num
            None: 조회 실패
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT check_num FROM Image WHERE id=(SELECT img_id FROM Object WHERE id=%s)"
                value = (obj_id)
                cursor.execute(query, value)
                v = sum(cursor.fetchall(), ())
                if v:
                    return v[0]
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def get_bbox_img(self, img_id):
        """
        Object table의 (img_id)를 받아 (obj_id)들을 가져옴
        얻은 (obj_id)들로 Bbox table의 row들을 조회

        Args:
            img_id (str): Object table의 (img_id)

        Return:
            tuple ()(): Bbox table의 row
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT * FROM Bbox " \
                        "WHERE obj_id IN (SELECT id FROM Object WHERE img_id=%s)"
                value = (img_id)
                cursor.execute(query, value)
                v = cursor.fetchall()
                if v:
                    return v
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def get_cat_id(self, super_name, cat_name):
        """
        SuperCateogry table의 (name)과 Category table의 (name)을 받아
        Category table의 (id) 반환

        Args:
            super_name (str): SuperCategory table의 (name)
            cat_name (str): Category table의 (name)

        Return:
            category_id (int): Category table의 (id)
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT id FROM Category WHERE name=%s AND " \
                        "super_id=(SELECT id FROM SuperCategory WHERE name=%s)"
                value = (super_name, cat_name)
                cursor.execute(query, value)
                v = sum(cursor.fetchall(), ())
                if v:
                    return v[0]
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def list_bbox(self, obj_id):
        """
        Bbox table의 (obj_id)를 이용해
        Bbox table의 모든 row 반환

        Args:
            obj_id (str): Bbox table의 obj_id

        Return:
            tuple()(): Bbox table의 row
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = 'SELECT * FROM Bbox WHERE obj_id=' + obj_id
                cursor.execute(query)
                v = cursor.fetchall()
                if v:
                    return v
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def list_obj(self, category_id, loc_ids):
        """
        Object table의 (category_id, loc_ids)를 입력 받아
        해당되는 Object table의 row들을 반환하는 함수

        Args:
            category_id (str): Object table의 category_id
            loc_ids (tuple): Object table의 loc_id들

        Return:
            tuple()(): Location table의 id
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query_head = 'SELECT img_id FROM Object WHERE (category_id=' + category_id + ') AND ('
                for loc_id in loc_ids:
                    query_head += 'loc_id={} OR '.format(loc_id[0])

                query = query_head[:-4] + ')'
                cursor.execute(query)
                # print('function: {}, query: {}'.format(inspect.stack()[0][3], query))
                v = cursor.fetchall()
                if v:
                    return v
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def check_image_check_num(self, img_id):
        """
        Image table의 이미지의 check_num을 반환

        Args:
            img_id (str): 조회하기 원하는 Object table의 id

        Return:
            int (0, 1, 2): 해당 object의 이미지 검수여부 반환
            None: 값 없음
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = 'SELECT check_num FROM Image WHERE id=' + img_id
                cursor.execute(query)
                v = sum(cursor.fetchall(), ())
                if v:
                    return v[0]
                else:
                    return None

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def check_obj_id(self, loc_id, category_id, iteration, mix_num) -> bool:
        """
        Object table의 (loc_id, category_id, iteration)를 입력 받아
        Object table의 특정 (id)를 check 하는 함수

        Args:
            loc_id (str): Object table의 loc_id
            category_id (str): Object table의 category_id
            iteration (str): Object table의 iteration
            mix_num (str): Object table의 mix_num

        Return:
            Bool: True or False
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT id FROM Object WHERE loc_id=%s AND category_id=%s AND iteration=%s AND mix_num=%s"
                value = (loc_id, category_id, iteration, mix_num)
                cursor.execute(query, value)
                obj_id = sum(cursor.fetchall(), ())
                if obj_id:
                    return True
                else:
                    return False

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def check_process(self, category_id) -> bool:
        """
        Object table의 (category_id)가 입력받은 값을 가지고 (mix_num)이 -1인 Object table의 row가 존재하고
        해당하는 모든 Object table의 row에 대한 Bbox table의 row와 Mask table의 row가 둘다 존재할 경우 True 반환
        이외의 경우 False 반환
        Args:
            category_id (str): Object table의 (category_id)

        Return:
            Bool: True or False
        """
        try:
            with self.db.cursor() as cursor:
                # Bbox query
                category_id = int(category_id)
                query = "SELECT id FROM Bbox " \
                        "WHERE obj_id IN (SELECT id FROM Object WHERE category_id=%s AND mix_num=-1)"
                value = (category_id)
                cursor.execute(query, value)
                bbox_ids = cursor.fetchall()

                # Mask query
                query = "SELECT id FROM Mask " \
                        "WHERE obj_id IN (SELECT id FROM Object WHERE category_id=%s AND mix_num=-1)"
                value = (category_id)
                cursor.execute(query, value)
                mask_ids = cursor.fetchall()

                if bbox_ids and mask_ids:
                    return True
                else:
                    return False

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def check_cat_id(self, super_name, cat_name) -> bool:
        """
        SuperCateogry table의 (name)과 Category table의 (name)을 입력받아
        Category table의 특정 (id)가 존재하는지 check하는 함수

        Args:
            super_name (str): SuperCategory table의 name
            cat_name (str): Category table의 name

        Return:
            Bool: True or False
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT id FROM Category WHERE name=%s AND " \
                        "super_id IN (SELECT id FROM SuperCategory WHERE name=%s)"
                value = (super_name, cat_name)
                cursor.execute(query, value)
                v = sum(cursor.fetchall(), ())
                if v:
                    return True
                else:
                    return False

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def update_img_check_num_obj_id(self, obj_id, check_num):
        """
        Object table의 (id)를 입력 받아
        Image table의 (check_num)을 update 하는 함수

        Args:
            obj_id (str): Object table의 id
            check_num (str): Image table의 check_num

        Return:
            True: 갱신 성공
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "UPDATE Image SET check_num=%s " \
                        "WHERE id=(SELECT img_id FROM Object WHERE id=%s)"
                value = (check_num, obj_id)
                cursor.execute(query, value)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def update_img_check_num_img_id(self, img_id, check_num):
        """
        Image table의 check_num 갱신

        Args:
            img_id (str): 수정하기 원하는 Object table의 id
            check_num (str): 수정하기 원하는 Image table의 check_num

        Return:
            True: 갱신 성공
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "UPDATE Image SET check_num=%s WHERE id=%s"
                value = (check_num, img_id)
                cursor.execute(query, value)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def update_img_img_obj_id(self, obj_id, img):
        """
        Object table의 (id)를 입력 받아
        Image table의 (data) update 하는 함수

        Args:
            obj_id (str): Object table의 id
            img (Image): update image 정보

        Return:
            True: 갱신 성공
            False: 쿼리 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "UPDATE Image SET data=%s" \
                        "WHERE id=(SELECT img_id FROM Object WHERE id=%s)"
                value = (img, obj_id)
                cursor.execute(query, value)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def update_img_img_img_id(self, img_id, img):
        """
        Image table의 (data) update

        Args:
            img_id (str): Image table의 (id)
            img (Image): Image table의 (data)

        Return:
            True: 갱신 성공
            False: 쿼리 실패
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

    def delete_object(self, img_id) -> bool:
        """
        Object table의 (img_id)를 받아
        해당하는 Object table의 모든 row를 삭제

        Args:
            img_id (str): Object table의 (img_id)

        Return:
            Bool: True or False
        """
        try:
            with self.db.cursor() as cursor:
                query = 'DELETE FROM Object WHERE img_id=' + img_id
                cursor.execute(query)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def delete_bbox(self, obj_id) -> bool:
        """
        Bbox table의 [object_id]를 가지는 모든 row 삭제

        Args:
            obj_id (str): Bbox table의 object_id

        Return:
            Bool: True or False
        """
        try:
            with self.db.cursor() as cursor:
                query = 'DELETE FROM Bbox WHERE obj_id=' + obj_id
                cursor.execute(query)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def delete_mask(self, obj_id) -> bool:
        """
        Mask table의 (object_id)를 가지는 모든 row 삭제

        Args:
            obj_id (str): Mask table의 (object_id)

        Return:
            Bool: True or False
        """
        try:
            with self.db.cursor() as cursor:
                query = 'DELETE FROM Mask WHERE obj_id=' + obj_id
                cursor.execute(query)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()

    def delete_bbox_img(self, img_id) -> bool:
        """
        Object table의 (img_id)를 통해 Object table의 (id)를 가져옴
        이를통해 관계된 Bbox table의 (obj_id)를 가지는 모든 bbox 삭제

        Args:
            img_id (str): Object table의 img_id

        Return:
            Bool: True or False
        """
        try:
            with self.db.cursor() as cursor:
                query = "DELETE FROM Bbox WHERE " \
                        "obj_id IN (SELECT id FROM Object WHERE img_id=%s)"
                value = (img_id)
                cursor.execute(query, value)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()


#-------------------------------수정 필요-----------------------------------
    def delete_nomix_img(self, img_id) -> bool:
        """
        Object table의 (img_id)를 받아
        SuperCategory table의 (name)이 mix가 아닌 Object table의 (row) 삭제

        Args:
            img_id (str): Object table의 (img_id)

        Return:
            Bool: True or False
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT name FROM SuperCategory "\
                        "WHERE name IN " \
                        "(SELECT super_id FROM Category " \
                        "WHERE id IN " \
                        "(SELECT category_id FROM Object WHERE img_id=%s))"

                value = (img_id)
                cursor.execute(query, value)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

        finally:
            self.db.commit()


def get_aug_image(db, category_id, grid_id):
    """
    Object table의 (category_id)와 Location의 (grid_id)를 받아
    Location table의 (x), (y), Object table의 (iteration), Image table의 (data) 반환

    Args:
        db (DB): DB class
        category_id (str): category table의 (id)
        grid_id (str): Grid table의 (id)

    Return:
        tuple ()()()(): (Location table의 x)(Location table의 y)(Object table의 iteration)(Image table의 data)
    """


def get_aug_mask(db, category_id, grid_id):
    """
    Object table의 (category_id), Location의 (grid_id)를 받아
    Location table의 (x), (y), Object table의 (iteration), Mask table의 (x), (y)

    Args:
        db (DB): DB class
        category_id (str): category table의 (id)
        grid_id (str): Grid table의 (id)

    Return:
        tuple ()()()()():(Location table의 x)(Location table의 y)(Object table의 iteration)(Mask table의 x)(Mask table의 y)
    """


# --------------------------------------- 수정 필요한 함수 ---------------------------------------
#
# def set_object_list(db, category_id, grid_id, iterations, mix_num):
#     """
#     Location table의 특정 (grid_id)를 가진 row와 Category table의 특정 (id)를 가진 row를 통해
#     [Location table의 특정 grid_id를 가진 row 수 X category table의 특정 category_id를 가진 row 수]만큼
#     Object table에 row 생성
#
#     Args:
#         db (DB): DB class
#         category_id (str): Category table의 id
#         grid_id (str): Location table의 grid_id
#         iterations (list): Object table의 iteration
#
#     Return:
#         Bool: True or False
#
#     """
#     # 특정 grid_id에 해당하는 row만 조사
#     loc_ids = db.get_location_from_grid_id(grid_id=grid_id)
#
#     for loc_id in loc_ids:
#         for iteration in iterations:
#             # 초기화를 위해 NULL(None)을 넣어줌
#             img_id = None
#             loc_id = loc_id
#             flag = db.set_object(img_id=img_id, loc_id=loc_id, category_id=category_id,
#                                  iteration=iteration, mix_num=mix_num)
#             if flag is False:
#                 return False
#
#     return True
#
#
# def list_object_check_num(db, category_id, grid_id, check_num_state):
#     """
#     Object table의 (category_id)
#     Location table의 (grid_id)를 입력 받아
#     Image table의 (check_num)이 check_state와 같으면 Object table의 row를 반환하는 함수
#
#     Args:
#         db (DB): DB class
#         category_id (str): Object table의 (category_id)
#         grid_id(str): Location table의 (grid_id)
#         check_num_state(str): Image table의 (check_num) 값과 비교될 값
#                           (0 : 검수 미진행, 1 : 완료, 2 : 거절)
#
#     Return:
#         tuple [object][row]: Object table의 row 값들
#
#     """
#     loc_ids = db.get_location_from_grid_id(grid_id=grid_id)
#     img_ids = db.get_obj_from_args(category_id=category_id, loc_ids=loc_ids)
#
#     print('loc_ids: ', loc_ids)
#     print('img_ids: ', img_ids)
#     obj_list = []
#     for img_id in img_ids:
#         img_id = str(img_id[0])
#         img_check_num = db.check_image_check_num(img_id=img_id)
#         if str(img_check_num) == check_num_state:
#             obj = db.get_obj_from_img_id(img_id=img_id)
#             obj_list.append(obj)
#
#     return sum(obj_list, ())