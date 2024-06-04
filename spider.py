from lxml import etree
from DrissionPage import ChromiumPage
import time
import queue
import threading

from proxy import fetch



# 爬取网页
main_url = 'https://scholar.google.com.hk/scholar'
params={
    'start': '0', 
    'q': 'abc', 
    'hl': 'zh-CN', 
    'as_sdt':'0,5'
} # 示例参数

scihub_url = 'https://sci-hub.53yu.com/'



def get_paper_info(q:str, round:int=1)->list[dict]:
    '''
    获取谷歌学术搜索结果

    Parameters
    ------------------
    q : str 
    搜索关键词
    round : int 
    搜索页数(一页10条)

    Returns
    ------------------
    list[dict]
    结果列表item `{'title': str, 'url': str}`
    '''
    main_url:str = 'https://scholar.google.com.hk/scholar'
    result:list[dict] = []
    for i in range(round):
        params={
            'start': str(i*10), 
            'q': q, 
            'hl': 'zh-CN', 
            'as_sdt':'0,5'
        }
        response = fetch(main_url, params=params)
        html = etree.HTML(response.text)
        ans_divs = html.xpath('//div[@id="gs_res_ccl_mid"]/div')
        for div in ans_divs:
            title = div.xpath('.//h3/a//text()')
            url = div.xpath('.//h3/a/@href')
            try:
                result.append({'title':''.join(title), 'url':url[0]})
            except:
                continue
    return result

def get_paper_file(q:queue.Queue, page_num:int=0)->bool:
    '''
    通过sci-hub获取论文pdf

    受不了了 用无头浏览器吧

    Parameters
    ------------------
    title : str
    论文标题
    url : str
    论文链接
    
    Returns
    ------------------
    bool 下载是否成功
    '''
    page = ChromiumPage(page_num)
    while not q.empty():
        item = q.get()
        title = item['title']
        url = item['url']
        page.get(scihub_url)
        input_box = page.ele('@name=request')
        input_box.input(url)
        page.ele('@id=open').click()
        try:
            link =page.ele('@id=pdf').attrs['src'].split('#')[0]
            if link.startswith('//'):
                link = 'https:'+link
            page.download(link, 'papers', title+'.pdf') 
        except Exception as e:
            print(e)
        finally:
            q.task_done()
    page.close()


if __name__ == '__main__':
    items = get_paper_info('abc', 3)
    q = queue.Queue()
    for item in items:
        q.put(item)
    threads = []
    for i in range(5):
        t = threading.Thread(target=get_paper_file, args=(q, i))
        threads.append(t)
        t.start()
    