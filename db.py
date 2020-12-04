import psycopg2
import os

def get_songs_list(user_id):
    #check db_name
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost')
    cur = conn.cursor()

    q = f'''
    select track from
    user_track
    where user_id = {user_id}
    order by score desc
    '''
    cur.execute(q)
    music = cur.fetchall()

    path = '/Users/finlandcowboy/Desktop/research projects/Music player/database/wavs/'
    paths = []
    for track in music:
        for t in os.listdir(path):
            if t.startswith(str(track[0])) and t.endswith('wav'):
                paths.append(path + t)
    return paths


def create_user(user, pasw):
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost')
    cur = conn.cursor()
    q = f'''
    insert into users (username, password) select \'{user}\',\'{pasw}\'
    where not exists (
        select * from users where username = \'{str(user)}\'
    ) and \'{user}\' not in (select username from users)
    '''
    cur.execute(q)
    conn.commit()
    conn.close()
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost')
    cur = conn.cursor()
    cur.execute(f'select user_id from users where username = \'{user}\'')
    user_id = cur.fetchall()
    cur.execute('select concat(artist, \' - \', song) from tracks')
    tracks = cur.fetchall()
    users_tracks = []
    for user_ in user_id:
        for track in tracks:
            users_tracks.append((user_[0], track[0]))
    query = f'select user_id from users where username = \'{user}\''
    cur.execute(query)
    user_id_1 = cur.fetchall()[0][0]
    for elem in users_tracks:
        cur.execute('insert into user_track (user_id, track, score) select %s, %s, 0 where not exists (select user_id from user_track where user_id = %s group by  user_id having count(user_id) > 100)', [user_id_1, elem[1], user_id_1])
        conn.commit()
    conn.close()



def get_user_id(user):
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost')
    cur = conn.cursor()
    query = f'select user_id from users where username = \'{user}\''
    cur.execute(query)
    user_id = cur.fetchall()[0][0]
    conn.close()
    return user_id



def set_like(user_id, track):
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='postgres', host='localhost')
    cur = conn.cursor()
    q = f'''
    update user_track
    set score = 1
    where score = 0
    and user_id = {user_id}
    and track like \'%{track}%\'
    '''
    cur.execute(q)
    conn.commit()
    conn.close()