from goldcode.utils.converter import Converter

converter = Converter()

html = '<p>hej med dig</p><p>nu her vi her </p>'

html = converter.linebreaks_adder(html)

print(html)