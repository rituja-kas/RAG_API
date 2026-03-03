def chunktext(text:str,chunksize:int=400,overlap:int=50):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunksize
        chunks.append(text[start:end])
        start += chunksize-overlap
    return chunks

