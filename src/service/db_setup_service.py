import os
import MySQLdb

class DatabaseSetupService:
    def __init__(self, mysql):
        self.mysql = mysql

    def setup_mysql_permissions(self):
        try:
            conn = MySQLdb.connect(
                host='localhost',
                user=os.getenv('MYSQL_USER'),
                passwd=os.getenv('MYSQL_PASSWORD')
            )
            cur = conn.cursor()
            
            cur.execute(f"GRANT ALL PRIVILEGES ON *.* TO 'alumind_user'@'localhost' WITH GRANT OPTION;")
            cur.execute(f"GRANT ALL PRIVILEGES ON {os.getenv('MYSQL_DB')}.* TO 'alumind_user'@'localhost';")
            
            cur.execute("FLUSH PRIVILEGES;")
            
            cur.close()
            conn.close()
            print("Permissões concedidas com sucesso ao usuário 'alumind_user'.")
        
        except MySQLdb.Error as e:
            print(f"Erro ao conceder permissões: {e}")

    def create_database(self):
        try:
            conn = MySQLdb.connect(
                host='localhost',
                user=os.getenv('MYSQL_USER'),
                passwd=os.getenv('MYSQL_PASSWORD')
            )
            cur = conn.cursor()
            
            cur.execute("SHOW DATABASES LIKE %s", (os.getenv('MYSQL_DB'),))
            result = cur.fetchone()

            if not result:
                cur.execute(f"CREATE DATABASE {os.getenv('MYSQL_DB')}")
                print(f"Banco de dados '{os.getenv('MYSQL_DB')}' criado com sucesso!")

            cur.close()
            conn.close()

        except MySQLdb.Error as e:
            print(f"Erro ao conectar ou criar banco de dados: {e}")

    def create_tables(self):
        try:
            conn = self.mysql.connection
            cur = conn.cursor()

            cur.execute("SHOW TABLES LIKE 'feedback'")
            feedback_table_exists = cur.fetchone()

            cur.execute("SHOW TABLES LIKE 'feature'")
            feature_table_exists = cur.fetchone()

            if not feedback_table_exists:
                cur.execute("""
                    CREATE TABLE feedback (
                id VARCHAR(100) PRIMARY KEY,
                feedback TEXT NOT NULL
                );

                """)
                print("Tabela 'feedback' criada com sucesso!")

            if not feature_table_exists:
                cur.execute("""
                    CREATE TABLE feature (
                    id VARCHAR(100),
                    sentiment VARCHAR(20) NOT NULL,
                    features JSON NOT NULL,
                    PRIMARY KEY (id),
                    FOREIGN KEY (id) REFERENCES feedback(id) ON DELETE CASCADE
                    );
                """)
                print("Tabela 'feature' criada com sucesso!")

            cur.close()
        
        except MySQLdb.Error as e:
            print(f"Erro ao verificar ou criar tabelas: {e}")