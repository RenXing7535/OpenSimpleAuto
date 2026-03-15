# 这段是AI写的 免责声明 还没有检查过 没有正式接入使用

import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

def search_internet(url, headers=None, timeout=10, max_retries=2):
    """
    联网爬取网页信息
    
    参数:
        url: str - 要爬取的网页URL
        headers: dict - 请求头（可选）
        timeout: int - 请求超时时间（默认10秒）
        max_retries: int - 最大重试次数（默认2次）
    
    返回:
        dict - 包含状态码、响应内容和解析后的文本
    """
    for attempt in range(max_retries + 1):
        try:
            # 默认请求头
            if not headers:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            
            # 发送请求
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取文本内容
            text_content = soup.get_text(separator='\n', strip=True)
            
            return {
                'status_code': response.status_code,
                'content': response.text,
                'text': text_content,
                'url': url,
                'error': None
            }
            
        except requests.RequestException as e:
            if attempt < max_retries:
                time.sleep(1)
                continue
            return {
                'status_code': None,
                'content': None,
                'text': None,
                'error': str(e),
                'url': url
            }

def search_unlock_info(question, headers=None, timeout=10, max_results=5):
    """
    根据问题字符串搜索普遍解锁信息
    
    参数:
        question: str - 问题字符串
        headers: dict - 请求头（可选）
        timeout: int - 请求超时时间（默认10秒）
        max_results: int - 最大返回结果数（默认5个）
    
    返回:
        dict - 包含搜索结果和相关信息
    """
    try:
        # 构建搜索URL（使用360搜索）
        search_query = urllib.parse.quote(question)
        search_url = f"https://www.so.com/s?q={search_query}"
        
        # 调用search_internet函数获取搜索结果
        search_result = search_internet(search_url, headers, timeout)
        
        if search_result['error']:
            return {
                'success': False,
                'error': search_result['error'],
                'question': question
            }
        
        # 解析搜索结果，提取相关信息
        soup = BeautifulSoup(search_result['content'], 'html.parser')
        
        # 提取搜索结果标题和链接
        search_results = []
        for result in soup.find_all('li', class_='res-list'):
            title_elem = result.find('h3')
            if title_elem:
                title = title_elem.get_text(strip=True)
                link_elem = title_elem.find('a')
                link = link_elem.get('href') if link_elem else ''
                
                # 获取摘要 - 尝试多种选择器
                snippet = ''
                for selector in ['p.res-desc', 'p.res-snippet', 'p', 'div.res-desc']:
                    if '.' in selector:
                        tag, class_name = selector.split('.')
                        snippet_elem = result.find(tag, class_=class_name)
                    else:
                        snippet_elem = result.find(selector)
                    
                    if snippet_elem:
                        snippet = snippet_elem.get_text(strip=True)
                        if snippet:
                            break
                
                if title and link:
                    search_results.append({
                        'title': title,
                        'url': link,
                        'snippet': snippet
                    })
            
            if len(search_results) >= max_results:
                break
        
        return {
            'success': True,
            'question': question,
            'search_url': search_url,
            'results': search_results[:max_results]
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'question': question
        }

# 示例用法
if __name__ == "__main__":
    result = search_internet('https://www.example.com')
    if result['error']:
        print(f"爬取失败: {result['error']}")
    else:
        print(f"状态码: {result['status_code']}")
        print(f"URL: {result['url']}")
        print("\n提取的文本内容:")
        print(result['text'][:500] + "..." if len(result['text']) > 500 else result['text'])
    
    unlock_result = search_unlock_info('如何解锁iPhone')
    if unlock_result['success']:
        print(f"搜索问题: {unlock_result['question']}")
        print(f"搜索URL: {unlock_result['search_url']}")
        print(f"找到 {len(unlock_result['results'])} 个结果")
        print("\n搜索结果:")
        for i, item in enumerate(unlock_result['results'], 1):
            print(f"{i}. {item['title']}")
            print(f"   URL: {item['url']}")
            print(f"   摘要: {item['snippet'][:150]}..." if len(item['snippet']) > 150 else f"   摘要: {item['snippet']}")
            print()
    else:
        print(f"搜索失败: {unlock_result['error']}")

    
