import os
import django
import csv
import sys
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chanel.settings")
django.setup()

from products.models import *
from attributes.models import *

CSV_PATH_LOOK = './looks_products.csv'
CSV_PATH_PRODUCT = './final_products_info.csv'
CSV_PATH_ALLPRODUCT = './final_chanel.csv'

def look_csv_deco(func):
    def wrapper(*args, **kwargs):
        with open(CSV_PATH_LOOK) as in_file:
            data_reader = csv.reader(in_file)
            next(data_reader, None)
            return func(data_reader, *args, **kwargs)
    return wrapper
    return look_csv_deco

def product_csv_deco(func):
    def wrapper(*args, **kwargs):
        with open(CSV_PATH_PRODUCT) as in_file:
            data_reader = csv.reader(in_file)
            next(data_reader, None)
            return func(data_reader, *args, **kwargs)
    return wrapper
    return product_csv_deco

def allproduct_csv_deco(func):
    def wrapper(*args, **kwargs):
        with open(CSV_PATH_ALLPRODUCT) as in_file:
            data_reader = csv.reader(in_file)
            next(data_reader, None)
            return func(data_reader, *args, **kwargs)
    return wrapper
    return allproduct_csv_deco

category_list = {
    '레디 투 웨어' : [
        '자켓',
        '드레스',
        '블라우스와 탑',
        '가디건 & 점퍼',
        '스커트',
        '팬츠 & 점프 수트',
        '아우터',
        '수영복',
        '니트웨어',
        '레더'
    ],
    '핸드백' : [
        '시즌 신상품',
        '클래식 플랩 백',
        '2.55 플랩 백',
        'Chanel 19 백',
        '샤넬 가브리엘 백',
        '보이 샤넬 플랩 백'
    ],
    '액세서리' : [
        '슈즈',
        '지갑',
        '커스텁 주얼리',
        '스카프',
        '모자',
        '까멜리아',
        '벨트'
    ],
    '아이웨어' : [
        '선글라스',
        '옵티컬'
    ]
}

def menu(dataset):
    for data in dataset.keys():
        Menu.objects.create(name=data)

    table_rows = Menu.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.name}')
    print('----------------------')

    return print('Create data to [Menu] table')

def category(dataset):
    for data in dataset.keys():
        values = dataset[data]
        for value in values:
            menu_id = Menu.objects.get(name=data).id
            Category.objects.create(name=value, menu_id=menu_id)

    table_rows = Category.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.name} | {table_row.menu.id}')
    print('----------------------')

    return print('Create data to [Category] table')

@allproduct_csv_deco
def collection(csv_data):
    collection_list = []
    for row in csv_data:
        collection_list.append(row[4])

    collections = set(collection_list)
    for collection in collections:
        Collection.objects.create(name=collection)

    table_rows = Collection.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.name}')
    print('----------------------')

    return print('Create data to [Collection] table')

@allproduct_csv_deco
def product(csv_data):
    for row in csv_data:
        code = row[0]
        name = row[1]
        price = row[2]
        price = re.compile('[가-힣 | ₩ |, ]+' ).sub('', price)
        if not price:
            price = 0
        else:
            price = int(price)
        collection = row[4]
        unique_id = row[9]
        collection_id = Collection.objects.get(name=collection).id
        Product.objects.create(
            product_code    = code,
            name            = name,
            price           = price,
            collection_id   = collection_id,
            unique_id       = unique_id
        )

    table_rows = Product.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.unique_id} | {table_row.product_code} | {table_row.name} | {table_row.price} | {table_row.collection.id} ( {table_row.collection.name} )')
    print('----------------------')

    return print('Create data to [Product] table')

@allproduct_csv_deco
def product_category(csv_data):
    product_info = {}
    for row in csv_data:
        code = row[0]
        category = row[8]
        if category:
            product_info[code] = []
            items = category.split(',')
            for item in items:
                product_info[code].append(item.strip())

    for product in product_info.keys():
        product_id = Product.objects.get(product_code = product.id)
        for category in product_info[product]:
            category_id = Category.objects.get(name=category).id
            ProductCategory.objects.create(
                product_id = product_id,
                category_id = category_id
            )

    table_rows = ProductCategory.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.product.id} ({table_row.product.name})| {table_row.category.id} ({table_row.category.name})|')
    print('----------------------')

    return print('Create data to [CategoryProduct] table')

@look_csv_deco
def look(csv_data):
    names = []
    for row in csv_data:
        name = row[2]
        names.append(name)
    names = set(names)
    for name in names:
        collection_id = Collection.objects.get(id=1).id
        Look.objects.create(
            name = name,
            collection_id = collection_id
        )

    table_rows = Look.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.name} | {table_row.collection.id} ( {table_row.collection.name} )')
    print('----------------------')

    return print('Create data to [Look] table')

