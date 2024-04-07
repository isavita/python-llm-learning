import ollama, chromadb, time, os
from mattsollamatools import chunker, chunk_text_by_sentences
from utils import getconfig


def readtext(filename):
    directory = "aoc_data"
    file_path = os.path.join(directory, filename)
    with open(file_path, 'r') as file:
        return file.read()

chroma = chromadb.HttpClient(host="localhost", port=8000)
# chroma.delete_collection("ollama-rag")
collection = chroma.get_or_create_collection(name="ollama-rag", metadata={"hnsw:space": "cosine"})

embedmodel = getconfig()["embedmodel"]
starttime = time.time()

directory = "aoc_data"

for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        text = readtext(filename)
        chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=7, overlap=0 )
        print(f"with {len(chunks)} chunks")
        for index, chunk in enumerate(chunks):
            embed = ollama.embeddings(model=embedmodel, prompt=chunk)['embedding']
            print(".", end="", flush=True)
            collection.add([filename+str(index)], [embed], documents=[chunk], metadatas={"source": filename})
    
print("--- %s seconds ---" % (time.time() - starttime))
