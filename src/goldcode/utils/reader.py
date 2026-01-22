import os
import pandas as pd
import logging
from goldcode.logging.setup import get_logger

class Reader():

    def __init__(self, logger = None, log_path = None):
        self.logger = get_logger(
            name=self.__class__.__name__,
            logger=logger,
            log_path=log_path
        )

    def test_me(self):
        return 'Hey'
    
    def load_df_from_chunks(self, input_folder, ext='.parquet'):
        """
        Loading a folder with parquet files and returns a pandas df with all parquets merged.
        All parquets must contain the same columns
        """

        try:
            paths = []
            dfs = []

            for root, _, files in os.walk(input_folder):
                for f in files:
                    if f.endswith(ext):
                        full_path = os.path.join(root, f)
                        paths.append(full_path)

            path_count = len(paths)

            paths.sort()

            for i, path in enumerate(paths):
                df = pd.read_parquet(path)
                dfs.append(df)

                self.logger.info(f"▶ Read {i} out of {path_count} chunks")

            
            df_concat = pd.concat(dfs)

            self.logger.info(f"✔ Loaded all {ext} to df")

            return df_concat

        except Exception as e:
            self.logger.error(e)




                