@allproduct_csv_deco
def product_look(csv_data):
    for row in csv_data:
        unique_id = row[9]
        look = row[3]
        if look:
            product_id = Product.objects.get(unique_id=unique_id).id
            look_id = Look.objects.get(name=look).id
            ProductLook.objects.create(
                product_id = product_id,
                look_id = look_id
            )

    table_rows = ProductLook.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.product} ({table_row.product.name})| {table_row.look} ({table_row.look.name})')
    print('----------------------')

    return print('Create data to [ProductLook] table')

@allproduct_csv_deco
def look_image(csv_data):
    look_image = {}
    for row in csv_data:
        name = row[3]
        images = row[7]
        images = images.replace('[','')
        images = images.replace(']','')
        images = images.replace(images[0], '')
        if name:
            look_image[name] = []
            for image in images.split(' '):
                if image[-1] == ',':
                    image.replace('jpg,', 'jpg')
                look_image[name].append(image)

    for lookname in look_image.keys():
        look_id = Look.objects.get(name=lookname).id
        for lookimage in look_image[lookname]:
            LookImage.objects.create(
                url=lookimage,
                look_id=look_id
            )

    table_rows = LookImage.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.look} ({table_row.look.name})| {table_row.url}')
    print('----------------------')

    return print('Create data to [LookImage] table')

@product_csv_deco
def product_image(csv_data):
    product_image = {}
    for row in csv_data:
        code = row[0]
        images = row[9]
        images = images.replace('[','')
        images = images.replace(']','')
        images = images.replace(images[0], '')
        if code:
            product_image[code] = []
            for image in images.split(' '):
                if image[-1] == ',':
                    image.replace('jpg,', 'jpg')
                product_image[code].append(image)

    for productcode in product_image.keys():
        product_id = Product.objects.get(product_code=productcode).id
        for productimage in product_image[productcode]:
            ProductImage.objects.create(
                url=productimage,
                product_id=product_id
            )

    table_rows = ProductImage.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.product} ({table_row.product.name})| {table_row.url}')
    print('----------------------')

    return print('Create data to [ProductImage] table')


@product_csv_deco
def size(csv_data):
    size_data = {}
    for row in csv_data:
        size_main = row[7]
        size_sub = row[8]
        size_data[size_main] = size_sub

    for size in size_data.keys():
        Size.objects.create(
            size_main = size,
            size_sub  = size_data[size]
        )

    table_rows = Size.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.size_main} | {table_row.size_sub}')
    print('----------------------')

    return print('Create data to [Size] table')

@product_csv_deco
def size_product(csv_data):
    for row in csv_data:
        code = row[0]
        size = row[7]
        product_id = Product.objects.get(product_code=code).id
        size_id = Size.objects.get(size_main=size).id
        SizeProduct.objects.create(
            product_id = product_id,
            size_id = size_id
        )

    table_rows = SizeProduct.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.product} ({table_row.product.name})| {table_row.size} ({table_row.size.size_main})')
    print('----------------------')

    return print('Create data to [SizeProduct] table')

@product_csv_deco
def material(csv_data):
    names = []
    for row in csv_data:
        name = row[4]
        names.append(name)
    names = set(names)

    for material in names:
        Material.objects.create(name=material)

    table_rows = Material.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.name} |')
    print('----------------------')

    return print('Create data to [Material] table')


@product_csv_deco
def material_product(csv_data):
    for row in csv_data:
        code = row[0]
        material = row[4]
        product_id = Product.objects.get(product_code=code).id
        material_id = Material.objects.get(name = material).id
        MaterialProduct.objects.create(
            product_id = product_id,
            material_id = material_id
        )

    table_rows = MaterialProduct.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.product} ({table_row.product.name})| {table_row.material} ({table_row.material.name})')
    print('----------------------')

    return print('Create data to [MaterialProduct] table')

@allproduct_csv_deco
def texture(csv_data):
    textures = []
    for row in csv_data:
        name = row[5]
        items = name.split(',')
        for item in items:
            textures.append(item.strip())
    textures = set(textures)

    for texture in textures:
        Texture.objects.create(name=texture)

    table_rows = Texture.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.name} | ')
    print('----------------------')

    return print('Create data to [Texture] table')


@allproduct_csv_deco
def texture_product(csv_data):
    items = {}
    for row in csv_data:
        unique_id = row[9]
        name = row[5]
        items[unique_id] = []
        textures = name.split(',')
        for texture in textures:
            items[unique_id].append(texture.strip())

    for item in items.keys():
        product_id = Product.objects.get(unique_id=item).id
        for texture in items[item]:
            texture_id = Texture.objects.get(name=texture).id
            TextureProduct.objects.create(
                product_id = product_id,
                texture_id = texture_id
            )

    table_rows = TextureProduct.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.product} ({table_row.product.name})| {table_row.texture} ({table_row.texture.name})')
    print('----------------------')

    return print('Create data to [TextureProduct] table')

