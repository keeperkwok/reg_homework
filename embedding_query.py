import chromadb
import json
import requests
 
# collection名称
collection_name="file_data"
 
def init_db_client():
    """初始化数据库客户端"""
    chroma_client = chromadb.PersistentClient(path="mydb.db")
    return chroma_client
 
def create_collection(collection_name):
    """创建collection"""
    chroma_client = init_db_client()
    collection=chroma_client.get_or_create_collection(name=collection_name)
    return collection
 
def add_documents(collection, documents, metadatas):
    """写入数据"""
    collection.add(
        # embeddings=self.embedding_fn(documents),  # 每个文档的向量
        documents=documents,  # 文档的原文
        metadatas=metadatas,
        ids=[f"id{i}" for i in range(len(documents))]  # 每个文档的 id
    )

def llm(query, res):

    
    url = 'https://smartvision.dcclouds.com:3004/send/1330/v1/chat/completions'
    headers = {'Content-Type': 'application/json'}

    d = {
            "model": "智谱GLM-4-9B",
            "messages": [
            {
                "role": "system",
                "content": '''
                    根据提供的上下文和出处，请帮我回答用户的问题，并给出原文出处，不要做多余的回答。
                    <context>
                        {}
                    </context>
                    <origin>
                        {}
                    </origin>
                    用户问题：
                '''.format(res['documents'][0][0], res['metadatas'][0][0]['origin'])
            },
            {
                "role": "user",
                "content": query
            }
            ],
            "stream": False
        }

    r = requests.post(url, json=d, headers=headers)

    return r.json()['choices'][0]['message']['content']

 
def db_test():
    collection = create_collection(collection_name)
    datas = []
    metadatas = []

    # 打开文件
    with open(collection_name+'.txt', 'r') as file:
        # 逐行迭代读取
        for line in file:
            # 处理读取到的行
            # print(line.strip())  # strip用于去掉行末的换行符
            j = json.loads(line.strip())
            datas.append(j['content'])
            del j['content']
            metadatas.append(j)


 
    add_documents(collection, datas, metadatas)
 
    # 查询数据
    question = "有一句话是两个人相爱的概率是多少来着？"
    # question = "如果有一拳解决不了的事情，该怎么办？"
    res=collection.query(
        query_texts=[question],
        n_results=1
    )
 
    # print(res)

    answer = llm(question, res)
    print(answer)
 
db_test()
