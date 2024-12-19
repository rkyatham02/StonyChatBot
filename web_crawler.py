import requests
from bs4 import BeautifulSoup
import html2text

def get_data_from_website(url):
    def fetch_html(url):
        response = requests.get(url)
        response.raise_for_status()
        return response

    def parse_html(html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        for tag in soup(["script", "style"]):
            tag.decompose()

        html2text_instance = html2text.HTML2Text()
        html2text_instance.ignore_links = True
        html2text_instance.ignore_images = True

        text_content = html2text_instance.handle(str(soup))
        return text_content, soup

    def extract_metadata(soup, url):
        page_title = soup.title.string.strip() if soup.title else "Untitled Page"
        meta_description = soup.find("meta", attrs={"name": "description"})

        description = meta_description["content"] if meta_description else page_title
        meta_keywords = soup.find("meta", attrs={"name": "keywords"})

        keywords = meta_keywords["content"] if meta_keywords else ""

        metadata = {
            'title': page_title,
            'url': url,
            'description': description,
            'keywords': keywords
        }
        
        return metadata

    try:
        response = fetch_html(url)
        text_content, soup = parse_html(response.content)
        metadata = extract_metadata(soup, url)
        return text_content, metadata

    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None, None