import os
import shutil
import pandas
from pandas.core.arrays.string_ import pandas_dtype
import tiktoken
from bs4 import BeautifulSoup

path_doc = "./doc_bevy/"
path_out = "./out/"

enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
doc_data = {"tags": [], "article": [], "tokens": []}

for root, dirs, files in os.walk(path_doc):
    for file in files:
        if file.endswith(".html"):
            prefix = root.replace(path_doc, "")
            prefix = prefix.replace("/", ",")
            file_no_ext = file.replace(".html", "")

            file_org = str(os.path.join(root, file))
            file_new = str(path_out + prefix + "," + file_no_ext)

            shutil.copyfile(file_org, file_new)

for root, dirs, files in os.walk(path_out):
    for file in files:
        tags_array = file.split(",")
        tags = " ".join(tags_array)

        with open(os.path.join(root, file)) as f, open("article.txt", "a") as a:
            content = f.read().splitlines()

            for line in content:
                soup = BeautifulSoup(line, "html.parser")
                text = str(soup.get_text())
                a.write(text + "\n")
            a.close()

        article = open("article.txt", "r")
        tokens = len(enc.encode(article.read()))

        article = open("article.txt", "r")

        doc_data["tags"].append(tags)
        doc_data["article"].append(article.read())
        doc_data["tokens"].append(tokens)
        open("article.txt", "w").close()

df = pandas.DataFrame(doc_data)
df.to_csv("documentation.csv", index=False, sep=',')
