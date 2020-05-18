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

        # select databases, 'use [database]'와 동일
        self.db.select_db(db_name)
        self.db.commit()

    def set_Environment(self, ipv4, floor, width, height, depth):
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

        Return:
            True (boolean): Table 값 set 성공
            False (boolean): Table 값 set 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'INSERT INTO Environment(ipv4, floor, width, height, depth) VALUES(%s, %s, %s, %s, %s)'
                values = (ipv4, floor, width, height, depth)
                cursor.execute(query, values)

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)

            self.db.commit()
            return True

    def update_Environment(self, id, ipv4=None, floor=None, width=None, height=None, depth=None):
        """
        Enviroment table의 특정 id의 값들을 갱신

        Args:
            id (str): Enviroment table의 특정 id(primary key)
            ipv4 (str): 냉장고 ip 주소
            floor (str): 냉 장고 층
            width (str): 냉장고 층 가로 길이
            height (str): 냉장고 층 세로 길이
            depth (str): 냉장고 층 높이

        Return:
            True (boolean): 갱신 성공
            False (boolean): 갱신 실패
        """
        with self.db.cursor() as cursor:
            try:
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
                return False

            self.db.commit()
            return True

    def set_Image(self, device_id, image, type, check_num):
        """
        Image table에 값 추가(setting)

        Args:
            device_id (str): Environment table의 id(foreigner key)
            image (image): image data
            type (str): 합성된 이미지인지 아닌지
            check_num (str): 검수표시할 check 컬럼

        Return:
             True (boolean): 값 추가 성공
             False (boolean): 값 추가 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'INSERT INTO Image(env_id, data, type, check_num) VALUES(%s, %s, %s, %s)'
                values = (device_id, image, type, check_num)

                cursor.execute(query, values)

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return False
            finally:
                self.db.commit()
                return True

    def update_Image(self, id, device_id=None, image=None, type=None, check_num=None):
        """
        Image table의 특정 id의 값들 갱신

        Args:
            id (str): Image table의 특정 id(primary key)
            device_id (str): Image table의 env_id(foreigner key)
            image (image): image 정보
            type (str): 합성된 이미지 인지 아닌지
            check_num (str): 검수표시할 check 컬럼

        Return:
            True (boolean): 갱신 성공
            False (boolean): 갱신 실패
        """
        with self.db.cursor() as cursor:
            try:
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
                return False

            self.db.commit()
            return True

    def set_Grid(self, width, height):
        """
        Grid table 값 추가(set)

        Args:
            width (str): grid 가로 칸 개수
            height (str): grid 세로 칸 개수
        Return:
            True (boolean): 추가 성공
            False (boolean): 추가 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'INSERT INTO Grid(width, height) VALUES(%s, %s)'
                values = (width, height)
                cursor.execute(query, values)

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return False

            self.db.commit()
            return True

    def update_Grid(self, id, width=None, height=None):
        """
        Grid table의 특정 id row 값들을 갱신

        Args:
            id (str): Grid table의 특정 id(primary key)
            width (str): grid 가로 칸 수
            height (str): grid 세로 칸 수

        Return:
            True (boolean): 갱신 성공
            False (boolean): 갱신 실패
        """
        with self.db.cursor() as cursor:
            try:
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
                return False

            self.db.commit()
            return True

    def set_Location(self, grid_id, x, y):
        """
        Location table의 값을 추가(set)

        Args:
            grid_id (str): Grid table의 id(foreigner key)
            x (str): 물체의 가로 좌표
            y (str): 물체의 세로 좌표

        Return:
            True (boolean): 추가 성공
            False (boolean): 추가 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'INSERT INTO Location(grid_id, x, y) VALUES(%s, %s, %s)'
                values = (grid_id, x, y)
                cursor.execute(query, values)

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return False

            self.db.commit()
            return True

    def update_Location(self, id, grid_id=None, x=None, y=None):
        """
        Location table의 특정 id의 row 정보 갱신

        Args:
            id (str): Location table의 특정 id(primary key)
            grid_id (str): Grid table의 특정 id(foreigner key)
            x (str): 물체의 x 좌표
            y (str): 물체의 y 좌표
        Return:
            True (boolean): 갱신 성공
            False (boolean): 갱신 실패
        """
        with self.db.cursor() as cursor:
            try:

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
                return False

            self.db.commit()
            return True

    def set_SuperCategory(self, name):
        """
        SuperCategory table의 row 추가(set)

        Arg:
            name (str): 물체의 이름(종류)

        Return:
            True (boolean): 추가 성공
            False (boolean): 추가 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'INSERT INTO SuperCategory(name) VALUES(%s)'
                values = (name)
                cursor.execute(query, values)

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return False

            self.db.commit()
            return True

    def update_SuperCategory(self, id, name=None):
        """
        SuperCategory table의 특정 id의 row 정보 갱신

        Args:
            id (str): SuperCategory table의 특정 id(primary key)
            name (str): 물체의 이름(종류)

        Return:
            True (boolean): 갱신 성공
            False (boolean): 갱신 실패
        """
        with self.db.cursor() as cursor:
            try:
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
                return False

            self.db.commit()
            return True

    def set_Category(self, super_id, name, width, height, depth, iteration, thumbnail):
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

        Return:
            True (boolean): 추가 성공
            False (boolean): 추가 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'INSERT INTO Category(super_id, name, width, height, depth, iteration, thumbnail) VALUES(%s, %s, %s, %s, %s, %s, %s)'
                values = (super_id, name, width, height, depth, iteration, thumbnail)
                cursor.execute(query, values)

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return False

            self.db.commit()
            return True

    def update_Category(self, id, super_id=None, name=None, width=None, height=None, depth=None, iteration=None, thumbnail=None):
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
            True (boolean): 갱신 성공
            False (boolean): 갱신 실패
        """
        with self.db.cursor() as cursor:
            try:
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
                return False

            self.db.commit()
            return True

    def set_Object(self, img_id, loc_id, category_id):
        """
        Object table의 정보 추가

        Args:
            img_id (str): Image table의 id(foreigner key)
            loc_id (str): Location table의 id(foreigner key)
            category_id (str): Category table의 id(foreigner key)

        Return:
            True (boolean): 추가 성공
            False (boolean): 추가 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'INSERT INTO Object(img_id, loc_id, category_id) VALUES(%s, %s, %s)'
                values = (img_id, loc_id, category_id)
                cursor.execute(query, values)

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return False

            self.db.commit()
            return True

    def update_Object(self, id, img_id=None, loc_id=None, category_id=None):
        """
        Object table의 특정 id 정보 갱신

        Args:
            id (str): Object table의 특정 id(primary key)
            img_id (str): Image talbe의 특정 id(foreigner key)
            loc_id (str): Location table의 특정 id(foreigner key)
            category_id (str): Category table의 특정 id(foreigner key)

        Return:
            True (boolean): 갱신 성공
            False (boolean): 갱신 실패
        """
        with self.db.cursor() as cursor:
            try:
                query_head = 'UPDATE Object SET '
                query_tail = ' WHERE id={}'.format(id)
                if img_id != None:
                    query_head += 'img_id={}, '.format(img_id)
                if loc_id != None:
                    query_head += 'loc_id={}, '.format(loc_id)
                if category_id != None:
                    query_head += 'Category_id={}, '.format(category_id)

                query = query_head[:-2]
                query += query_tail

                cursor.execute(query)

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return False

            self.db.commit()
            return True

    def set_Bbox(self, obj_id, x, y, width, height):
        """
        Bbox table에 정보 추가

        Args:
            obj_id (str): Object table의 id(foreigner key)
            x (str): Bbox의 왼쪽 시작 점 x 좌표
            y (str): Bbox의 왼쪽 시작 점 y 좌표
            width (str): Bbox의 가로 크기
            height (str): Bbox의 세로 크기

        Return:
            True (boolean): 추가 성공
            False (boolean): 추가 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'INSERT INTO Bbox(obj_id, x, y, width, height) VALUES(%s, %s, %s, %s, %s)'
                values = (obj_id, x, y, width, height)
                cursor.execute(query, values)

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return False

            self.db.commit()
            return True

    def update_Bbox(self, id, x=None, y=None, width=None, height=None):
        """
        Bbox table의 특정 id row 갱신

        Args:
            id (str): Bbox table의 특정 id(primary key)
            x (str): Bbox의 왼쪽 시작점 x 좌표
            y (str): Bbox의 왼쪽 시작점 y 좌표
            width (str): Bbox의 가로 크기
            height (str): Bboxm의 세로 크기

        Return:
            True (boolean): 갱신 성공
            False (boolean): 갱신 실패
        """
        with self.db.cursor() as cursor:
            try:
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
                return False

            self.db.commit()
            return True

    def set_Mask(self, obj_id, x, y):
        """
        Mask table의 정보 추가

        Args:
            obj_id (str): Object table의 id(foreigner key)
        """
        with self.db.cursor() as cursor:
            try:
                query = 'INSERT INTO Mask(obj_id, x, y) VALUES(%s, %s, %s)'
                values = (obj_id, x, y)
                cursor.execute(query, values)

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return False

            self.db.commit()
            return True

    def update_Mask(self, id, obj_id=None, x=None, y=None):
        with self.db.cursor() as cursor:
            try:
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
                return False

            self.db.commit()
            return True

    def get_table(self, id, table):
        """
        mysql databse에 있는 특정 table의 특정 id를 가져옵니다.
        Args:
            id (str): table의 id 값
            table (str): 조회하기 원하는 table 이름
        Return:
            tuple[][] (tuple): 해당 id의 row 값
            None: 조회 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM ' + table + ' WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return cursor.fetchall()

            except Exception as e:
                print('Error function:', inspect.stack()[0][3], '_', table)
                print(e)
                return None

    def delete_table(self, id, table):
        """
        mysql databse에 있는 특정 table의 특정 id를 지웁니다..
        Args:
            id (str): table의 id 값
            table (str): 조회하기 원하는 table 이름
        Return:
            True (boolean): 삭제 성공
            False (boolean): 삭제 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'DELETE FROM ' + table + ' WHERE id=%s'
                values = (id)
                cursor.execute(query, values)

            except Exception as e:
                print('Error function:', inspect.stack()[0][3], table)
                print(e)
                return False

            self.db.commit()
            return True

    def list_table(self, table):
        """
        mysql databse에 있는 특정 table의 모든 값을 가져옵니다.
        Args:
            table (str): 조회하기 원하는 table 이름
        Return:
            list[][] (list): 특정 table의 모든 값
            None: 조회 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM ' + table
                cursor.execute(query)
                return list(cursor.fetchall())

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
        with self.db.cursor() as cursor:
            try:
                query = 'DROP TABLE '
                query += table
                cursor.execute(query)
                return list(cursor.fetchall())

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return None

    def last_id_table(self, table):
        """
        table의 마지막 id 값 조회

        Args:
            table (str): table 이

        Return:
            list[][] (list): 마지막 id 값
            None: 조회 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT MAX(id) FROM ' + table
                cursor.execute(query)
                return list(cursor.fetchall())

            except Exception as e:
                print('Error function:', inspect.stack()[0][3], '_', table)
                print(e)
                return None