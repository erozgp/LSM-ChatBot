import pymysql
import datetime

dt = datetime.datetime.now()

class DataBase:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='lsmchatbot_dev'
        )

        self.cursor = self.connection.cursor()

    def agregarUsuarios(self, users_dic):
        sql = "INSERT INTO usuarios(nombreusuario, identificador, inserted_at, updated_at) VALUES('{}', '{}', '{}', '{}')".format(users_dic["primer_nombre"], users_dic["id"], dt.strftime('%Y-%m-%d %H:%M:%S'), dt.strftime('%Y-%m-%d %H:%M:%S'))
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise

if __name__ == '__main__':
    print('Holaaa xd')
