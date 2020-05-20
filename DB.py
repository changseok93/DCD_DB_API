# -*- coding: utf-8 -*-
import pymysql
import querys
import inspect


class DB:
    """
    MySQL 서버와 정보를 주고받는 class 입니다.
    """
    def __init__(self, ip, port, user, password, db_name, charset='utf8mb4'):
        """
        DB class를 초기화하는 함수
        pymysql.connect()를 이용해 MySQL과 연결
        데이터베이스 생성
        mysql 서버의 변수 설정
            wait_timeout: 활동하지 않는 커넥션을 끊을때까지 서버가 대기하는 시간
            interactive_timeout: 활동중인 커넥션이 닫히기 전까지 서버가 대기하는 시간
            max_connections: 한번에 mysql 서버에 접속할 수 있는 클라이언트 수
            참조: https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html

        Args:
            ip (str): MySQL 서버에 로그인하기위한 ip 주소
            port (int): 포트 포워딩을 위한 포트
            user (str): MySQL 서버에 로그인을 위한 아이디
            password (str): MySQL 서버에 로그인을 위한 비밀번호
            db_name (str): 데이터베이스 네임
            charset (str): 문자 인코딩 방식

        Example:
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

                query = 'SET GLOBAL wait_timeout=31536000;'
                cursor.execute(query)

                query = 'SET GLOBAL interactive_timeout=31536000;'
                cursor.execute(query)

                query = 'SET GLOBAL max_connections=100000;'
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
        촬영된 냉장고의 환경(environment) 정보를 Enviroment table에 저장
        cursor Object를 가져옴 -> cursor.execute()를 통해 SQL 실행
        commit()을 통해 mySQL 서버에 확정 반영

        Args:
            ipv4 (str): 연결된 냉장고의 ip
            floor (str) : 냉장고 층
            width (str): 냉장고 층 가로길이
            height (str): 냉장고 층 세로길이
            depth (str): 냉장고 층 높이

        Example:
            db.set_environment(ipv4='127.223.444.443', floor='1', width='2', height='3', depth='2')
        """
        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO Environment(ipv4, floor, width, height, depth) VALUES(%s, %s, %s, %s, %s)'
                values = (ipv4, floor, width, height, depth)
                cursor.execute(query, values)

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)

        finally:
            self.db.commit()

    def update_environment(self, id, ipv4=None, floor=None, width=None, height=None, depth=None):
        """
        Enviroment table의 특정 id의 값들을 갱신

        Args:
            id (str): Enviroment table의 특정 id(primary key)
            ipv4 (str): 냉장고 ip 주소
            floor (str): 냉 장고 층
            width (str): 냉장고 층 가로 길이
            height (str): 냉장고 층 세로 길이
            depth (str): 냉장고 층 높이

        Example:
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

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)

        finally:
            self.db.commit()

    def set_image(self, device_id, image, type, check_num):
        """
        Image table에 값 추가(setting)

        Args:
            device_id (str): Environment table의 id(foreigner key)
            image (image): image data
            type (str): 합성된 이미지인지 아닌지
            check_num (str): 검수표시할 check 컬럼

        Example:
            mydb.set_image(device_id='1', image=img, type='0', check_num='1')
        """
        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO Image(env_id, data, type, check_num) VALUES(%s, %s, %s, %s)'
                values = (device_id, image, type, check_num)

                cursor.execute(query, values)

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)

        finally:
            self.db.commit()

    def update_image(self, id, device_id=None, image=None, type=None, check_num=None):
        """
        Image table의 특정 id의 값들 갱신

        Args:
            id (str): Image table의 특정 id(primary key)
            device_id (str): Image table의 env_id(foreigner key)
            image (image): image 정보
            type (str): 합성된 이미지 인지 아닌지
            check_num (str): 검수표시할 check 컬럼
        Example:
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

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)

        finally:
            self.db.commit()

    def set_grid(self, width, height):
        """
        Grid table 값 추가(set)

        Args:
            width (str): grid 가로 칸 개수
            height (str): grid 세로 칸 개수

        Example:
            mydb.set_grid(width='3', height='3')
        """
        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO Grid(width, height) VALUES(%s, %s)'
                values = (width, height)
                cursor.execute(query, values)

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)

        finally:
            self.db.commit()

    def update_grid(self, id, width=None, height=None):
        """
        Grid table의 특정 id row 값들을 갱신

        Args:
            id (str): Grid table의 특정 id(primary key)
            width (str): grid 가로 칸 수
            height (str): grid 세로 칸 수

        Example:
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

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)

        finally:
            self.db.commit()

    def set_location(self, grid_id, x, y):
        """
        Location table의 값을 추가(set)

        Args:
            grid_id (str): Grid table의 id(foreigner key)
            x (str): 물체의 가로 좌표
            y (str): 물체의 세로 좌표

        Example:
            mydb.set_location(grid_id='1', x='2', y='2')
        """
        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO Location(grid_id, x, y) VALUES(%s, %s, %s)'
                values = (grid_id, x, y)
                cursor.execute(query, values)

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)

        finally:
            self.db.commit()

    def update_location(self, id, grid_id=None, x=None, y=None):
        """
        Location table의 특정 id의 row 정보 갱신

        Args:
            id (str): Location table의 특정 id(primary key)
            grid_id (str): Grid table의 특정 id(foreigner key)
            x (str): 물체의 x 좌표
            y (str): 물체의 y 좌표

        Example:
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

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)

        finally:
            self.db.commit()

    def set_supercategory(self, name):
        """
        SuperCategory table의 row 추가(set)

        Arg:
            name (str): 물체의 이름(종류)

        Example:
            mydb.set_supercategory(name='hi4')
        """
        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO SuperCategory(name) VALUES(%s)'
                values = (name)
                cursor.execute(query, values)

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)

        finally:
            self.db.commit()

    def update_supercategory(self, id, name=None):
        """
        SuperCategory table의 특정 id의 row 정보 갱신

        Args:
            id (str): SuperCategory table의 특정 id(primary key)
            name (str): 물체의 이름(종류)

        Example:
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

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)

        finally:
            self.db.commit()

    def set_category(self, super_id, name, width, height, depth, iteration, thumbnail):
        """
        Category table에 row 정보 추가

        Args:
            super_id (str): SuperCategory table의 특정 id(foreigner key)
            name (str): 물품의 이름
            width (str): 물체의 가로 크기
            height (str): 물체의 세로 크기
            depth (str): 물체의 높이
            iteration (str): 물체 촬영 횟수
            thumbnail (image): 썸네일 이미지

        Example:
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

        Example:
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

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)

        finally:
            self.db.commit()

    def set_object(self, img_id, loc_id, category_id, iteration):
        """
        Object table의 정보 추가

        Args:
            img_id (str): Image table의 id(foreigner key)
            loc_id (str): Location table의 id(foreigner key)
            category_id (str): Category table의 id(foreigner key)
            iteration (str): 물체를 방향 별로 찍어야하는 횟수

        Example:
            mydb.set_object(img_id='1', loc_id='1', category_id='1', iteration=2)
        """
        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO Object(img_id, loc_id, category_id, iteration) VALUES(%s, %s, %s, %s)'
                values = (img_id, loc_id, category_id, iteration)
                cursor.execute(query, values)

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)

        finally:
            self.db.commit()

    def update_object(self, id, img_id=None, loc_id=None, category_id=None, iteration=None):
        """
        Object table의 특정 id 정보 갱신

        Args:
            id (str): Object table의 특정 id(primary key)
            img_id (str): Image talbe의 특정 id(foreigner key)
            loc_id (str): Location table의 특정 id(foreigner key)
            category_id (str): Category table의 특정 id(foreigner key)
            iteration (str): 물체를 방향 별로 찍어야하는 횟수

        Example:
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

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)

        finally:
            self.db.commit()

    def set_bbox(self, obj_id, x, y, width, height):
        """
        Bbox table에 정보 추가

        Args:
            obj_id (str): Object table의 id(foreigner key)
            x (str): Bbox의 왼쪽 시작 점 x 좌표
            y (str): Bbox의 왼쪽 시작 점 y 좌표
            width (str): Bbox의 가로 크기
            height (str): Bbox의 세로 크기

        Example:
            mydb.set_bbox(obj_id='1', x='10', y='10', width='1', height='1')
        """
        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO Bbox(obj_id, x, y, width, height) VALUES(%s, %s, %s, %s, %s)'
                values = (obj_id, x, y, width, height)
                cursor.execute(query, values)

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)

        finally:
            self.db.commit()

    def update_bbox(self, id, x=None, y=None, width=None, height=None):
        """
        Bbox table의 특정 id row 갱신

        Args:
            id (str): Bbox table의 특정 id(primary key)
            x (str): Bbox의 왼쪽 시작점 x 좌표
            y (str): Bbox의 왼쪽 시작점 y 좌표
            width (str): Bbox의 가로 크기
            height (str): Bboxm의 세로 크기

        Example:
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

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)

        finally:
            self.db.commit()

    def set_mask(self, obj_id, x, y):
        """
        Mask table의 정보 추가

        Args:
            obj_id (str): Object table의 id(foreigner key)
            x: Mask 점의 x 좌표
            y: Mask 점의 y 좌표

        Example:
            mydb.set_mask(obj_id='1', x='20', y='20')
        """
        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO Mask(obj_id, x, y) VALUES(%s, %s, %s)'
                values = (obj_id, x, y)
                cursor.execute(query, values)

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)

        finally:
            self.db.commit()

    def update_mask(self, id, obj_id=None, x=None, y=None):
        """
        Mask table의 정보 업데이트

        Args:
            id: Mask table의 id(primary key)
            obj_id (str): Object table의 id(foreigner key)
            x: Mask 점의 x 좌표
            y: Mask 점의 y 좌표

        Example:
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

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)

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

        Example:
            mydb.delete_table(id='1', table='Bbox')
        """
        try:
            with self.db.cursor() as cursor:
                query = 'DELETE FROM ' + table + ' WHERE id=%s'
                values = (id)
                cursor.execute(query, values)

        except Exception as e:
            print('Error function:', inspect.stack()[0][3], table)
            print(e)

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
        """
        try:
            with self.db.cursor() as cursor:
                query = 'DROP TABLE '
                query += table
                cursor.execute(query)

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)

    def last_id_table(self, table):
        """
        table의 마지막 id 값 조회

        Args:
            table (str): table 이름

        Return:
            list[][]: 마지막 id 값
            None: 조회 실패

        Example:
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
        Environment table의 ipv4와 floor를 받아 Environment table id를 반환하는 함수

        Args:
            ipv4 (str): Environment table ipv4 정보
            floor (str): Environment table floor 정보

        Return:
            int: Environment table id
            None: 조회 실패

        example:
            mydb.get_env_id_from_args(ipv4='127.223.444.443', floor='1')
            SQL:
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
        Grid table의 width와 height 값을 받아 Grid table id를 반환하는 함수

        Args:
            width (str): gird 가로 칸 수
            height (str): grid 세로 칸 수

        Return:
            int: Grid table id
            None: 조회 실패

        Example:
            mydb.get_grid_id_from_args(width='3', height='3')
            SQL:
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

    def get_supercategory_id_from_args(self, name):
        """
        SuperCategory table의 name을 입력받아 SuperCategory table id 반환하는 함수

        Args:
            name (str): SuperCategory table의 name 정보

        Return:
            int: name에 해당하는 id
            None: 조회 실패

        Example:
            mydb.supercategory_id_from_args(name='스낵')
            SQL:
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
        조회하고 싶은 location 위치와 상위 grid를 받아 해당하는 location의 id를 반환하는 함수

        Args:
            grid_id (str): grid_id 값(foreigner key)
            x (str): location table의 width 값
            y (str): location table의 height 값

        Return:
            int: 해당 location의 id
            None: 조회 실패

        Example:
             mydb.get_location_id_from_args(grid_id=grid_id, x='22', y='2')
             SQL:
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
        조회하고 싶은 category name과 상위 super category name을 받아 해당하는 category의 id를 반환하는 함수

        Args:
            super_id (str): 조회하기 원하는 category의 상위 super_category
            category_name (str): 조회하기 원하는 category의 name

        Return:
            int: 해당 category의 id
            None: 조회 실패

        Example:
            mydb.get_category_id_from_args(super_id=super_id, category_name='ee2')
            SQL:
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
        Object table에서 img_id를 반환하는 함

        Args:
            obj_id (str): 조회하기 원하는 object의 id

        Return:
            int: 해당하는 Object table의 image id
            None: 조회 실패

        Example:
            mydb.check_img_check_num(img_id=img_id)
            SQL:
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

    def get_obj_id_from_args(self, img_id, loc_id, category_id, iteration):
        """
        Object table의 id를 반환하는 함수

        Args:
            img_id (str): Object table의 img_id
            loc_id (str): Object table의 loc_id
            category_id (str): Object table의 category_id
            iteration (str): Object table의 iteration

        Return:
            int: Object table의 id
            None: 조회 실패
        """
        try:
            with self.db.cursor() as cursor:
                query = "SELECT id FROM Object WHERE img_id=%s AND loc_id=%s AND category_id=%s AND iteration=%s"
                value = (img_id, loc_id, category_id, iteration)
                cursor.execute(query, value)
                return sum(cursor.fetchall(), ())[0]

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return None

    def check_image_check_num(self, img_id):
        """
        Image table의 이미지의 검수 여부(check_num)를 반환하는 함수

        Args:
            img_id (str): 조회하기 원하는 object의 id

        Return:
            int (0, 1, 2): 해당 object의 이미지 검수여부 반환
            None: 조회 실패

        Example:
            mydb.check_img_check_num(img_id=img_id)
            SQL:
                SELECT check_num FROM Image WHERE id=1
        """
        try:
            with self.db.cursor() as cursor:
                query = 'SELECT check_num FROM Image WHERE id=' + img_id
                cursor.execute(query)
                return sum(cursor.fetchall(), ())[0]

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return None

    def update_image_check_num(self, img_id, check_num):
        """
        Image table의 check_num을 원하는 값으로 수정하는 함수

        Args:
            img_id (str): 수정하기 원하는 Object table id
            check_num (str): 수정하기 원하는 Image table check_num

        Return:
            Bool: True or False

        Example:
            mydb.update_img_check_num(img_id=img_id, check_num=check_num)
            SQL:
                UPDATE Image SET check_num=100 WHERE id=1
        """
        try:
            with self.db.cursor() as cursor:
                query = 'UPDATE Image SET check_num=' + check_num + ' WHERE id=' + img_id
                print(query)
                cursor.execute(query)
                return True

        except Exception as e:
            print('Error function:', inspect.stack()[0][3])
            print(e)
            return False

    def update_image_img(self, img_id, img):
        """
        Image table의 image를 바꿈

        Args:
            img_id (str): Image table의 id
            img (Image): update할 image 데이터

        Return:
            Bool: True or False

        Example:
            db.update_image_img(img_id=img_id, img=img)
            SQL:
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

