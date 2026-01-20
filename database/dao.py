from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_all_artists():

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT *
                FROM artist a
                """
        cursor.execute(query)
        for row in cursor:
            artist = Artist(id=row['id'], name=row['name'])
            result.append(artist)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artist_min_album(n_alb,id_map):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select tmp.aid
                    from (
                    select a.id as aid, count(*) as somma
                    from artist a, album a2 
                    where a.id=a2.artist_id 
                    group by aid 
                    having somma >= %s ) tmp

                """
        cursor.execute(query, (n_alb,))
        for row in cursor:

            result.append(id_map[row['aid']])
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artist_connessi(id_map):

        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select tmp1.aid as aid_uno, tmp2.aid as aid_due, count(*) as peso
                    from(select a.artist_id as aid, t.genre_id as genere
                    from track t, album a
                    where a.id = t.album_id
                    group by a.artist_id , t.genre_id) as tmp1,
                    (select a.artist_id as aid, t.genre_id as genere
                    from track t, album a
                    where a.id = t.album_id
                    group by a.artist_id , t.genre_id) as tmp2
                    where tmp1.aid < tmp2.aid
                    group by tmp1.aid, tmp2.aid
                """
        cursor.execute(query)
        for row in cursor:
            result.append((id_map[row['aid_uno']], id_map[row["aid_due"]], row["peso"]))
        cursor.close()
        conn.close()
        return result

