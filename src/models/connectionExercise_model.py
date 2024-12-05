import psycopg
class ExerciseConnection:
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
    
    def execute_query(self, query, params=None, fetch=False):
        """Método general para ejecutar consultas con parámetros y manejar errores"""
        if self.conn:
            try:
                with self.conn.cursor() as cur:
                    cur.execute(query, params)
                    if fetch:
                        return cur.fetchall()
                    self.conn.commit()
            except psycopg.Error as e:
                print(f"Error en la consulta: {e}")
                self.conn.rollback()
        else:
            print("Conexión no disponible.")
    
    def write(self, data):
        """Método para insertar un ejercicio con video e imagen"""
        query = """
            INSERT INTO ejercicios (id_musculo, id_categoria, nombre, descripcion)
            VALUES (%s, %s, %s, %s) RETURNING id
        """
        
        exercise_id = self.execute_query(query, data[:4], fetch=True)[0][0]
        
        video_query = """
            INSERT INTO ejercicio_videos (ejercicio_id, video_url)
            VALUES (%s, %s)
        """
        self.execute_query(video_query, (exercise_id, data[4]))
        
        
        image_query = """
            INSERT INTO ejercicio_imagenes (ejercicio_id, image_url)
            VALUES (%s, %s)
        """
        self.execute_query(image_query, (exercise_id, data[5]))
        
        return exercise_id
    
    def read_all(self):
        """Método para obtener todos los ejercicios"""
        query = """
            SELECT e.id, e.id_musculo, e.id_categoria, e.nombre, e.descripcion, ev.video_url, ei.image_url
            FROM ejercicios e
            LEFT JOIN ejercicio_videos ev ON e.id = ev.ejercicio_id
            LEFT JOIN ejercicio_imagenes ei ON e.id = ei.ejercicio_id
        """
        return self.execute_query(query, fetch=True)
    
    def read_one(self, exercise_id: int):
        query = """
        SELECT e.id, e.id_musculo, e.id_categoria, e.nombre, e.descripcion, ev.video_url, ei.image_url
        FROM ejercicios e
        LEFT JOIN ejercicio_videos ev ON e.id = ev.ejercicio_id
        LEFT JOIN ejercicio_imagenes ei ON e.id = ei.ejercicio_id
        WHERE e.id = %s
    """
        result = self.execute_query(query, (exercise_id,), fetch=True)
        if not result:
            return None  
        return {
        "id": result[0][0],
        "id_musculo": result[0][1],
        "id_categoria": result[0][2],
        "nombre": result[0][3],
        "descripcion": result[0][4],
        "videoUrl": result[0][5],
        "imageUrl": result[0][6]
    }

    def delete(self, exercise_id: int):
        delete_video_query = "DELETE FROM ejercicio_videos WHERE ejercicio_id = %s"
        delete_image_query = "DELETE FROM ejercicio_imagenes WHERE ejercicio_id = %s"
        
        self.execute_query(delete_video_query, (exercise_id,))
        self.execute_query(delete_image_query, (exercise_id,))

        delete_query = "DELETE FROM ejercicios WHERE id = %s"
        self.execute_query(delete_query, (exercise_id,))
        
        return True
    
    def update(self, data):
        query = """
        UPDATE ejercicios
        SET id_musculo = %s, id_categoria = %s, nombre = %s, descripcion = %s
        WHERE id = %s
        """
        self.execute_query(query, data[:5])
        video_query = """
        UPDATE ejercicio_videos
        SET video_url = %s
        WHERE ejercicio_id = %s
        """
        self.execute_query(video_query, (data[5], data[4]))
        image_query = """
        UPDATE ejercicio_imagenes
        SET image_url = %s
        WHERE ejercicio_id = %s
        """
        self.execute_query(image_query, (data[6], data[4]))
        return True

