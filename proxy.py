# 使用socks5代理 clash

import requests

local_clash_proxy = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890'
}

# 请求函数
def fetch(url:str, **kwargs)->requests.Response:
    '''
    使用clash本地http代理请求函数
    代理地址：`http://127.0.0.1:7890`

    Parameters
    ------------------
    url : `str`
    请求url
    method : `str` = `get`
    请求方法
    **kwargs : `dict`
    携带参数

    Returns
    ------------------
    `Response` 响应对象
    '''
    response = requests.get(url, proxies=local_clash_proxy, **kwargs)
    
    return response
# 测试
if __name__ == '__main__':
    with open('t.html', 'w', encoding='UTF-8') as f:
        f.write(fetch('https://scholar.google.com.hk/scholar', params={'start': '10', 'q': 'abc', 'hl': 'zh-CN', 'as_sdt':'0,5'}))