import pymysql
import querys
import inspect


class DB:
    """
    MySQL 서버와 정보를 주고받는 class 입니다.
    """
    def __init__(self, ip, port, user, password, db_name, charset='utf8'):
        """
        DB class 초기화
        pymysql.connect()를 이용해 MySQL과 연결

        Args:
            ip: MySQL 서버에 로그인하기위한 ip 주소
            port: 포트 포워딩을 위한 포트
            user: MySQL 서버에 로그인을 위한 아이디
            password: MySQL 서버에 로그인을 위한 비밀번호
            db_name: 데이터베이스 네임
            charset: 문자 인코딩 방식
        """
        try:
            self.db = pymysql.connect(host=str(ip), port=port, user=user, passwd=password, db=db_name, charset=charset)
            print("setting on")

        except Exception as e:
            print('invalid DB information')
            print(e)
        #-- let's think about cashing here --
        #-- ---------------------------------

    def set_environment(self, ipv4, floor, width, height, depth):
        """
        촬영된 냉장고의 환경(environment) 정보를 Enviroment table에 저장
        cursor Object를 가져옴 -> cursor.execute()를 통해 SQL 실행
        commit()을 통해 mySQL 서버에 확정 반영

        Args:
            ipv4: 연결된 냉장고의 ip
            floor: 냉장고 층
            width: 냉장고 층 가로길이
            height: 냉장고 층 세로길이
            depth: 냉장고 층 높이

        Return:
            True: Table 값 추가(set) 성공
            False: Table 값 추가(set) 실패
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

    def get_environment(self, id):
        """
        Enviroment table의 특정 id의 정보를 가져옴

        Arg:
            id: Enviroment table의 특정 id(primary key)

        Retrun:
            cursor.fetchall(): Enviroment table의 특정 id의 row 값들
            None: error가 발생했을 때
        """
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM Environment WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return cursor.fetchall()

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return None

    def delete_environment(self, id):
        """
        Enviroment table의 특정 id 값 삭제

        Arg:
            id: Enviroment table의 특정 id(primary key)

        Return:
            True: 삭제 성공
            False: 삭제 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'DELETE FROM Environment WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return False

            self.db.commit()
            return True

    def update_environment(self, id, ipv4=None, floor=None, width=None, height=None, depth=None):
        """
        Enviroment table의 특정 id의 값들을 갱신

        Args:
            id: Enviroment table의 특정 id(primary key)
            ipv4: 냉장고 ip 주소
            floor: 냉장고 층
            width: 냉장고 층 가로 길이
            height: 냉장고 층 세로 길이
            depth: 냉장고 층 높이

        Return:
            True: 갱신 성공
            False: 갱신 실패
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

    def list_environment(self):
        """
        Environment table의 모든 값 반환

        Return:
           list(): Environment table의 모든 값을 리스트로 반환
           None: 에러로 인한 반환 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM Environment'
                cursor.execute(query)
                return list(cursor.fetchall())
            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return None

    def set_image(self, device_id, image, type, check_num):
        """
        Image table에 값 추가(setting)

        Args:
            device_id: Environment table의 id(foreigner key)
            image: image data
            type: 합성된 이미지인지 아닌지
            check_num: 검수표시할 check 컬럼

        Return:
             True: 값 추가 성공
             False: 값 추가 실패
        """
        with self.db.cursor() as cursor:
            try:
                if isinstance(image, str):
                    with open(image, 'rb') as file:
                        image = file.read()

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

    def get_image(self, id):
        """
        Image table에서 특정 id의 값 가져옴

        Arg:
            id: Image table에서 특정 id(primary key)

        Return:
            cursor.fetchall(): 특정 id의 row 조회
            None: 조회 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM Image WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return cursor.fetchall()

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return None

    def delete_image(self, id):
        """
        Image table의 특정 id의 row 정보 삭제

        Arg:
            id: Image table의 특정 id(primary key)
        Return:
            True: 삭제 성공
            False: 삭제 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'DELETE FROM Image WHERE id=%s'
                values = (id)
                cursor.execute(query, values)

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return False

            self.db.commit()
            return True

    def update_image(self, id, device_id=None, image=None, type=None, check_num=None):
        """
        Image table의 특정 id의 값들 갱신

        Args:
            id: Image table의 특정 id(primary key)
            device_id: Image table의 env_id(foreigner key)
            image: image 정보
            type: 합성된 이미지 인지 아닌지
            check_num: 검수표시할 check 컬럼

        Return:
            True: 갱신 성공
            False: 갱신 실패
        """
        with self.db.cursor() as cursor:
            try:
                if isinstance(image, str):
                    with open(image, 'rb') as file:
                        image = file.read()

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

    def list_image(self):
        """
        Image table의 모든 값 조회

        Return:
            list(): Image table의 모든 값 조회
            None: 조회 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM Image'
                cursor.execute(query)
                return list(cursor.fetchall())

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return None

    def set_grid(self, width, height):
        """
        Grid table 값 추가(set)

        Args:
            width: grid 가로 칸 개수
            height: grid 세로 칸 개수
        Return:
            True: 추가 성공
            False: 추가 실패
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

    def get_grid(self, id):
        """
        Grid table에서 특정 id의 row 조회

        Arg:
            id: Grid table의 특정 id(primary key)
        Return:
            cursor.fetchall(): 특정 id의 row 정보
            None: 조회 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM Grid WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return cursor.fetchall()

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return None

    def delete_grid(self, id):
        """
        Grid table에서 특정 id의 row 정보 삭제

        Arg:
            id: Grid table의 특정 id(primary key)
        Return:
            True: 삭제 성공
            False: 삭제 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'DELETE FROM Grid WHERE id=%s'
                values = (id)
                cursor.execute(query, values)

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return False

            self.db.commit()
            return True

    def update_grid(self, id, width=None, height=None):
        """
        Grid table의 특정 id row 값들을 갱신

        Args:
            id: Grid table의 특정 id(primary key)
            width: grid 가로 칸 수
            height: grid 세로 칸 수

        Return:
            True: 갱신 성공
            False: 갱신 실패
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

    def list_grid(self):
        """
        Grid table의 모든 값 조회

        Return:
            list(): Grid table의 모든 값
            None: 조회 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM Grid'
                cursor.execute(query)
                return list(cursor.fetchall())

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return None

    def set_location(self, grid_id, x, y):
        """
        Location table의 값을 추가(set)

        Args:
            grid_id: Grid table의 id(foreigner key)
            x: 물체의 가로 좌표
            y: 물체의 세로 좌표

        Return:
            True: 추가 성공
            False: 추가 실패
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

    def get_location(self, id):
        """
        Location table의 특정 id의 row 값 조회

        Arg:
            id: Location table의 특정 id(primary key)

        Return:
            cursor.fetchall(): Location table의 특정 id의 row 값
            None: 조회 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM Location WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return cursor.fetchall()

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return None

    def delete_location(self, id):
        """
        Location table의 특정 id row 삭제

        Arg:
            id: Location table의 특정 id(primary key)

        Return:
            True: 삭제 성공
            False: 삭제 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'DELETE FROM Location WHERE id=%s'
                values = (id)
                cursor.execute(query, values)

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return False

            self.db.commit()
            return True

    def update_location(self, id, grid_id=None, x=None, y=None):
        """
        Location table의 특정 id의 row 정보 갱신

        Args:
            id: Location table의 특정 id(primary key)
            grid_id: Grid table의 특정 id(foreigner key)
            x: 물체의 x 좌표
            y: 물체의 y 좌표
        Return:
            True: 갱신 성공
            False: 갱신 실패
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

    def list_location(self):
        """
        Location table의 모든 정보 획득

        Return:
            list(): Location table의 모든 정보
            None: 조회 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM Location'
                cursor.execute(query)
                return list(cursor.fetchall())

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return None

    def set_superCategory(self, name):
        """
        SuperCategory table의 row 추가(set)

        Arg:
            name: 물체의 이름(종류)

        Return:
            True: 추가 성공
            False: 추가 실패
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

    def get_superCategory(self, id):
        """
        SuperCategory table의 특정 id의 row 조회

        Arg:
            id: SuperCategory table의 특정 id(primary key)

        Return:
            cursor.fetchall(): superCategory table의 특정 id의 row 정보
            None: 조회 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM SuperCategory WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return cursor.fetchall()

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return None

    def delete_superCategory(self, id):
        """
        SuperCategory table의 특정 id의 row 정보 삭제

        Arg:
            id: SuperCategory table의 특정 id(primary key)

        Return:
            True: 삭제 성공
            False: 삭제 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'DELETE FROM SuperCategory WHERE id=%s'
                values = (id)
                cursor.execute(query, values)

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return False

            self.db.commit()
            return True

    def update_superCategory(self, id, name=None):
        """
        SuperCategory table의 특정 id의 row 정보 갱신

        Args:
            id: SuperCategory table의 특정 id(primary key)
            name: 물체의 이름(종류)

        Return:
            True: 갱신 성공
            False: 갱신 실패
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

    def list_superCategory(self):
        """
        SuperCategory table의 모든 정보 조회

        Return:
            list(): superCategory table의 모든 정보
            None: 조회 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM SuperCategory'
                cursor.execute(query)
                return list(cursor.fetchall())

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return None

    def set_category(self, super_id, name, width, height, depth, iteration, thumbnail):
        """
        Category table에 row 정보 추가

        Args:
            super_id: SuperCategory table의 특정 id(foreigner key)
            name: 물품의 이름
            width: 물체의 가로 크기
            height: 물체의 세로 크기
            depth: 물체의 높이
            iteration: 물체 촬영 횟수
            thumbnail: 썸네일 이미지

        Return:
            True: 추가 성공
            False: 추가 실패
        """
        with self.db.cursor() as cursor:
            try:
                if isinstance(thumbnail, str):
                    with open(thumbnail, 'rb') as file:
                        thumbnail = file.read()

                query = 'INSERT INTO Category(super_id, name, width, height, depth, iteration, thumbnail) VALUES(%s, %s, %s, %s, %s, %s, %s)'
                values = (super_id, name, width, height, depth, iteration, thumbnail)
                cursor.execute(query, values)

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return False

            self.db.commit()
            return True

    def get_category(self, id):
        """
        Category table의 특정 id의 row 조회

        Arg:
            id: Category table의 id(primary key)

        Return:
            cursor.fetchall(): id의 row 정보
            None: id 조회 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM Category WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return cursor.fetchall()

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return None

    def delete_category(self, id):
        """
        Category table의 특정 id row 삭제

        Arg:
            id: Category table의 특정 id(primary key)

        Return:
            True: 삭제 성공
            False: 삭제 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'DELETE FROM Category WHERE id=%s'
                values = (id)
                cursor.execute(query, values)

            except Exception as e:
                print(e)
                print('Error function:', inspect.stack()[0][3])
                return False

            self.db.commit()
            return True

    def update_category(self, id, super_id=None, name=None, width=None, height=None, depth=None, iteration=None, thumbnail=None):
        """
        Category table의 특정 id의 row 정보 갱신

        Args:
            id: Category table의 특정 id(primary key)
            super_id: superCategory의 id(foreigner key)
            name: 물품의 이름
            width: 물체의 가로 크기
            height: 물체의 세로 크기
            depth: 물체의 높이
            iteration: 물체 촬영 횟수
            thumbnail: 썸네일 이미지

        Return:
            True: 갱신 성공
            False: 갱신 실패
        """
        with self.db.cursor() as cursor:
            try:
                if isinstance(thumbnail, str):
                    with open(thumbnail, 'rb') as file:
                        thumbnail = file.read()

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

    def list_category(self):
        """
        Category table의 모든 정보 조회

        Return:
            list(): Category table의 모든 정보
            None: 조회 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM Category'
                cursor.execute(query)
                return list(cursor.fetchall())

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return None

    def set_object(self, img_id, loc_id, category_id):
        """
        Object table의 정보 추가

        Args:
            img_id: Image table의 id(foreigner key)
            loc_id: Location table의 id(foreigner key)
            category_id: Category table의 id(foreigner key)

        Return:
            True: 추가 성공
            False: 추가 실패
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

    def get_object(self, id):
        """
        Object table의 특정 id의 row 정보 조회

        Arg:
            id: Object table의 특정 id(primary key)

        Return:
            cursor.fetchall(): Object table의 모든 정보
            None: 조회 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM Object WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return cursor.fetchall()

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return None

    def delete_object(self, id):
        """
        Object table에서 특정 id row 삭제

        Arg:
            id: Object talbe의 특정 id(primary key)

        Return:
            True: 삭제 성공
            False: 삭제 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'DELETE FROM Object WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return False

            self.db.commit()
            return True

    def update_object(self, id, img_id=None, loc_id=None, category_id=None):
        """
        Object table의 특정 id 정보 갱신

        Args:
            id: Object table의 특정 id(primary key)
            img_id: Image talbe의 특정 id(foreigner key)
            loc_id: Location table의 특정 id(foreigner key)
            category_id: Category table의 특정 id(foreigner key)

        Return:
            True: 갱신 성공
            False: 갱신 실패
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

    def list_object(self):
        """
        Object table의 모든 정보 조회

        Return:
            list(): Object table의 모든 정보를 list로 반환
            None: 조회 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM Object'
                cursor.execute(query)
                return list(cursor.fetchall())

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return None

    def set_bbox(self, obj_id, x, y, width, height):
        """
        Bbox table에 정보 추가

        Args:
            obj_id: Object table의 id(foreigner key)
            x: Bbox의 왼쪽 시작 점 x 좌표
            y: Bbox의 왼쪽 시작 점 y 좌표
            width: Bbox의 가로 크기
            height: Bbox의 세로 크기

        Return:
            True: 추가 성공
            False: 추가 실패
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

    def get_bbox(self, id):
        """
        Bbox table의 특정 id row 조회

        Arg:
            id: Bbox table의 특정 id(primary key)

        Return:
            cursor.fetchall(): 특정 id의 row 정보
            None: 조회 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM Bbox WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return cursor.fetchall()

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return None

    def delete_bbox(self, id):
        """
        Bbox table의 특정 id 삭제

        Arg:
            id: Bbox table의 특정 id(primary key)

        Return:
            True: 삭제 성공
            False: 삭제 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'DELETE FROM Bbox WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return False

            self.db.commit()
            return True

    def update_bbox(self, id, x=None, y=None, width=None, height=None):
        """
        Bbox table의 특정 id row 갱신

        Args:
            id: Bbox table의 특정 id(primary key)
            x: Bbox의 왼쪽 시작점 x 좌표
            y: Bbox의 왼쪽 시작점 y 좌표
            width: Bbox의 가로 크기
            height: Bboxm의 세로 크기

        Return:
            True: 갱신 성공
            False: 갱신 실패
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

    def list_bbox(self):
        """
        Bbox table의 모든 정보 조회

        Return:
            list(): Bbox table의 모든 정보 조회
            None: 조회 실패
        """
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM Bbox'
                cursor.execute(query)
                return list(cursor.fetchall())

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return None

    def set_mask(self, obj_id, x, y):
        """
        Mask table의 정보 추가

        Args:
            obj_id: Object table의 id(foreigner key)
            x:

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

    def get_mask(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM Mask WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return cursor.fetchall()

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return None

    def delete_mask(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'DELETE FROM Mask WHERE id=%s'
                values = (id)
                cursor.execute(query, values)

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return False

            self.db.commit()
            return True

    def update_mask(self, id, obj_id=None, x=None, y=None):
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

    def list_mask(self):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM Mask'
                cursor.execute(query)
                return list(cursor.fetchall())

            except Exception as e:
                print('Error function:', inspect.stack()[0][3])
                print(e)
                return None

    def table_initialize(self):
        try:
            with self.db.cursor() as cursor:
                for i, sql in enumerate(querys.initial_queries):
                    print('{} 번째 sql 실행중...'.format(i + 1))
                    cursor.execute(sql)

                cursor.execute("SHOW TABLES")
                for line in cursor.fetchall():
                    print(line)

        except Exception as e:
            print('your database is already exist')
            print(e)

        finally:
            self.db.commit()