import requests
import datetime
from requests_html import HTML
import csv


# now = datetime.datetime.now()
# year = now.year


def url_to_txt(url, filename="boxoffice.html", save=False):
    r = requests.get(url)
    if r.status_code == 200:
        html_text = r.text
        if save:
            with open(f"world_boxoffice.html", 'w',    encoding='utf-8') as f:
                f.write(html_text)
        return html_text

    return ""


url = "https://www.boxofficemojo.com/"


def parse_and_extract(url):

    html_text = url_to_txt(url)
    r_html = HTML(html=html_text)
    table_class = ".a-link-normal "
    r_table = r_html.find(table_class)
    # print(r_table)

    table_data = []
    header_names = []

    if len(r_table) == 1:

        parsed_table = r_table[0]
        rows = parsed_table.find("tr")
        header_row = rows[0]
        header_cols = header_row.find("th")
        header_names = [x.text for x in header_cols]

        for row in rows:
            # print(row.text)
            cols = row.find("td")
            row_data = []
            for i, col in enumerate(cols):
                #print(i, col.text, '\n')
                row_data.append(col.text)
            table_data.append(row_data)

        with open("box.csv", "w", newline="") as new_file:
            writer = csv.writer(new_file)
            writer.writerows(table_data)


print(parse_and_extract("https://www.boxofficemojo.com/"))
