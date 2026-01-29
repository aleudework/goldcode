import pandas as pd
import csv
import re


class CSVDecoder():

    def __init__(self, encoder = 'cp1252', seperator=';', regex="^000\d{9}$", max_number_of_col = 1000, start_row=0):
        self.encoder = encoder
        self.seperator = seperator
        self.regex = regex # Regex til at angive split
        self.max_number_of_col = max_number_of_col
        self.start_row = start_row

    def extract_from_csv(self, input_csv: None, encoder: None, seperator: None, regex: None, max_number_of_col: None, start_row: None):
        """
        Docstring for fix_csv
        
        :param self: Description
        :param input_csv: Description
        :type input_csv: None
        """
        # Set objekt hvis værdier udfyldt
        try:
            if encoder:
                self.encoder = encoder
            if seperator:
                self.seperator = seperator
            if regex:
                self.regex = regex
            if max_number_of_col:
                self.max_number_of_col = max_number_of_col
            if start_row:
                self.start_row = start_row

            # Hent column names
            columns = self.get_column_names(input_csv)

            # Hent CSV data
            text_splitted = self.read_csv(input_csv)

            # Clean CSV data
            text_cleaned = self.clean_for_special_characters(text_splitted)

            lines = self.build_lines(text_cleaned, self.regex, self.start_row)

            # Merger for lange lines
            final_lines = self.match_lines_to_column(lines, columns)

            return columns, final_lines

        except Exception as e:
            print(e)

    def get_column_names(self, input_csv: None):
        """
        Retunerer kolonneoverskrifter fra CSV
        """
        try:
            with open(input_csv, encoding=self.encoder, errors="ignore") as f:
                header = f.readline()

            header = header.replace("\ufeff", "").strip() # Fjerner BOM
            columns = header.split(self.seperator)

            # Retunerer kun maks number of col, hvis der er sat en begrænsning
            return columns[:self.max_number_of_col]
            
        except Exception as e:
            print(e)

    def read_csv(self, input_csv):
        """
        Læs CSV og split tekst ind i et array ud fra en seperator
        """
        with open(input_csv, "r", encoding=self.encoder) as f:
            raw_text = f.read() # Læser filen som en lang streng
            
            # Fjern første række (header)
            raw_text = raw_text.split("\n", 1)[1]

            splited_text = raw_text.split(self.seperator) # Splitter strengen ud på elementer ud fra seperator
            return splited_text
    
    def clean_for_special_characters(self, input):
        """
        Renser for special characters i listen pr. element.
        """
        cleaned_list = []

        for text in input:
            cleaned_text = text.replace("\n", "")

            cleaned_list.append(cleaned_text)

        return cleaned_list


    def build_lines(self, input, regex, start_row=0):
        """
        Tager en 1D liste og laver den om til en 2D liste (linjer).

        Når regex matcher:
        - start_row = 0  → ny linje starter normalt
        - start_row < 0  → de sidste |start_row| elementer flyttes
                        fra forrige linje til den nye
        """

        lines = []            # Alle færdige linjer
        current_line = []     # Den linje vi er i gang med at bygge

        # Forbered regex én gang (hurtigere)
        pattern = re.compile(regex)

        # Gå igennem hvert element i input-listen
        for text in input:

            # Tjek om dette element matcher regex
            if pattern.search(text):

                # Hvis vi allerede har noget i current_line
                if current_line:

                    # Hvis start_row er negativ (fx -6)
                    # betyder det: flyt de sidste 6 elementer
                    # over i den nye linje
                    if start_row < 0:

                        # split_idx er negativt, fx -6
                        split_idx = start_row

                        # Tag de sidste |start_row| elementer
                        new_line = current_line[split_idx:]

                        # Behold resten i den gamle linje
                        current_line = current_line[:split_idx]

                        # Gem den gamle linje
                        lines.append(current_line)

                        # Start ny linje med de flyttede elementer
                        current_line = new_line

                    else:
                        # Normal opførsel:
                        # afslut nuværende linje og start en ny
                        lines.append(current_line)
                        current_line = []

            # Tilføj nuværende element til current_line
            # (regex-elementet kommer med i den nye linje)
            current_line.append(text)

        # Til sidst: gem den sidste linje, hvis der er noget i den
        if current_line:
            lines.append(current_line)

        return lines
    
    def match_lines_to_column(self, lines, columns):
        """
        Tager linjer og sørger for, at der kun er ligeså kolonner som i overskrifter.
        Ellers flettes de sammen
        """

        column_len = len(columns)
        final_lines = []

        for line in lines:
            # Skip linjen hvis linjen er tom
            if len(line) < 1:
                continue

            # Hvis der er flere kolonner end linjer
            if len(line) > column_len:
                # Behold de første kolonner (% sidste kolonne)
                new_line = line[: column_len - 1]

                # Flet resten sammen til en sidste kolonne
                rest_lines = line[column_len - 1 :]
                merged_lines = "".join(rest_lines)

                new_line.append(merged_lines)
            else:
                new_line = line
            
            final_lines.append(new_line)
        
        return final_lines
    
    def load_as_df(self, rows, cols, file_name):
        
        df = pd.DataFrame(rows, columns=cols)
        
        # Remove control characters
        CONTROL_CHARS = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F]")
        df = df.applymap(
            lambda x: CONTROL_CHARS.sub("", x) if isinstance(x, str) else x
        )

        return df, file_name

