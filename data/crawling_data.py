import requests
from bs4 import BeautifulSoup
import json
import time

headers = {'User-Agent': 'Mozilla/5.0'}

def get_article_links(page_url):
    response = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', class_='item-news')
    links = []
    for article in articles:
        title_tag = article.find('h3', class_='title-news')
        if title_tag and title_tag.a:
            links.append(title_tag.a['href'])
    return links

def get_article_content(article_url):
    response = requests.get(article_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Tiêu đề
    title_tag = soup.find('h1', class_='title-detail')
    title = title_tag.get_text(strip=True) if title_tag else ""

    # Thời gian
    time_tag = soup.find('span', class_='date')
    publish_time = time_tag.get_text(strip=True) if time_tag else ""

    # Tác giả
    author_tag = soup.find('p', class_='Normal', style='text-align:right;')
    author = author_tag.strong.get_text(strip=True) if author_tag and author_tag.strong else "Không rõ"

    # Mô tả + Nội dung
    desc_tag = soup.find('p', class_='description')
    description = desc_tag.get_text(strip=True) if desc_tag else ""
    content = soup.find('article', class_='fck_detail')
    paragraphs = content.find_all('p', class_='Normal') if content else []
    content_text = "\n".join(p.get_text(strip=True) for p in paragraphs)
    full_content = description + "\n" + content_text
    full_content = full_content.replace(f"\n{author}","")
    return {
        'title': title,
        'author': author,
        'time': publish_time,
        'content': full_content,
        'url': article_url
    }

# ========== MAIN ==========
number_page = 10
all_articles = []
for i in range(2,number_page):
    page_url = f'https://vnexpress.net/thoi-su-p{i}'
    article_links = get_article_links(page_url)
    for link in article_links:
        try:
            data = get_article_content(link)
            all_articles.append(data)
            print(f"✔ Đã lưu: {data['title']}")
            time.sleep(1)  # nghỉ để tránh bị chặn IP
        except Exception as e:
            print(f"❌ Lỗi với link {link}: {e}")


    # Ghi vào file JSON
with open('vnexpress_thoi_su.json', 'a', encoding='utf-8') as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=4)
