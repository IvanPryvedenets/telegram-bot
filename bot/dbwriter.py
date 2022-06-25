import psycopg2


def writer(*args, **kwargs):

    conn = psycopg2.connect(
                dbname='d1hfd95bsculk1', user='zkdwfesfnlqxik', 
                password='18832829be26b7b27a99b2f6cb1e5d8bc49398fbcd01ad1e2d3aacc1af772ca4',
                host='ec2-34-200-35-222.compute-1.amazonaws.com')
                
    cursor = conn.cursor()

    conn.autocommit = True

    with open('bot/dataFiles/музика.txt', 'r') as a, \
            open('bot/dataFiles/фільми.txt', 'r') as b, \
            open('bot/dataFiles/книги.txt', 'r') as c, \
            open('bot/dataFiles/youtube.txt', 'r') as d:

        data = (a, b, c, d)

        i = 0

        while i < 4:
            for line in data[i].readlines():
                file = data[i].name.split('/')[-1]
                file = file.split('.')[0]

                insert = line.split(', ')

                query = 'INSERT INTO {} (author, image, genre, link, description) VALUES (%s, %s, %s, %s, %s)'.format(file)

                cursor.execute(query, insert)

            i += 1

    cursor.close()
    conn.close()
