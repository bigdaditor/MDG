import random
import product_scrap
import sqlite3
import time
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

def generate_log():
    while True:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        # 유저 정보
        c.execute('SELECT username, email, address FROM users WHERE id =' + str(random.randint(1, 1000)))
        user = c.fetchone()
        log_message = dict()
        log_message['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        log_message['code'] = '200'
        log_message['message'] = 'success'
        log_message['user'] = {
            'username': user[0],
            'email': user[1],
            'address': user[2]
        }
        log_message['product'] = []

        for _ in range(random.randint(1, 10)):
            c.execute('SELECT name, price, '+ str(random.randint(1,5)) +' AS count FROM product WHERE id =' + str(random.randint(1, 50)))
            product = c.fetchone()
            log_message['product'].append({
                'name': product[0],
                'price': product[1],
                'count': product[2]
            })

        print(log_message)

        # 1초에서 10초 사이 무작위 주기로 대기
        wait_time = random.uniform(1, 10)
        time.sleep(wait_time)