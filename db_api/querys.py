# -*- coding: utf-8 -*-

initial_queries = list()

# table environment
create_env_sql="""
CREATE TABLE Environment(
env_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
ipv4 CHAR(50) NOT NULL,
floor SMALLINT UNSIGNED NOT NULL,
width SMALLINT UNSIGNED NOT NULL,
height SMALLINT UNSIGNED NOT NULL,
depth SMALLINT UNSIGNED NOT NULL,
PRIMARY KEY(env_id),
UNIQUE KEY UNIQUE_KEY (ipv4, floor)
) AUTO_INCREMENT=20001"""
initial_queries.append(create_env_sql)

# table Grid
create_grid_sql="""
CREATE TABLE Grid(
grid_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
width SMALLINT UNSIGNED NOT NULL,
height SMALLINT UNSIGNED NOT NULL,
PRIMARY KEY(grid_id),
UNIQUE KEY UNIQUE_KEY (width, height)
)"""
initial_queries.append(create_grid_sql)

# table SuperCategory
create_superCategories_sql="""
CREATE TABLE SuperCategory(
super_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
super_name VARCHAR(100) NOT NULL UNIQUE,
PRIMARY KEY(super_id)
)"""
initial_queries.append(create_superCategories_sql)

# table Image
create_img_sql="""
CREATE TABLE Image(
env_id INT UNSIGNED NOT NULL,
img_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
img MEDIUMBLOB NOT NULL,
type TINYINT UNSIGNED NOT NULL,
check_num TINYINT UNSIGNED NOT NULL,
PRIMARY KEY(img_id),
FOREIGN KEY FOREIGN_KEY (env_id) REFERENCES Environment(env_id) ON UPDATE CASCADE ON DELETE CASCADE
)"""
initial_queries.append(create_img_sql)

# table Location
create_loc_sql="""
CREATE TABLE Location(
grid_id INT UNSIGNED NOT NULL,
loc_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
x TINYINT UNSIGNED NOT NULL,
y TINYINT UNSIGNED NOT NULL,
PRIMARY KEY(loc_id),
FOREIGN KEY FOREIGN_KEY (grid_id) REFERENCES Grid(grid_id) ON UPDATE CASCADE ON DELETE CASCADE,
UNIQUE KEY UNIQUE_KEY (grid_id, x, y)
)"""
initial_queries.append(create_loc_sql)

# table class
create_categories_sql="""
CREATE TABLE Category(
super_id INT UNSIGNED NOT NULL,
cat_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
cat_name VARCHAR(100) NOT NULL,
width SMALLINT UNSIGNED NOT NULL,
height SMALLINT UNSIGNED NOT NULL,
depth SMALLINT UNSIGNED NOT NULL,
iteration TINYINT UNSIGNED NOT NULL,
thumbnail MEDIUMBLOB NOT NULL,
PRIMARY KEY(cat_id),
FOREIGN KEY FOREIGN_KEY (super_id) REFERENCES SuperCategory(super_id) ON UPDATE CASCADE ON DELETE CASCADE,
UNIQUE KEY UNIQUE_KEY (cat_name, super_id)
)"""
initial_queries.append(create_categories_sql)

# table Object
create_object_sql="""
CREATE TABLE Object(
img_id INT UNSIGNED,
loc_id INT UNSIGNED NOT NULL,
cat_id INT UNSIGNED NOT NULL,
obj_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
iteration INT UNSIGNED NOT NULL,
mix_num INT NOT NULL,
aug_num INT NOT NULL,
PRIMARY KEY(obj_id),
FOREIGN KEY FOREIGN_KEY_Image (img_id) REFERENCES Image(img_id) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY FOREIGN_KEY_Category (cat_id) REFERENCES Category(cat_id) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY FOREIGN_KEY_Location (loc_id) REFERENCES Location(loc_id) ON UPDATE CASCADE ON DELETE CASCADE,
UNIQUE KEY UNIQUE_KEY (loc_id, cat_id, iteration, mix_num)
)"""
initial_queries.append(create_object_sql)

# table Bbox
create_bbox_sql="""
CREATE TABLE Bbox(
obj_id INT UNSIGNED NOT NULL,
bbox_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
x SMALLINT UNSIGNED NOT NULL,
y SMALLINT UNSIGNED NOT NULL,
width SMALLINT UNSIGNED NOT NULL,
height SMALLINT UNSIGNED NOT NULL,
PRIMARY KEY(bbox_id),
FOREIGN KEY FOREIGN_KEY (obj_id) REFERENCES Object(obj_id) ON UPDATE CASCADE ON DELETE CASCADE,
UNIQUE KEY UNIQUE_KEY (obj_id)
)"""
initial_queries.append(create_bbox_sql)

# table Mask
create_mask_sql="""
CREATE TABLE Mask(
obj_id INT UNSIGNED NOT NULL,
mask_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
x SMALLINT UNSIGNED NOT NULL,
Y SMALLINT UNSIGNED NOT NULL,
PRIMARY KEY(mask_id),
FOREIGN KEY FOREIGN_KEY (obj_id) REFERENCES Object(obj_id) ON UPDATE CASCADE ON DELETE CASCADE
)"""
initial_queries.append(create_mask_sql)
