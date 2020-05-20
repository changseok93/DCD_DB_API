def Object(Location = "1x2", super_category = "스낵", category = "육포", iteration = "1"):
    """
    조회하고 싶은 object의 속성들을 받아 해당하는 object의 id를 반환하는 함수

    Args:
        Location (str): 조회하기 원하는 object의 상위 location
        super_category (str): 조회하기 원하는 object의 상위 super_category
        category (str): 조회하기 원하는 object의 name
        iteration (str): 조회하기 원하는 object의 iteration
    Return:
        int : 해당 object의 id
    """
===========> 불가능, notion에 있는 DB Scheme 참조, 해당 정보를 얻기위해서는 더 많은 정보가 필요함


def check_object(Location = "1x2", super_category = "스낵", category = "육포", iteration = '1'):
    """
    조회하고 싶은 object들의 속성을 받아 해당하는 object가 존재하는지 반환하는 함수

    Args:
        Location (str): 조회하기 원하는 object의 상위 category
        super_category (str): 조회하기 원하는 object의 category의  super_category
        category (str): 조회하기 원하는 object의 category
        iteration (str): 조회하기 원하는 object의 iterarion

    Return:
        Bool : 해당하는 object가 존재하는지 반환
    """

===========> 불가능, notion에 있는 DB Scheme 참조, 해당 정보를 얻기위해서는 더 많은 정보가 필요함


#검수 완료된 오브젝트 반환
def allow_object_list(super_category = "스낵", cateory = "육포", grid = "3x3"):
    """
    super_category하위의 category를 속성으로 가지며, 입력받은 grid를 상위 그리드로 하는
    모든 location을 가지는 오브젝트들 중 검수완료된 이미지를 가지는 오브젝트들만 반환하는 함수

    Args:
        super_category (str): 조회하기 원하는 object의 super_category
        category (str): 조회하기 원하는 object의 category
        grid(str): 조회하기 원하는 object의 location이 가지는 상위 grid

    Return:
        list[object1, object2, ...]  : 검수 완료된 오브젝트들로 이루어진 1차원 리스트
    """

===========> 불가능, notion에 있는 DB Scheme 참조, 해당 정보를 얻기위해서는 더 많은 정보가 필요함

#검수 거절된 오브젝트 반환
def reject_object_list(super_category="스낵", cateory="육포", grid="3x3"):
    """
    super_category하위의 category를 속성으로 가지며, 입력받은 grid를 상위 그리드로 하는
    모든 location을 가지는 오브젝트들 중 검수거절된 이미지를 가지는 오브젝트들만 반환하는 함수

    Args:
        super_category (str): 조회하기 원하는 object의 super_category
        category (str): 조회하기 원하는 object의 category
        grid(str): 조회하기 원하는 object의 location이 가지는 상위 grid

    Return:
        list []  : 검수거절된 오브젝트들로 이루어진 1차원 리스트
    """
===========> 불가능, notion에 있는 DB Scheme 참조, 해당 정보를 얻기위해서는 더 많은 정보가 필요함

#검수되지 않은 오브젝트 반환
def nocheck_object_list(super_category="스낵", cateory="육포", grid="3x3"):
    """
    super_category하위의 category를 속성으로 가지며, 입력받은 grid를 상위 그리드로 하는 모든 location을 가지는 오브젝트들 중 검수되지 않은 이미지를 가지는 오브젝트들만 반환하는 함수

    Args:
        super_category (str): 조회하기 원하는 object의 super_category
        category (str): 조회하기 원하는 object의 category
        grid(str): 조회하기 원하는 object의 location이 가지는 상위 grid

    Return:
        list[object1, object2, ...]  : 검수되지 않은 오브젝트들로 이루어진 1차원 리스트
    """

    for location in len(gird):

        for iteration_ in "육포".iteration:

            object = object_list
            {location = location, iterarion = iteration_}
            image = image(object.image_id)
            if image.check_num == 0:
                reject_list.append(object)

    return reject_list

===========> 불가능, notion에 있는 DB Scheme 참조, 해당 정보를 얻기위해서는 더 많은 정보가 필요함

#검수 허락된 오브젝트를 제외한 오브젝트 반환
def recapture_object_list(super_category="스낵", cateory="육포", grid="3x3"):
    """
    super_category하위의 category를 속성으로 가지며, 입력받은 grid를 상위 그리드로 하는 모든 location을 가지는 오브젝트들 중 허락되지 않은 이미지를 가지는 오브젝트들만 반환하는 함수

    Args:
        super_category (str): 조회하기 원하는 object의 super_category
        category (str): 조회하기 원하는 object의 category
        grid(str): 조회하기 원하는 object의 location이 가지는 상위 grid
    Return:
        list[object1, object2, ...]  : 검수허락되지 않은 오브젝트들로 이루어진 1차원 리스트
    """
===========> 불가능, notion에 있는 DB Scheme 참조, 해당 정보를 얻기위해서는 더 많은 정보가 필요함

#카테고리와 그리드를 정하면 그리드의 모든 로케이션에 반복횟수 만큼의 오브젝트를 자동 생성
def set_object_list(super_category = "스낵", category = "육포", grid = "3x5"):
    """
    category와 grid를 입력으로 받아 해당 category와 grid로 만들 수 있는 모든 object를 생성하는 함수

    Args:
        super_category (str): 생성하고 싶은 object가 가지는 category가 가지는 상위 super_category
        category (str): 생성하고 싶은 object가 가지는 category
        grid (str): 생성하고 싶은 object의 location이 가지는 상위 grid
    """

    for location in len(gird):

        for iteration_ in "육포".iteration:

            set_object(image = "육포".thumbnail, category = "육포", location = location, iteration = iteration_)

            if object(image = "육포".thumbnail, category = "육포", location = locationm, iteration = iteration_) already exist:
                continue

===========> 이해가 잘 안되니 어떤 파라미터를 입력으로 줄지 DB scheme 기준으로 자세히 기술
