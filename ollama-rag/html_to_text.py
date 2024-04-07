from bs4 import BeautifulSoup
import os

def read_convert_save_html_to_text():
    directory = "aoc_data"
    results = []
    
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                html_content = file.read()
                soup = BeautifulSoup(html_content, 'lxml')
                text = soup.get_text(separator=' ', strip=True)
                text_filename = filename.replace('.html', '.txt')
                text_file_path = os.path.join(directory, text_filename)
                
                with open(text_file_path, 'w') as text_file:
                    text_file.write(text)
                
                results.append((text_filename, text))
    
    return results

if __name__ == "__main__":
    texts = read_convert_save_html_to_text()
    for filename, text in texts:
        print(f"File saved: {filename}")
