# "Database code" for the DB News.

import psycopg2

BDNAME = "news"


def get_article():
    db = psycopg2.connect(database=BDNAME)
    c = db.cursor()
    c.execute('''
        select articles.title as title,
        count(log.path) as views from articles
        join
        log on log.path like '%' || articles.slug
        group by articles.title
        order by views desc limit 3''')
    return c.fetchall()
    db.close()


def get_author():
    db = psycopg2.connect(database=BDNAME)
    c = db.cursor()
    c.execute('''select authors.name as name, count(log.path) as views
        from articles
        join log on log.path like '%' || articles.slug
        join authors on authors.id = articles.author
        group by authors.name
        order by views desc''')
    return c.fetchall()
    db.close()


def get_error():
    db = psycopg2.connect(database=BDNAME)
    c = db.cursor()
    c.execute('''
        create view total_requests as select time::date as date,
        count(*) as total,
        sum((status != '200 OK')::int)::float as err
        from log
        group by date order by total desc
    ''')
    c.execute('''
        select date,
        (err/total)*100 as percentual
        from total_requests
        where ((err/total)*100) > 1
    ''')
    return c.fetchall()
    db.close()
