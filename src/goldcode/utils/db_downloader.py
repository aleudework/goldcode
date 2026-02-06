"""
Skal omstruktureres og med kommentarer
"""


import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging
import pandas as pd

class DBDownloader():
    def __init__(self, server = None, database = None, username = None, password = None, conn_str = None):
        self.server = server or os.getenv('SERVER_KONV_DB')
        self.database = database or os.getenv('DATABASE_KONV_DB')
        self.username = username or os.getenv('USERNAME_KONV_DB')
        self.password = password or os.getenv('PASSWORD_KONV_DB')
        self.conn_str = conn_str or (
        f"mssql+pyodbc://{self.username}:{self.password}@{self.server}:1433/{self.database}"
        "?driver=ODBC+Driver+18+for+SQL+Server"
        "&TrustServerCertificate=yes")

    def set_default_konv_db(self):
        try:
            server = os.getenv('SERVER_KONV_DB')
            database = os.getenv('DATABASE_KONV_DB')
            username = os.getenv('USERNAME_KONV_DB')
            password = os.getenv('PASSWORD_KONV_DB')

            conn_str = (
                f"mssql+pyodbc://{username}:{password}@{server}:1433/{database}"
                "?driver=ODBC+Driver+18+for+SQL+Server"
                "&TrustServerCertificate=yes")
        
            self.conn_str = conn_str

        except Exception as e:
            print(e)
    
    def set_default_eg_konv(self):
        try:
            server = os.getenv('SERVER_KONV_DB')
            database = os.getenv('EG_KONV_DB')
            username = os.getenv('USERNAME_KONV_DB')
            password = os.getenv('PASSWORD_KONV_DB')

            conn_str = (
                f"mssql+pyodbc://{username}:{password}@{server}:1433/{database}"
                "?driver=ODBC+Driver+18+for+SQL+Server"
                "&TrustServerCertificate=yes")
        
            self.conn_str = conn_str

        except Exception as e:
            print(e)
    
        
    def set_default_eg_prod(self):
        try:
            server = os.getenv('SERVER_PROD')
            database = os.getenv('EG_PROD_DB')
            username = os.getenv('USERNAME_KONV_DB')
            password = os.getenv('PASSWORD_KONV_DB')

            conn_str = (
                f"mssql+pyodbc://{username}:{password}@{server}:1433/{database}"
                "?driver=ODBC+Driver+18+for+SQL+Server"
                "&TrustServerCertificate=yes")
        
            self.conn_str = conn_str

        except Exception as e:
            print(e)
    


            
    def test_connection(self, conn_str=None):
        """
        Test connection to DB
        """
        try:
            if conn_str is None:
                conn_str = self.conn_str

            engine = create_engine(conn_str)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("DB-forbindelse OK")
        except SQLAlchemyError as e:
            print("DB-forbindelse fejlede:", e)

    def sql(self, sql, log_path=None, conn_str=None):
        """
        Docstring for download_from_sql_query
        
        :param self: Description
        :param sql: Description
        :param outfile: Description
        :param log_path: Description
        :param conn_str: Description
        """

        # --- Logging setup --- #
        # Opret log handler (der kommer to, én til terminal og én til log-fil)
        log_handlers = []
        # Håndter log fil
        if log_path:
            # log handler for file. Appender hvis filen eksisterer
            log_handlers.append(logging.FileHandler(log_path, mode='a', encoding='utf-8'))
        # Håndter terminal
        log_handlers.append(logging.StreamHandler())
        # Configurer log
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s: %(message)s",
            handlers=log_handlers
        )

        # Informer om tabel til upload
        logging.info(f"[INFO] Påbegynder download")
        
        try:
            engine = create_engine(self.conn_str)

            with engine.connect() as conn:

                df = pd.read_sql(
                    text(sql),
                    conn
                )

                logging.info(f"[INFO] Tabel hentet fra database")

                return df

        except Exception as e:

            logging.error(e)
            # Retunerer en tom df
            df = pd.DataFrame()
            return df

    def download_large_table(self, table_name, output_path, log_path=None, chunksize=1_000_000, conn_str=None):

        # Use class conn_str
        if conn_str is None:
            conn_str = self.conn_str

        # --- Logging setup --- #
        # Opret log handler (der kommer to, én til terminal og én til log-fil)
        log_handlers = []
        # Håndter log fil
        if log_path:
            # log handler for file. Appender hvis filen eksisterer
            log_handlers.append(logging.FileHandler(log_path, mode='a', encoding='utf-8'))
        # Håndter terminal
        log_handlers.append(logging.StreamHandler())
        # Configurer log
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s: %(message)s",
            handlers=log_handlers
        )

        # Informer om tabel til upload
        logging.info(f"[INFO] Påbegynder download af {table_name}")

        # --- Egentlig logik ---

        sql = f"SELECT * FROM {table_name}"
        
        if not os.path.isdir(output_path):
            print(f"Output mappe eksisterer ikke")
            return
        
        try:
            # Initilisere engine til database
            engine = create_engine(conn_str)

            with engine.connect() as conn:

                # Definerer en chunk. Opretter en generator (som først kaldes i loopet
                # Lidt som pandas i forvejen definerer noget og først eksekveres ved specifikke funktioner)
                chunks = pd.read_sql(
                    text(sql),
                    conn,
                    chunksize=chunksize
                )

                for i, chunk in enumerate(chunks):
                    path = os.path.join(output_path, f"{table_name}_{i}.parquet")
                    chunk.to_parquet(path, index=False)
                    logging.info(f"[GEMT] Chunk nr: {i}, I alt {len(chunk)} rækker, path: {path}")


            logging.info(f"[FÆRDIG] Download er kørt færdigt")

        except SQLAlchemyError as e:
            logging.error(f"FEJL i DB-Motor: {e}")


