import random
import product_scrap
from faker import Faker

fake = Faker('ko_KR')

# 유저 - 이름, 이메일, 비밀번호, 전화번호 생성
def generate_user():
    name = fake.name()
    email = fake.email()
    password = fake.password()
    return name, email, password

# 도로명 주소 랜덤으로 선택
def generate_address():
    address_file = open('address.txt', 'r', encoding='utf-8')
    address_list = address_file.readlines()
    address_list = [address.rstrip() for address in address_list]
    random_line = random.choice(address_list)
    address_file.close()
    return random_line

def generate_product(keyword):
    results = product_scrap.search(keyword)
    return results