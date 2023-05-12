# rust_doc_to_csv

This python script takes the html documentation from `cargo doc` and compiles
it into a .csv file for embedding with chatGPT

Copy the rust documentation in the `rust_doc/` directory and execute `main.py`.
```
python main.py
```
The compiled `documentation.csv` separates the documentations data into three 
columns: 

`tags, article, tokens`