@product_csv_deco
def shape(csv_data):
    shapes = []
    for row in csv_data:
        name = row[10]
        shapes.append(name)
    shapes = set(shapes)

    for shape in shapes:
        Shape.objects.create(name=shape)

    table_rows = Shape.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.name} |')
    print('----------------------')

    return print('Create data to [Shape] table')

@product_csv_deco
def shape_product(csv_data):
    for row in csv_data:
        code = row[0]
        shape = row[10]
        product_id = Product.objects.get(product_code = code).id
        shape_id = Shape.objects.get(name = shape).id
        ShapeProduct.objects.create(
            product_id = product_id,
            shape_id = shape_id
        )

    table_rows = ShapeProduct.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.product} ({table_row.product.name}) | {table_row.shape} ({table_row.shape.name}) |')
    print('----------------------')

    return print('Create data to [ShapeProduct] table')

@allproduct_csv_deco
def color(csv_data):
    colors = []
    for row in csv_data:
        items = row[6]
        items = items.split(',')
        for item in items:
            colors.append(item.strip())
    colors = set(colors)

    for color in colors:
        Color.objects.create(name=color)

    table_rows = Color.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.name} |')
    print('----------------------')

    return print('Create data to [Color] table')

@allproduct_csv_deco
def color_product(csv_data):
    products = {}
    for row in csv_data:
        unique_id = row[9]
        item = row[6]
        products[unique_id] = []
        colors = item.split(',')
        for color in colors:
            products[unique_id].append(color.strip())

    for product in products.keys():
        product_id = Product.objects.get(unique_id=product).id
        for color in products[product]:
            color_id = Color.objects.get(name=color).id
            ColorProduct.objects.create(
                product_id = product_id,
                color_id = color_id
            )

    table_rows = ColorProduct.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.product} ({table_row.product.name}) | {table_row.color} ({table_row.color.name}) |')
    print('----------------------')

    return print('Create data to [ColorProduct] table')


@product_csv_deco
def theme(csv_data):
    themes = []
    for row in csv_data:
        theme = row[2]
        itmes = theme.split(',')
        for item in itmes:
            themes.append(item.strip())
    themes = set(themes)

    for theme in themes:
        Theme.objects.create(name=theme)

    table_rows = Theme.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.name} |')
    print('----------------------')

    return print('Create data to [Theme] table')


@product_csv_deco
def theme_product(csv_data):
    products = {}
    for row in csv_data:
        code = row[0]
        themes = row[2]
        products[code] = []
        themes = themes.split(',')
        for theme in themes:
            products[code].append(theme.strip())

    for product in products.keys():
        product_id = Product.objects.get(product_code = product).id
        for theme in products[product]:
            theme_id = Theme.objects.get(name=theme).id
            ThemeProduct.objects.create(
                product_id = product_id,
                theme_id = theme_id
            )

    table_rows = ThemeProduct.objects.all()
    print('----------------------')
    for table_row in table_rows:
        print(f'{table_row.id} | {table_row.product} ({table_row.product.name}) | {table_row.theme} ({table_row.theme.name}) |')
    print('----------------------')

    return print('Create data to [ThemeProduct] table')


def choice_db():
    print("""
          1. Menu
          2. Category
          3. Collection
          4. Product
          5. ProductCategory
          6. Look
          7. ProductLook
          8. LookImage
          9. ProductImage
          10. Size
          11. SizeProduct
          12. Material
          13. MaterialProduct
          14. Texture
          15. TextureProduct
          16. Shape
          17. ShapeProduct
          18. Color
          19. ColorProduct
          20. Theme
          21. ThemeProduct
          0. EXIT
          """)
    choice = int(input('데이터를 생성할 테이블을 입력하세요 : '))
    return choice


def create_db():
    choice = choice_db()
    if choice == 1:
        menu(category_list)
    elif choice == 2:
        category(category_list)
    elif choice == 3:
        collection()
    elif choice == 4:
        product()
    elif choice == 5:
        product_category()
    elif choice == 6:
        look()
    elif choice == 7:
        product_look()
    elif choice == 8:
        look_image()
    elif choice == 9:
        product_image()
    elif choice == 10:
        size()
    elif choice == 11:
        size_product()
    elif choice == 12:
        material()
    elif choice == 13:
        material_product()
    elif choice == 14:
        texture()
    elif choice == 15:
        texture_product()
    elif choice == 16:
        shape()
    elif choice == 17:
        shape_product()
    elif choice == 18:
        color()
    elif choice == 19:
        color_product()
    elif choice == 20:
        theme()
    elif choice == 21:
        theme_product()
    elif choice == 0:
        print("GOOD BYE")
    else:
        print('입력값이 잘못되었습니다.')
        create_db()

create_db()
