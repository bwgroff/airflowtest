from sqlalchemy import create_engine
from random import uniform, gauss


def fake_data(n_rows=1000):
    output = []
    for _ in xrange(n_rows):
        x = uniform(0, 10)
        y = gauss(x ** 2, 1)
        output.append((x, y))
    return output


if __name__ == '__main__':
    engine = create_engine('mysql://og:og@localhost/og')
    conn = engine.connect()
    conn.execute('create table if not exists fakedata (x double, y double);')

    data = fake_data()
    for x, y in data:
        conn.execute('insert into fakedata values ({}, {})'.format(x, y))
