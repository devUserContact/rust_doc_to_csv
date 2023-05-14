import os
import os.path as path
import shutil
import pandas as pd
import tiktoken
from bs4 import BeautifulSoup

path_doc = "./rust_doc/"
path_out = "./out/"

enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

for root, dirs, files in os.walk(path_doc):
    for file in files:
        if file.endswith(".html"):
            prefix = root.replace(path_doc, "")
            prefix = prefix.replace("/", ",")
            file_no_ext = file.replace(".html", "")

            file_org = str(path.join(root, file))
            file_new = str(path_out + prefix + "," + file_no_ext)
            shutil.copyfile(file_org, file_new)

chunk_size = 3
chunk_num = 1
chunk_data = {"tags": [], "article": [], "tokens": []}

for root, dirs, files in os.walk(path_out):
    for file in files:
        tags = " ".join(file.split(","))

        with open(path.join(root, file)) as f, open("article.txt", "a") as a:
            content = f.read().splitlines()

            for line in content:
                soup = BeautifulSoup(line, "html.parser")
                text = str(soup.get_text())
                a.write(text + "\n")
            a.close()

        article = open("article.txt", "r")
        tokens = len(enc.encode(article.read()))
        article.seek(0)

        chunk_data["tags"].append(tags)
        chunk_data["article"].append(article.read())
        chunk_data["tokens"].append(tokens)
        article.close()
        open("article.txt", "w").close()

        if len(chunk_data["tags"]) == chunk_size:
            df = pd.DataFrame(chunk_data)
            chunk_num_str = str(chunk_num).zfill(5)
            df.to_csv(f"documentation_chunk{chunk_num_str}.csv", index=False, sep=",")
            chunk_num += 1
            chunk_data = {"tags": [], "article": [], "tokens": []}

if len(chunk_data["tags"]) > 0:
    df = pd.DataFrame(chunk_data)
    chunk_num_str = str(chunk_num).zfill(5)
    df.to_csv(f"documentation_chunk{chunk_num_str}.csv", index=False, sep=",")

os.remove("article.txt")
