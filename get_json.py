import requests
import json
import time

'''
从https://api.xygeng.cn/one
'''

url = 'https://api.xygeng.cn/one'
e = 1
batch = 1000
for l in range(e):
    print('==file {}=='.format(l+1))
    lines = []

    for i in range(batch):
        time.sleep(1)
        print('--line {}--'.format(i+1))
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()['data']
            # print(data)
            lines.append(json.dumps(data, ensure_ascii=False)+('\n' if  i!=batch else ''))
        else:
            print("请求失败,status_code={}".format(response.status_code))
            break


    # print(lines)
    with open('file{}.txt'.format(l+1), 'w') as file:
        file.writelines(lines)

