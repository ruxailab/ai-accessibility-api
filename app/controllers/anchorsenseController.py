
from bs4 import BeautifulSoup
from bs4.element import Tag
from utils.AnchorInsight.isDescriptive import is_descriptive_link



'''
{
    element: <a></a>
    is_descriptive:yes,
}

'''

anchorlist=[]
anchor



def fetch_all_anchor_tags(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    anchor_tags = soup.find_all('a')
    return anchor_tags



def analyse_anchor_tag(html_content):
    print(html_content)
    anchor_tags=fetch_all_anchor_tags(html_content)
    anchorObject={"element":anchor_tags}
    for tag in anchor_tags:
        anchorObject={"element":tag}
        result=is_descriptive_link(tag)
        
        
        
    