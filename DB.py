import pymysql


class DB:
    """
    무슨일을 하는 클래스인지 적어주세요
    """
    def __init__(self, ip, port, user, password, db_name, charset='utf8'):
        """
        무슨일을 하는 함수인지 적어주세요

        Args:
            ip:
            port:
            user:
            password:
            db_name:
            charset:

        Returns:

        """

        self.db = pymysql.connect(host=str(ip), port=port, user=user, passwd=password, db=db_name, charset=charset)
        #-- let's think about cashing here --
        #--
        #--
        #-- ---------------------------------

    # environment table APIs
    def set_environment(self, ipv4, floor, width, height, depth):
        """
        무슨일을 하는 함수인지 적어주세요

        Args:
            ipv4:
            floor:
            width:
            height:
            depth:

        Returns:
        """
        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO environment(ipv4, floor, width, height, depth) VALUES(INET_ATON("%s"), %s, %s, %s, %s)'
                values = (ipv4, floor, width, height, depth)
                cursor.execute(query, values)
        except:
            return False

        finally:
            self.db.commit()
            return True

    def get_environment(self, id):
        """
        무슨일을 하는 함수인지 적어주세요

        Args:
            id:

        Returns:
        """
        # 'select * from environment where id = id'
        # return tuple type env data
        print('now working on')

    def delete_environment(self, id):
        """
        무슨일을 하는 함수인지 적어주세요

        Args:
            id:

        Returns:
        """
        # 'delete * from environment where id = id'
        # return True/False
        print('now working on')

    def update_environment(self, id, ipv4, floor, width, height, depth):
        """
        무슨일을 하는 함수인지 적어주세요

        Args:
            id:
            ipv4:
            floor:
            width:
            height:
            depth:

        Returns:
        """
        # 'update environment set ... where id = id
        # return True/False
        print('now working on')

    def list_environment(self):
        """
        무슨일을 하는 함수인지 적어주세요

        Args:

        Returns:
        """
        # 'select * from environment'
        # return tuple type lists
        print('now working on')

    def set_image(self, device_id, image, type):
        """
        무슨일을 하는 함수인지 적어주세요

        Args:
            device_id:
            image:
            type:
        Retruns:

        """
        if isinstance(image, str):
            try:
                with open(image, 'rb') as file:
                    image = file.read()
            except:
                print('invalid file name...')

        try:
            with self.db.cursor() as cursor:
                query = 'INSERT INTO image(env_id, data, type) VALUES(%s, %s, %s)'
                values = (device_id, image, type)
                cursor.execute(query, values)
        except:
            return False
        finally:
            self.db.commit()
            return True

    def get_image(self, id):
        print('now working on..')

    def delete_image(self, id):
        print('now working on..')

    def update_image(self, id, device_id, image, type):
        print('now working on..')

    def list_image(self):
        print('now working on..')

    def set_grid(self, width, height):
        print('now working on..')

    def get_grid(self, id):
        print('now working on..')

    def detete_grid(self, id):
        print('now working on..')

    def update_grid(self, id, width, height):
        print('now working on..')

    def list_grid(self):
        print('now working on..')

    def set_location(self, grid_id, loc_x, loc_y):
        print('now working on..')

    def get_location(self, id):
        print('now working on..')

    def delete_location(self, id):
        print('now working on..')

    def update_location(self, id, grid_id, loc_x, loc_y):
        print('now working on..')

    def list_location(self):
        print('now working on..')

    def set_superCategory(self, name):
        print('now working on..')

    def get_superCategory(self, id):
        print('now working on..')

    def delete_superCategory(self, id):
        print('now working on..')

    def update_superCategory(self, id, name):
        print('now working on..')

    def list_superCategory(self):
        print('now working on..')

    def set_category(self, super_id, name, width, height, depth, thumbnail):
        print('now working on..')

    def get_category(self, id):
        print('now working on..')

    def delete_category(self, id):
        print('now working on..')

    def update_category(self, id, super_id, name, width, height, depth, thumbnail):
        print('now working on..')

    def list_category(self):
        print('now working on..')

    def set_object(self, img_id, loc_id, category_id):
        print('now working on..')

    def get_object(self, id):
        print('now working on..')

    def delete_object(self, id):
        print('now working on..')

    def update_object(self, id, img_id, loc_id, category_id):
        print('now working on..')

    def list_object(self):
        print('now working on..')

    def set_bbox(self, obj_id, x, y, width, height):
        print('now working on..')

    def get_bbox(self, id):
        print('now working on..')

    def delete_bbox(self, id):
        print('now working on..')

    def update_bbox(self, id, x, y, width, height):
        print('now working on..')

    def list_bbox(self):
        print('now working on..')

    def set_mask(self, obj_id, x, y):
        print('now working on..')

    def get_mask(self, id):
        print('now working on..')

    def delete_mask(self, id):
        print('now working on..')

    def update_mask(self, id, obj_id, x, y):
        print('now working on..')

    def list_mask(self):
        print('now working on..')

    #-------------------------------------------------------------------------------------------------------------------
    # additional APIs
    def list_mask(self, obj_id):
        print('now working on..')


