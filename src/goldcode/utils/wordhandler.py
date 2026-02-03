from docx import Document

class WordHander():

    def __init__(self):
        pass


    def extract_text(self, document: str):
        """
        Decoder dokument og laver liste over paragraffer i dokumentet inklusiv formattering.
        En liste over paragraffer og decoded runs, som kan bruges til at genere HTML
        """

        # Hent liste med paragraffer
        paragraphs = self._read_paragraphs(document)
        
        # Decode paragraffer
        paragraphs = self._decode_paragraphs(paragraphs)

        # Fjerner tomme paragraphs til sidst
        paragraphs = self._remove_last_paragraphs(paragraphs)

        # Returner decoded data
        return paragraphs


    def extract_plain_text(self, document: str):
        """
        Laver en liste med hver paragraf i dokumentet som et element.
        Derer intet formatering i dette.
        """
        
        # Hent liste med paragraffer
        paragraphs = self._read_paragraphs(document)
        
        # Decode paragraffer
        paragraphs = self._decode_paragraphs(paragraphs)

        # Fjerner tomme paragraphs til sidst
        paragraphs = self._remove_last_paragraphs(paragraphs)

        # Concat text
        output = []

        for paragraph in paragraphs:
            # Tekst til paragraf
            text = ""

            # Tilføj alt tekst i run til paragraf
            for run in paragraph:
                text += run['text']
            
            # Tilføj paragraf
            output.append(text)

        return output
    
    
    def _remove_last_paragraphs(self, decoded_paragraphs):
        """
        Fjerner tomme paragraffer til sidst i et dokument
        """

        for i in range(len(decoded_paragraphs) - 1, -1, -1):

            if len(decoded_paragraphs[i]) != 0:
                return decoded_paragraphs
            else:
                del decoded_paragraphs[i]


    def _decode_paragraphs(self, paragraphs: list):
        """
        Tager en list of paragraphs, decoder dem og retunerer en list med objekter, hvor hvert element er en paragraph med runs.
        Retunerer liste med paragraphs og runs, hvor hvert run er decoded til brug i f.eks. html
        """
        try:
            decoded_document = []

            for j, paragraph in enumerate(paragraphs):
                # Decoded paragraph
                decoded_paragraph = []

                # Når der er bullet, er det altid hele paragraffen (fra start til slut) som er i bullet

                # Angiver om denne paragraph er bullet.
                is_bullet = (paragraph.style and "list paragraph" in paragraph.style.name.lower())          

                for _, run in enumerate(paragraph.runs):

                    # Tjekker formattering
                    is_bold = bool(run.bold)
                    is_italic = bool(run.italic)
                    is_underline = bool(run.underline)

                    decoded_run = {
                        "text": run.text,
                        "is_bold": is_bold,
                        "is_italic": is_italic,
                        "is_underline": is_underline,
                        "is_bullet": is_bullet
                    }

                    decoded_paragraph.append(decoded_run)
            
                decoded_document.append(decoded_paragraph)
            
            return decoded_document

        except Exception as e:
            print(e)


    def _read_paragraphs(self, document: str):
        """
        Læser word dokumenter og retunerer en liste med paragraphs
        """
        try: 
            # Tjekker om dokumentet er et Word-dokument
            if not document.lower().endswith(('.doc', '.docx', 'docs')):
                print("Ikke et word-dokument, springer over")
                return

            # Læser dokument
            doc = Document(document)

            # Retunerer liste med alle paragraffer
            return [p for p in doc.paragraphs]
        except Exception as e:
            print(e)