from bs4 import BeautifulSoup

def get_img_tags_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')
    return img_tags


def get_anchor_tags_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    anchor_tags = soup.find_all('a')
    return anchor_tags


def get_aria_tags_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    btn_tags=soup.find_all('button')
    a_tags=soup.find_all('button')
    input_tags=soup.find_all('button')
    nav_tags=soup.find_all('button')
    required_tags=btn_tags + a_tags + input_tags + nav_tags
    return required_tags

