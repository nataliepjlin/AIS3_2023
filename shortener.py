import os
from bs4 import BeautifulSoup
import re

def filter_html_tags(html_content, allowed_tags):
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    def is_allowed(tag):
        return tag.name in allowed_tags

    lines = []
    for line in soup.stripped_strings:
        if any(tag in line for tag in allowed_tags):
            lines.append(line)

    result_text = '\n'.join(lines)
    return result_text

def remove_empty_lines(text):
    lines = filter(lambda x: x.strip(), text.splitlines())
    result_text = '\n'.join(lines)
    return result_text

def extract_urls(html_content):
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', html_content)

    # List of patterns indicating URLs to exclude (e.g., fonts, SVGs, stylesheets)
    exclude_patterns = ['.woff', '.woff2', '.ttf', '.eot', '.svg', '.css','xhtml','/svg','/xhtml','xlink']

    filtered_urls = []
    for url in urls:
        if not any(pattern in url for pattern in exclude_patterns):
            filtered_urls.append(url)

    return filtered_urls



def process_html_files(input_folder, output_folder, allowed_tags):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    html_files = [file for file in os.listdir(input_folder) if file.endswith('.html')]

    output_file_path = os.path.join(output_folder, 'output.txt')

    with open(output_file_path, 'w', encoding='utf-8') as text_file:
        for html_file in html_files:
            input_file_path = os.path.join(input_folder, html_file)

            with open(input_file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()

            filtered_data = filter_html_tags(html_content, allowed_tags)
            filtered_data_without_empty_lines = remove_empty_lines(filtered_data)

            urls_data = extract_urls(html_content)

            text_file.write(filtered_data_without_empty_lines)
            text_file.write('\n\nURLs:\n')
            for url in urls_data:
                text_file.write(url + '\n')
            text_file.write("-"*20+'\n')

allowed_tags = ['head', 'title', 'meta', 'body', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'strong', 'a', 'img', 'hr', 'table', 'tbody', 'tr', 'th', 'td', 'ol', 'ul', 'li', 'ruby', 'label','style']

input_folder_path = '/home/natalielin/crawl/results/raw/'
output_folder_path = '/home/natalielin/crawl/results/processed'

process_html_files(input_folder_path, output_folder_path, allowed_tags)
print("OK")