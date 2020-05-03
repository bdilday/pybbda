import logging
import requests
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)


def replace_chars(text, chars_list=None):
    if chars_list is None:
        chars_list = "/"
    return re.sub(r"[{}]".format(chars_list), "_", text)


def url_to_table_rows(url, table_id):
    logger.debug("getting table %s from URL %s", table_id, url)
    payload = requests.get(url).text
    soup = BeautifulSoup(payload, features="lxml")
    tbl = soup.find(id=table_id)
    rows = tbl.find_all("tr")
    table_rows = [
        [column.get_text() for column in row.find_all(["td", "th"])] for row in rows
    ]
    logger.debug("found table with %d rows", len(table_rows))
    return table_rows
