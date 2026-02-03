from goldcode.utils.wordhandler import WordHander
from goldcode.utils.converter import Converter


handler = WordHander()
converter = Converter()

path = '/Users/alhu/Downloads/Adm 1.docx'

#path = '/Users/alhu/Downloads/testdoku.docx'

paragraphs = handler.extract_text(path)

flatten = converter.flatten(paragraphs)

for i, flat in enumerate(flatten):
    print(flat)
    if i == 5:
        break

html = converter.convert_text_to_eg_html(flatten)

print(html)