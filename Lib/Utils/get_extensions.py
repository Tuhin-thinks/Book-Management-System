import os.path

import requests
from bs4 import BeautifulSoup


def write_to_file(filename, data):
    with open(filename, 'w') as extensions_file:
        extensions_file.write("\n".join(data))
    print("File written in :", os.path.realpath(filename))


def get_page_source(page_link):
    page = requests.get(page_link, headers={'Referrer': 'google.com'})
    contents = page.content
    soup = BeautifulSoup(contents, 'html.parser')

    selector = "strong.color3"
    extension_tags = soup.select(selector)
    extensions = []
    for extension_tag in extension_tags:
        extension_name = extension_tag.text
        if not extension_name.startswith('.'):
            extension_name = '.' + extension_name
        print(extension_name)
        extensions.append(extension_name)
    return extensions


def main():
    extension_list = get_page_source("https://www.file-extensions.org/filetype/extension/name/e-book-files")
    write_to_file("ExtensionsFile.txt", extension_list)


if __name__ == '__main__':
    main()
