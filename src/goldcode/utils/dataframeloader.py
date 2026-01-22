import os
import pandas as pd
import logging
from goldcode.logging.setup import get_logger

class DataFrameLoader():

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

    
    def load_files_to_df(self, input_folder, exclude_ext = [], exclude_folders = []):
        """
        Load filepaths to df
        """

        try:

            rows = []
            counter = 0

            for dirpath, dirnames, filenames in os.walk(input_folder):

                # Exclude folders
                dirnames[:] = [d for d in dirnames if d not in exclude_folders]

                for f in filenames:
                    ext = os.path.splitext(f)[1]

                    # Exclude ext
                    if ext in exclude_ext:
                        continue

                    rows.append({
                        "filename": f,
                        "ext": ext,
                        "path": os.path.join(dirpath, f)
                    })

                    counter += 1

                    if counter % 5000 == 0:
                        self.logger.info(f"▶ Found files: {counter}")
                
                df = pd.DataFrame(rows)

                self.logger.info(f"✔ Found total {counter} files")

                return df

        except Exception as e:
            self.logger.error(e)
