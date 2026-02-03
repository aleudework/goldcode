
class Converter():

    def __init__(self):
        pass



    def flatten(self, paragraphs):
        """
        Tager en 2D med paragraphs og flatten til 1D. Tilføjer en paragraph værdi, som angiver, hvilke paragraph, det hører til.
        Den flatten list bruges til efterfølgende behandling.
        """

        output = []

        # Loop over runs
        for i, runs in enumerate(paragraphs):
            for j, run in enumerate(runs):
                
                # Append
                value = run
                value['line'] = i + 1
                output.append(value)

        return output
            



    def convert_text_to_eg_html(self, flatten_text: list):
        """
        Tager en flatten liste over tekst.
        Kan bruges til at decode et word dokument og derefter konverterer teksten med formattering til EG HTML til brug i afdelingstekster.
        """

        # Starter html
        html = '<p>'


        for i, text in enumerate(flatten_text):
            prev = flatten_text[i-1] if i > 0 else None # Finder forrige
            next = flatten_text[i+1] if i < len(flatten_text) - 1 else None # Finder næste

            # Henter linje værdier
            prev_line = prev and prev.get('line')
            this_line = text and text.get('line')
            next_line = next and next.get('line')

            # Henter bullet værdier
            prev_bullet = prev and prev.get('is_bullet')
            this_bullet = text and text.get('is_bullet')
            next_bullet = next and next.get('is_bullet')

            # Henter bold værdier
            prev_bold = prev and prev.get('is_bold')
            this_bold = text and text.get('is_bold')
            next_bold = next and next.get('is_bold')

            # Henter bold værdier
            prev_italic = prev and prev.get('is_italic')
            this_italic = text and text.get('is_italic')
            next_italic = next and next.get('is_italic')

            # Henter underline værdier
            prev_underline = prev and prev.get('is_underline')
            this_underline = text and text.get('is_underline')
            next_underline = next and next.get('is_underline')

            ### Paragraf start

            # Start ny paragraf, hvis der er dobbelt linjeskift
            if (
                prev is not None
                and (this_line - prev_line) >= 2 
                and this_line > 1
                ):
                html += '<p>'
            
            # Opret linjeskift, hvis ny linje
            if (
                prev is not None
                and (this_line - prev_line) == 1 
                and this_line > 1
                and this_bullet is not True
                ):
                html += '<br>'


            ### Bullet point start

            # Start unordered list, hvis første bullet point er true.
            if (
                prev is not None
                and (this_line - prev_line) > 0 # Sikrer sig linjeskift
                and prev_bullet is not True
                and this_bullet is True
                ):
                html += '</p><ul><li><p>'

            # Start kun bullet hvis ny linje i samme liste
            if (
                prev is not None
                and (this_line - prev_line) > 0 # Sikrer sig linjeskift / dermed ny bullet
                and prev_bullet is True # Skal være true her i forhold til
                and this_bullet is True
                ):
                html += '<li><p>'

            ### Formattering start
            if ((
                    prev is not None
                    and prev_bold is not True
                    and this_bold is True
                ) or (
                    prev is None
                    and this_bold is True
                )):
                html += '<strong>'


            if ((
                    prev is not None
                    and prev_italic is not True
                    and this_italic is True
                ) or (
                    prev is None
                    and this_italic is True
                )):
                html += '<em>'


            if ((
                    prev is not None
                    and prev_underline is not True
                    and this_underline is True
                ) or (
                    prev is None
                    and this_underline is True
                )):
                html += '<u>'


            ### Tilføjer råtekst
            html += text.get('text')


            ### Formattering slut
            if ((
                    next is not None
                    and next_underline is not True
                    and this_underline is True
                ) or (
                    next is None
                    and this_underline is True
                )):
                html += '</u>'

            if ((
                    next is not None
                    and next_italic is not True
                    and this_italic is True
                ) or (
                    next is None
                    and this_italic is True
                )):
                html += '</em>'

            if ((
                    next is not None
                    and next_bold is not True
                    and this_bold is True
                ) or (
                    next is None
                    and this_bold is True
                )):
                html += '</strong>'


            ### Bullet point slut
            if (
                (next is not None
                and (next_line - this_line) > 0 
                and this_bullet is True 
            ) or (# afvikler hvis slut
                next is None
                and this_bullet is True
            )):
                html += '</p></li>'


            ### Unordered list slut
            if (
                (next is not None
                and (next_line - this_line) > 0 
                and this_bullet is True 
                and next_bullet is not True # Hvis ikke flere bullet points, afslut
            ) or ( 
                next is None
                and this_bullet is True
            )):
                html += '</ul><p>'

            ### Paragraf slut

            # Hvis næste linje er ny paragraf, afslut paragraf.
            if (
                this_line is not None
                and next_line is not None
                and (next_line - this_line) > 1 
                ):
                html += '</p>'
        
        html += '</p>'
        
        return html
            


