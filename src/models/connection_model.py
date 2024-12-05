import psycopg

class UserConnection:
    def __init__(self):
        try:
            self.conn = psycopg.connect(
                dbname='easyfitpg', 
                user='emafer77',
                password='Maniola777', 
                host='localhost',
                port='5432'
            )
        except psycopg.OperationalError as err:
            print(f"Error de conexión: {err}")
            self.conn = None  
    
    def write(self, data):
        if self.conn:  
            try:
                with self.conn.cursor() as cur:
                    cur.execute("""
                        INSERT INTO usuarios (
                            nombre, apellidos, correo, contrasena, telefono, 
                            edad, genero, peso, altura, objetivo_id
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, data)
                    self.conn.commit()
            except psycopg.Error as e:
                print(f"Error en la consulta: {e}")
                self.conn.rollback() 
        else:
            print("Conexión no disponible.")
    
    def __del__(self):
        if self.conn:
            self.conn.close() 
    
    def read_all(self):
        if self.conn:
            try:
                with self.conn.cursor() as cur:
                    cur.execute("""SELECT * FROM usuarios""")
                    return cur.fetchall()
            except psycopg.Error as e:
                print(f"Error al leer datos: {e}")
                self.conn.rollback()  
        else:
            print("Conexión no disponible.")
            return None

    def read_one(self, id):
        if self.conn:
            try:
                with self.conn.cursor() as cur:
                    cur.execute("""SELECT * FROM usuarios WHERE id = %s""", (id,))
                    return cur.fetchone()
            except psycopg.Error as e:
                print(f"Error al leer el usuario: {e}")
                self.conn.rollback() 
        else:
            print("Conexión no disponible.")
            return None

    def delete(self, id):
        if self.conn:
            try:
                with self.conn.cursor() as cur:
                    cur.execute("""DELETE FROM usuarios WHERE id = %s""", (id,))
                    self.conn.commit() 
            except psycopg.Error as e:
                print(f"Error al eliminar el usuario: {e}")
                self.conn.rollback() 
        else:
            print("Conexión no disponible.")

    def update(self, data: dict):
        if self.conn:
            try:
                with self.conn.cursor() as cur:
                    cur.execute("""
                        UPDATE usuarios SET
                            nombre = %(nombre)s,
                            apellidos = %(apellidos)s,
                            correo = %(correo)s,
                            contrasena = %(contrasena)s,   
                            telefono = %(telefono)s,
                            edad = %(edad)s,
                            genero = %(genero)s,
                            peso = %(peso)s,
                            altura = %(altura)s,
                            objetivo_id = %(objetivo_id)s
                        WHERE id = %(id)s
                    """, data)
                    self.conn.commit() 
            except psycopg.Error as e:
                print(f"Error al actualizar el usuario: {e}")
                self.conn.rollback()  
        else:
            print("Conexión no disponible.")
