from collections import OrderedDict

from bs4 import BeautifulSoup


def unique_list(lst):
    try:
        unique = list(OrderedDict.fromkeys(lst).keys())
    except TypeError:
        unique = []
        [unique.append(obj) for obj in lst if obj not in unique]
    return unique


def html_to_text(html):
    soup = BeautifulSoup(html, features='html.parser')
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out
    # get text

    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    links = [a['href'] for a in soup.find_all(
        href=True) if a and a['href'].startswith('http')]
    if links:
        text = '{}\nLinks:\n{}'.format(text, '\n'.join(unique_list(links)))

    return text
