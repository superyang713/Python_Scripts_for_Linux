import re

text = """
Alice, My number is 415-730-0000. 23232-23232-2323222
Call me when it's convenient.
-Bob
I have a 64,000,000 year old egg.
"""

phoneRegex = re.compile(
    r'\d{1,3}(,\d{3})+'
)
mo = phoneRegex.search(text)

if mo is not None:
    print(mo.group())


if re.match('-t\d', '-t5'):
    print('find it')
