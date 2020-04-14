initial_queries = list()

# table environment
create_env_sql="""
CREATE TABLE environment(
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
ipv4 INT UNSIGNED NOT NULL,
floor INT UNSIGNED NOT NULL,
width INT UNSIGNED NOT NULL,
height INT UNSIGNED NOT NULL,
depth INT UNSIGNED NOT NULL,
PRIMARY KEY(id)
)"""
initial_queries.append(create_env_sql)

# table image
create_img_sql="""
CREATE TABLE image(
env_id INT UNSIGNED NOT NULL,
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
data longblob NOT NULL,
type INT UNSIGNED NOT NULL,
PRIMARY KEY(id),
FOREIGN KEY(env_id)
    REFERENCES environment(id)
)"""
initial_queries.append(create_img_sql)

# table grid
create_grid_sql="""
CREATE TABLE grid(
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
width INT UNSIGNED NOT NULL,
height INT UNSIGNED NOT NULL,
PRIMARY KEY(id)
)"""
initial_queries.append(create_grid_sql)

# table location
create_loc_sql="""
CREATE TABLE location(
grid_id INT UNSIGNED NOT NULL,
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
x INT UNSIGNED NOT NULL,
y INT UNSIGNED NOT NULL,
PRIMARY KEY(id),
FOREIGN KEY(grid_id)
    REFERENCES grid(id)
)"""
initial_queries.append(create_loc_sql)

# table super_class
create_superCategories_sql="""
CREATE TABLE super_class(
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
name CHAR(50) NOT NULL,
PRIMARY KEY(id)
)"""
initial_queries.append(create_superCategories_sql)

# table class
create_categories_sql="""
CREATE TABLE class(
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
super_id INT UNSIGNED NOT NULL,
name CHAR(50) NOT NULL,
width INT UNSIGNED NOT NULL,
height INT UNSIGNED NOT NULL,
depth INT UNSIGNED NOT NULL,
thumbnail blob,
PRIMARY KEY(id),
FOREIGN KEY(super_id)
    REFERENCES super_class(id)
)"""
initial_queries.append(create_categories_sql)

# table object
create_object_sql="""
CREATE TABLE object(
img_id INT UNSIGNED NOT NULL,
loc_id INT UNSIGNED NOT NULL,
class_id INT UNSIGNED NOT NULL,
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
PRIMARY KEY(id),
FOREIGN KEY(img_id)
    REFERENCES image(id) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY(loc_id)
    REFERENCES location(id) ON UPDATE CASCADE ON DELETE CASCADE,
FOREIGN KEY(class_id)
    REFERENCES class(id) ON UPDATE CASCADE ON DELETE CASCADE
)"""
initial_queries.append(create_object_sql)


# table bbox
create_bbox_sql="""
CREATE TABLE bbox(
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
obj_id INT UNSIGNED NOT NULL,
x INT UNSIGNED NOT NULL,
y INT UNSIGNED NOT NULL,
width INT UNSIGNED NOT NULL,
height INT UNSIGNED NOT NULL,
PRIMARY KEY(id),
FOREIGN KEY(obj_id)
    REFERENCES object(id) ON UPDATE CASCADE ON DELETE CASCADE
)"""
initial_queries.append(create_bbox_sql)

# table mask
create_mask_sql="""
CREATE TABLE mask(
id INT UNSIGNED NOT NULL AUTO_INCREMENT,
obj_id INT UNSIGNED NOT NULL,
x INT UNSIGNED NOT NULL,
Y INT UNSIGNED NOT NULL,
PRIMARY KEY(id),
FOREIGN KEY(obj_id)
    REFERENCES object(id) ON UPDATE CASCADE ON DELETE CASCADE
)"""
initial_queries.append(create_mask_sql)