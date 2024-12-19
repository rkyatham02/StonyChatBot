import requests
from bs4 import BeautifulSoup
import html2text

def get_data_from_website(url):
    """
    Retrieve text content and metadata from a given URL.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        tuple: A tuple containing the text content (str) and metadata (dict).
               If an error occurs during retrieval, returns (None, None).
    """
    
    def fetch_html(url):
        """
        Fetch HTML content from a given URL.
        
        Args:
            url (str): The URL to fetch content from.
        
        Returns:
            response (requests.Response): The response object containing the HTML content.
        
        Raises:
            requests.RequestException: If an error occurs during the request.
        """
        response = requests.get(url)
        response.raise_for_status()
        return response

    def parse_html(html_content):
        """
        Parse the HTML content using BeautifulSoup and convert it to text.

        Args:
            html_content (str): The HTML content to parse.

        Returns:
            str: The text content extracted from the HTML.
        """
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove script and style tags from the HTML
        for tag in soup(["script", "style"]):
            tag.decompose()

        # Convert HTML to text
        html2text_instance = html2text.HTML2Text()

        # Setting the Ignores
        html2text_instance.ignore_links = True
        html2text_instance.ignore_images = True

        text_content = html2text_instance.handle(str(soup))
        return text_content, soup

    def extract_metadata(soup, url):
        """
        Extract metadata from the parsed HTML.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object representing the parsed HTML.
            url (str): The URL of the webpage.

        Returns:
            dict: A dictionary containing the metadata.
        """
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
        # Fetch HTML content
        response = fetch_html(url)

        # Parse HTML content and convert to text
        text_content, soup = parse_html(response.content)

        # Extract metadata
        metadata = extract_metadata(soup, url)

        return text_content, metadata

    except requests.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None, None