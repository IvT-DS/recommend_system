# Streamlit app related with Recommendation systems. 💡
   
## Team 🧑🏻‍💻
1. [Ivan Tereshchenko](https://github.com/IvT-DS)
2. [Aleksey Kamaev](https://github.com/AlexeyKamaev)

## Tasks 📌
1. To parse a selection of series descriptions.
2. To build a search system for the most suitable options for a user query.
3. Additionally: the service must accept a description of the series from the user and return a specified number of suitable options.

## Requirements 🖋️
1. The sample must include at least 5,000 series.
2. The search should take place as quickly as possible (hello, FAISS).
3. In the process of data collection, it is better to collect as much information (fields) as possible.

## Project results 🤖
1. Day 1. 10,000 series descriptions from the site have been parsed https://kino.mail.ru , a layout page was prepared on huggingface, which returned a random 10 series from the sample.
2. Day 2. 2 implementations have been prepared in ipynb files. A selection of TV series is a classic method based on cosine similarity and using the Faiss library. The deployment of the project on huggingface has begun.
3. Day 3. The project has been completed on huggingface, and the code has been optimized.
4. General: The MiniLM-L12-v2 model was used to vectorize the text.

## Used instruments 🧰
1. Python.
2. Pytorch.
3. Beautiful soup.
4. [FAISS](https://github.com/facebookresearch/faiss)
5. [Huggingface](https://huggingface.co/spaces/IvT-DS/find_my_show).
