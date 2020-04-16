import pymysql
import querys


class DB:
    """
    MySQL database와 정보를 주고받는 API class 입니다.
    """
    def __init__(self, ip, port, user, password, db_name, charset='utf8'):
        """
        DB class 초기화

        Args:
            ip: ipv4 주소
            port: 포트 포워딩을 위한 포트
            user: MySQL 서버에 로그인을 위한 아이디
            password: MySQL 서버에 로그인을 위한 비밀번호
            db_name: 데이터베이스 네임
            charset: 문자 인코딩 방식
        """
        try:
            self.db = pymysql.connect(host=str(ip), port=port, user=user, passwd=password, db=db_name, charset=charset)
        except Exception as e:
            print('invalid DB information')
            print(e)
        #-- let's think about cashing here --
        #--
        #--
        #-- ---------------------------------

    # environment table APIs
    def set_environment(self, ipv4, floor, width, height, depth):
        """
        Args:
            ipv4:
            floor:
            width:
            height:
            depth:

        Returns:
            True: Mysql에 쿼리 날리기 성
            False:
        """
        with self.db.cursor() as cursor:
            try:
                query = 'INSERT INTO environment(ipv4, floor, width, height, depth) VALUES(INET_ATON(%s), %s, %s, %s, %s)'
                values = (ipv4, floor, width, height, depth)
                cursor.execute(query, values)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def get_environment(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM environment WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return cursor.fetchall()

            except Exception as e:
                print(e)
                return None

    def delete_environment(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'DELETE FROM environment WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def update_environment(self, id, ipv4, floor, width, height, depth):
        with self.db.cursor() as cursor:
            try:
                query_head = 'UPDATE environment SET '
                query_tail = ' WHERE id={}'.format(id)
                if ipv4 != None:
                    query_head += 'ipv4=INET_ATON("{}"), '.format(ipv4)
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
                print(e)
                return False

            self.db.commit()
            return True

    def list_environment(self):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM environment'
                cursor.execute(query)
                return list(cursor.fetchall())
            except:
                return None

    def set_image(self, device_id, image, type):

        with self.db.cursor() as cursor:
            try:
                if isinstance(image, str):
                    with open(image, 'rb') as file:
                        image = file.read()

                query = 'INSERT INTO image(env_id, data, type) VALUES(%s, %s, %s)'
                values = (device_id, image, type)

                cursor.execute(query, values)

            except Exception as e:
                print(e)
                return False
            finally:
                self.db.commit()
                return True

    def get_image(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM image WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return cursor.fetchall()

            except Exception as e:
                print(e)
                return None

    def delete_image(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'DELETE FROM image WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def update_image(self, id=None, device_id=None, image=None, type=None):
        with self.db.cursor() as cursor:
            try:
                if isinstance(image, str):
                    with open(image, 'rb') as file:
                        image = file.read()

                query_head = 'UPDATE image SET '
                query_tail = ' WHERE id={}'.format(id)
                if device_id != None:
                    query_head += 'env_id={}, '.format(device_id)
                if image != None:
                    query_head += "data=x'{}' , ".format(image.hex())
                if type != None:
                    query_head += 'type={}, '.format(type)

                query = query_head[:-2]
                query += query_tail
                cursor.execute(query)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def list_image(self):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM image'
                cursor.execute(query)
                return list(cursor.fetchall())
            except:
                return None

    def set_grid(self, width, height):
        with self.db.cursor() as cursor:
            try:
                query = 'INSERT INTO grid(width, height) VALUES(%s, %s)'
                values = (width, height)
                cursor.execute(query, values)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def get_grid(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM grid WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return cursor.fetchall()

            except Exception as e:
                print(e)
                return None

    def detete_grid(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'DELETE FROM grid WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def update_grid(self, id, width, height):
        with self.db.cursor() as cursor:
            try:

                query_head = 'UPDATE grid SET '
                query_tail = ' WHERE id={}'.format(id)
                if width != None:
                    query_head += 'width={}, '.format(width)
                if width != None:
                    query_head += 'height={}, '.format(height)
                query = query_head[:-2]
                query += query_tail

                cursor.execute(query)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def list_grid(self):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM grid'
                cursor.execute(query)
                return list(cursor.fetchall())
            except:
                return None

    def set_location(self, grid_id, x, y):
        with self.db.cursor() as cursor:
            try:
                query = 'INSERT INTO location(grid_id, x, y) VALUES(%s, %s, %s)'
                values = (grid_id, x, y)
                cursor.execute(query, values)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def get_location(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM location WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return cursor.fetchall()

            except Exception as e:
                print(e)
                return None

    def delete_location(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'DELETE FROM location WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def update_location(self, id, grid_id, x, y):
        with self.db.cursor() as cursor:
            try:

                query_head = 'UPDATE location SET '
                query_tail = ' WHERE id={}'.format(id)
                if grid_id != None:
                    query_head += 'grid_id={}, '.format(grid_id)
                if x != None:
                    query_head += 'x={}, '.format(x)
                if y != None:
                    query_head += 'y={}, '.format(y)
                query = query_head[:-2]
                query += query_tail

                cursor.execute(query)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def list_location(self):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM location'
                cursor.execute(query)
                return list(cursor.fetchall())
            except:
                return None

    def set_superCategory(self, name):
        with self.db.cursor() as cursor:
            try:
                query = 'INSERT INTO superCategory(name) VALUES(%s)'
                values = (name)
                cursor.execute(query, values)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def get_superCategory(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM superCategory WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return cursor.fetchall()

            except Exception as e:
                print(e)
                return None

    def delete_superCategory(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'DELETE FROM superCategory WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def update_superCategory(self, id, name):
        with self.db.cursor() as cursor:
            try:

                query_head = 'UPDATE superCategory SET '
                query_tail = ' WHERE id={}'.format(id)
                if name != None:
                    query_head += 'name={}, '.format(name)
                query = query_head[:-2]
                query += query_tail

                cursor.execute(query)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def list_superCategory(self):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM superCategory'
                cursor.execute(query)
                return list(cursor.fetchall())
            except:
                return None

    def set_category(self, super_id, name, width, height, depth, thumbnail):
        with self.db.cursor() as cursor:
            try:
                if isinstance(thumbnail, str):
                    with open(thumbnail, 'rb') as file:
                        thumbnail = file.read()

                query = 'INSERT INTO category(super_id, name, width, height, depth, thumbnail) VALUES(%s, %s, %s, %s, %s, %s)'
                values = (super_id, name, width, height, depth, thumbnail)
                cursor.execute(query, values)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def get_category(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM category WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return cursor.fetchall()

            except Exception as e:
                print(e)
                return None

    def delete_category(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'DELETE FROM category WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def update_category(self, id, super_id, name, width, height, depth, thumbnail):
        with self.db.cursor() as cursor:
            try:
                if isinstance(thumbnail, str):
                    with open(thumbnail, 'rb') as file:
                        thumbnail = file.read()

                query_head = 'UPDATE category SET '
                query_tail = ' WHERE id={}'.format(id)
                if super_id != None:
                    query_head += 'super_id={}, '.format(super_id)
                if name != None:
                    query_head += 'name={}, '.format(name)
                if width != None:
                    query_head += 'width={}, '.format(width)
                if height != None:
                    query_head += 'height={}, '.format(height)
                if depth != None:
                    query_head += 'depth={}, '.format(depth)
                if thumbnail != None:
                    query_head += "thumbnail=x'{}' , ".format(thumbnail.hex())

                query = query_head[:-2]
                query += query_tail
                cursor.execute(query)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def list_category(self):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM category'
                cursor.execute(query)
                return list(cursor.fetchall())
            except:
                return None

    def set_object(self, img_id, loc_id, category_id):
        with self.db.cursor() as cursor:
            try:
                query = 'INSERT INTO object(img_id, loc_id, category_id) VALUES(%s, %s, %s)'
                values = (img_id, loc_id, category_id)
                cursor.execute(query, values)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def get_object(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM object WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return cursor.fetchall()

            except Exception as e:
                print(e)
                return None

    def delete_object(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'DELETE FROM object WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def update_object(self, id, img_id, loc_id, category_id):
        with self.db.cursor() as cursor:
            try:
                query_head = 'UPDATE object SET '
                query_tail = ' WHERE id={}'.format(id)
                if img_id != None:
                    query_head += 'img_id={}, '.format(img_id)
                if loc_id != None:
                    query_head += 'loc_id={}, '.format(loc_id)
                if category_id != None:
                    query_head += 'category_id={}, '.format(category_id)

                query = query_head[:-2]
                query += query_tail

                cursor.execute(query)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def list_object(self):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM object'
                cursor.execute(query)
                return list(cursor.fetchall())
            except:
                return None

    def set_bbox(self, obj_id, x, y, width, height):
        with self.db.cursor() as cursor:
            try:
                query = 'INSERT INTO bbox(obj_id, x, y, width, height) VALUES(%s, %s, %s, %s, %s)'
                values = (obj_id, x, y, width, height)
                cursor.execute(query, values)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def get_bbox(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM bbox WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return cursor.fetchall()

            except Exception as e:
                print(e)
                return None

    def delete_bbox(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'DELETE FROM bbox WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def update_bbox(self, id, x, y, width, height):
        with self.db.cursor() as cursor:
            try:
                query_head = 'UPDATE bbox SET '
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
                print(e)
                return False

            self.db.commit()
            return True

    def list_bbox(self):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM bbox'
                cursor.execute(query)
                return list(cursor.fetchall())
            except:
                return None

    def set_mask(self, obj_id, x, y):
        with self.db.cursor() as cursor:
            try:
                query = 'INSERT INTO mask(obj_id, x, y) VALUES(%s, %s, %s)'
                values = (obj_id, x, y)
                cursor.execute(query, values)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def get_mask(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM mask WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
                return cursor.fetchall()

            except Exception as e:
                print(e)
                return None

    def delete_mask(self, id):
        with self.db.cursor() as cursor:
            try:
                query = 'DELETE FROM mask WHERE id=%s'
                values = (id)
                cursor.execute(query, values)
            except Exception as e:
                print(e)
                return False

            self.db.commit()
            return True

    def update_mask(self, id, obj_id, x, y):
        with self.db.cursor() as cursor:
            try:
                query_head = 'UPDATE mask SET '
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
                print(e)
                return False

            self.db.commit()
            return True

    def list_mask(self):
        with self.db.cursor() as cursor:
            try:
                query = 'SELECT * FROM mask'
                cursor.execute(query)
                return list(cursor.fetchall())
            except:
                return None

    #-------------------------------------------------------------------------------------------------------------------
    # additional APIs
    def initialize(self):
        try:
            with self.db.cursor() as cursor:
                for i, sql in enumerate(querys.initial_queries):
                    print('{} 번째 sql 실행중...'.format(i + 1))
                    cursor.execute(sql)

                cursor.execute("SHOW TABLES")
                for line in cursor.fetchall():
                    print(line)

        except:
            print('your database is already exist')

        finally:
            self.db.commit()

    def list_mask(self, obj_id):
        print('now working on..')
