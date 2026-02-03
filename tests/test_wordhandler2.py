from goldcode.utils.wordhandler import WordHander
from goldcode.utils.converter import Converter


handler = WordHander()
converter = Converter()

path = '/Users/alhu/Downloads/Fleksibel 0301_7715849144901535452.docx'

#path = '/Users/alhu/Downloads/testdoku.docx'


paragraphs = handler.extract_text(path)

print(paragraphs)

