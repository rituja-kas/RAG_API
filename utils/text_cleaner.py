import re

def clean_text(text:str):
    if not text:
        return ''

    text = text.replace('\n','').replace('\t','')

    text = re.sub('[^a-zA-Z]',' ',text)
    text = ''.join(c for c in text if c.isprintable())
    text = text.strip()
    return text

