from bs4 import BeautifulSoup
import urllib.parse
from dataclasses import dataclass
import streamlit as st
import requests


# General configurations
LIMIT = 40
NEWS_URLS = [
    ("https://www.ynet.co.il", "/news/article"),
    ("https://www.israelhayom.co.il", "/news"),
    ("https://www.hamal.co.il/main", "/main"),
    ("https://www.n12.co.il", "/news-military"),
]
headers = {
    'cache-control': "max-age=0",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'sec-fetch-site': "none",
    'sec-fetch-mode': "navigate",
    'sec-fetch-user': "?1",
    'sec-fetch-dest': "document",
    'accept-language': "en-US,en;q=0.9"
}


@dataclass
class UrlData:
    url: str
    source_name: str
    title: str


def aquire_data():
    data = []

    for url, fil in NEWS_URLS:
        counter = 0
        html = requests.get(url, headers=headers).content
        soup = BeautifulSoup(html, 'html.parser')
        if soup.title is None:
            data.append(UrlData("", url, "Error fetching data."))

        for link in soup.find_all('a'):
            link_url = link.get('href')

            if len(link.text) > 15 and fil in link_url:
                counter += 1
                if 'http' not in link_url:
                    link_url = url.split(fil)[0] + urllib.parse.unquote(link_url)
                # print(link_url, link.text.strip())
                data.append(UrlData(link_url, url, link.get_text().strip()))

            if counter == LIMIT:
                break
    return data


def setup_page(data):
    st.set_page_config(layout="wide")
    st.markdown("""<h1><div dir="rtl">חדשות</div></h1>""", unsafe_allow_html=True)
    cols = st.columns(len(NEWS_URLS), gap="small")
    urls = [item[0] for item in NEWS_URLS]
    mapping = {url: i for i, url in enumerate(urls)}
    for url, index in mapping.items():
        with cols[index]:
            st.markdown(f"""<a href='{url}'><h4 style="text-align: center;">{url}</h4></a>""", unsafe_allow_html=True)

    for item in data:
        with cols[mapping[item.source_name]]:
            st.markdown("""<div dir="rtl">""" + item.title + ("<a href='%s'> (%s) </a>" % (item.url, item.source_name.split('www.')[1].split('/')[0])) + "</div>", unsafe_allow_html=True)


def main():
    data = aquire_data()
    setup_page(data)


if __name__ == '__main__':
    main()
