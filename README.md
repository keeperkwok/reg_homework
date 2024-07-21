# 环境

Java版本  

```
Java3.10
```

安装依赖  

```
pip install requests
pip install chromadb
```

# 下载样例数据

从 https://api.xygeng.cn/one 随机获得名言警句1000条, 保存为一条条的json行到文件file_data.txt  
样例数据
```json
{"id": 519, "tag": "其他", "name": "佚名", "origin": "青玉案·元夕", "content": "众里寻他千百度，蓦然回首，那人却在，灯火阑珊处。", "created_at": "2019-01-23T07:19:06.000Z", "updated_at": "2022-03-09T08:42:10.000Z"}
```

# 向量存储与检索

使用内存向量数据库ChromaDB，将json拆分为documents和metadatas，存入到向量数据库中  

```python
collection.add(
        # embeddings=self.embedding_fn(documents),  # 每个文档的向量
        documents=documents,  # 文档的原文
        metadatas=metadatas,
        ids=[f"id{i}" for i in range(len(documents))]  # 每个文档的 id
    )
```

# 大模型综述

检索到topK个切片后，由大模型综述，使用问学智谱GLM-4-9B大模型

```python
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
```

# 结果截图

## 问题1
```python
question = "有一句话是两个人相爱的概率是多少来着？"
```
```json
{"id": 1318, "tag": "动画", "name": "佚名", "origin": "《秒速五厘米》", "content": "人一生会遇到约2920万人，两个人相爱的概率是0.000049。所以你不爱我，我不怪你。", "created_at": "2019-01-23T09:40:04.000Z", "updated_at": "2022-03-09T08:42:10.000Z"}
```

<img width="276" alt="image" src="https://github.com/user-attachments/assets/d3d022c7-b712-4628-bc53-a2e08fd1d21e">

## 问题2
```python
question = "如果有一拳解决不了的事情，该怎么办？"
```
```json
{"id": 947, "tag": "动画", "name": "佚名", "origin": "《一拳超人》", "content": "世界上 ，没有一拳解决不了的事，如果有，那就两拳。", "created_at": "2019-01-23T08:23:02.000Z", "updated_at": "2022-03-09T08:42:10.000Z"}
```
<img width="1024" alt="image" src="https://github.com/user-attachments/assets/7a1c77c0-fc47-4eee-8cb4-fff25dcae03d">


