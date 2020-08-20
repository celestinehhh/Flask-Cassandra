# python
# -*- coding:utf-8 -*-
# author: GU　SIYUAN time:2020/8/10
import logging
from cassandra.cluster import Cluster

log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

KEYSPACE = "images"
cluster = Cluster(contact_points=['172.18.0.2'], port=9042)
session = cluster.connect()


def createKeySpace():
    log.info("Creating keyspace...")

    try:
        session.execute("""
           CREATE KEYSPACE %s
           WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
           """ % KEYSPACE)
        log.info("setting keyspace...")
        session.set_keyspace(KEYSPACE)
        log.info("creating table...")
        session.execute('''
        CREATE TABLE myClassification (
               Created_time text,
               image_name text,
               image_label text,
               PRIMARY KEY (Created_time)
           )''')

    except Exception as e:
        log.error("Unable to create keyspace")
        log.error(e)


def Insert(Created_time, image_name, image_label):
    try:
        session.set_keyspace(KEYSPACE)
        info = [Created_time, image_name, image_label]
        session.execute(
            """
            INSERT INTO myClassification (Created_time, image_name, image_label)
            VALUES (%s, %s, %s)
            """, info)
    except Exception as e:
        log.error("Unable to insert a picture")
        log.error(e)


def Show_All():
    session.set_keyspace(KEYSPACE)
    rows = session.execute('select * from myClassification')
    return rows
