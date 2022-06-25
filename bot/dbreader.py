import psycopg2
import sys


def db_reader(word):
    try:
        conn = psycopg2.connect(
                dbname='d1hfd95bsculk1', user='zkdwfesfnlqxik', 
                password='18832829be26b7b27a99b2f6cb1e5d8bc49398fbcd01ad1e2d3aacc1af772ca4',
                host='ec2-34-200-35-222.compute-1.amazonaws.com')
    except psycopg2.OperationalError as er:
        sys.exit(1)

    cursor = conn.cursor()

    query = 'SELECT DISTINCT genre FROM {}'.format(word)

    cursor.execute(query)

    data = cursor.fetchall()

    return data


def genre_constructor(table, genre):
    try:
        conn = psycopg2.connect(
                dbname='d1hfd95bsculk1', user='zkdwfesfnlqxik', 
                password='18832829be26b7b27a99b2f6cb1e5d8bc49398fbcd01ad1e2d3aacc1af772ca4',
                host='ec2-34-200-35-222.compute-1.amazonaws.com')
    except psycopg2.OperationalError as er:
        sys.exit(1)

    cursor = conn.cursor()

    query = "SELECT author, image, link, description FROM {} WHERE genre = '{}'".format(table, genre)

    cursor.execute(query)

    data = cursor.fetchall()

    return data


def comm_dispath(id):
    try:
        conn = psycopg2.connect(
                dbname='d1hfd95bsculk1', user='zkdwfesfnlqxik', 
                password='18832829be26b7b27a99b2f6cb1e5d8bc49398fbcd01ad1e2d3aacc1af772ca4',
                host='ec2-34-200-35-222.compute-1.amazonaws.com')
    except psycopg2.OperationalError as er:
        sys.exit(1)

    cursor = conn.cursor()
    conn.autocommit = True

    query = "INSERT INTO users (user_id) VALUES ({})".format(id)

    cursor.execute(query)
    cursor.close()
    conn.close()
