initial_queries = list()

# table environment
create_env_sql="""
CREATE TABLE Environment(
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
ipv4 CHAR(50) NOT NULL,
floor SMALLINT UNSIGNED NOT NULL,
width SMALLINT UNSIGNED NOT NULL,
height SMALLINT UNSIGNED NOT NULL,
depth SMALLINT UNSIGNED NOT NULL,
PRIMARY KEY(id)
)"""
initial_queries.append(create_env_sql)

# table Image
create_img_sql="""
CREATE TABLE Image(
env_id INT UNSIGNED NOT NULL,
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
data LONGBLOB NOT NULL,
type TINYINT UNSIGNED NOT NULL,
check_num TINYINT UNSIGNED NOT NULL,
PRIMARY KEY(id),
FOREIGN KEY(env_id) REFERENCES Environment(id)
)"""
initial_queries.append(create_img_sql)

# table Grid
create_grid_sql="""
CREATE TABLE Grid(
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
width SMALLINT UNSIGNED NOT NULL,
height SMALLINT UNSIGNED NOT NULL,
PRIMARY KEY(id)
)"""
initial_queries.append(create_grid_sql)

# table Location
create_loc_sql="""
CREATE TABLE Location(
grid_id INT UNSIGNED NOT NULL,
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
x TINYINT UNSIGNED NOT NULL,
y TINYINT UNSIGNED NOT NULL,
PRIMARY KEY(id),
FOREIGN KEY(grid_id) REFERENCES Grid(id)
)"""
initial_queries.append(create_loc_sql)

# table super_class
create_superCategories_sql="""
CREATE TABLE SuperCategory(
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
name VARCHAR(100) NOT NULL,
PRIMARY KEY(id)
)"""
initial_queries.append(create_superCategories_sql)

# table class
create_categories_sql="""
CREATE TABLE Category(
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
super_id INT UNSIGNED NOT NULL,
name VARCHAR(100) NOT NULL,
width SMALLINT UNSIGNED NOT NULL,
height SMALLINT UNSIGNED NOT NULL,
depth SMALLINT UNSIGNED NOT NULL,
iteration TINYINT UNSIGNED NOT NULL,
thumbnail LONGBLOB,
PRIMARY KEY(id),
FOREIGN KEY(super_id) REFERENCES SuperCategory(id)
)"""
initial_queries.append(create_categories_sql)

# table Object
create_object_sql="""
CREATE TABLE Object(
img_id INT UNSIGNED NOT NULL,
loc_id INT UNSIGNED NOT NULL,
category_id INT UNSIGNED NOT NULL,
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
PRIMARY KEY(id),
FOREIGN KEY(img_id) REFERENCES Image(id) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY(loc_id) REFERENCES Location(id) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY(category_id) REFERENCES Category(id) ON UPDATE CASCADE ON DELETE CASCADE
)"""
initial_queries.append(create_object_sql)

# table Bbox
create_bbox_sql="""
CREATE TABLE Bbox(
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
obj_id INT UNSIGNED NOT NULL,
x SMALLINT UNSIGNED NOT NULL,
y SMALLINT UNSIGNED NOT NULL,
width SMALLINT UNSIGNED NOT NULL,
height SMALLINT UNSIGNED NOT NULL,
PRIMARY KEY(id),
FOREIGN KEY(obj_id) REFERENCES Object(id) ON UPDATE CASCADE ON DELETE CASCADE
)"""
initial_queries.append(create_bbox_sql)

# table Mask
create_mask_sql="""
CREATE TABLE Mask(
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
obj_id INT UNSIGNED NOT NULL,
x SMALLINT UNSIGNED NOT NULL,
Y SMALLINT UNSIGNED NOT NULL,
PRIMARY KEY(id),
FOREIGN KEY(obj_id) REFERENCES Object(id) ON UPDATE CASCADE ON DELETE CASCADE
)"""
initial_queries.append(create_mask_sql)