import random
import string
import markdown
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from markupsafe import escape

def generate_random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def markdown_to_html_secure(markdown_text,img_to_text=False):
    content = markdown.markdown(markdown_text)

    soup = BeautifulSoup(content, 'html.parser')
    ps = soup.find_all('p')
    for p in ps:
        try:
            if '\n' in p.string:
                p.string = p.string.replace("\n","<br>")
        except TypeError:
            pass

    links = soup.find_all('a')
    for link in links:
            if 'href' in link.attrs:
                url = link.attrs['href']
                parsed_result = urlparse(url)
                if parsed_result.scheme not in ['http', 'https']:
                    link.attrs['href'] = ''
                    link.attrs['target'] = '#'
                    link.attrs['rel'] = 'noopener noreferrer'
                    link.string = 'URL已被移除'
                else:
                    link.attrs['target'] = '_blank'
                    link.attrs['rel'] = 'noopener noreferrer'
                    link.attrs['href'] = '/redirect?url=' + link.attrs['href']


        imgs = soup.find_all('img')
        for img in imgs:
            img.attrs['src'] = 'https://imgpreview-proxy.nicewhite.xyz/' + img.attrs['src']
            if img_to_text:
                img.string = '(圖片)'

    content = str(soup)
    if escape('<br>') in content:
        content = content.replace(escape('<br>'),"<br>")
    return content

    