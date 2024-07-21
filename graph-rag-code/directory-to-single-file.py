import os
import argparse

def get_language(file_extension):
    extension_map = {
        '.ex': 'elixir',
        '.exs': 'elixir',
        '.py': 'python',
        '.md': 'markdown',
        '.txt': 'text'
    }
    return extension_map.get(file_extension.lower(), '')

def process_directory(src_dir, dest_file):
    with open(dest_file, 'w', encoding='utf-8') as outfile:
        for root, _, files in os.walk(src_dir):
            for file in files:
                if file.endswith(('.ex', '.exs', '.md', '.txt')):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, src_dir)
                    
                    outfile.write(f"# {relative_path}\n\n")
                    
                    _, file_extension = os.path.splitext(file)
                    language = get_language(file_extension)
                    
                    if language:
                        outfile.write(f"```{language}\n")
                    
                    with open(file_path, 'r', encoding='utf-8') as infile:
                        outfile.write(infile.read())
                    
                    if language:
                        outfile.write("\n```")
                    
                    outfile.write("\n\n")

def main():
    parser = argparse.ArgumentParser(description="Combine directory contents into a single file.")
    parser.add_argument("src", help="Source directory path")
    parser.add_argument("dest", help="Destination file path (should end with .txt)")
    args = parser.parse_args()
    
    if not args.dest.endswith('.txt'):
        print("Error: Destination file should have a .txt extension")
        return
    
    process_directory(args.src, args.dest)
    print(f"Combined contents written to {args.dest}")

if __name__ == "__main__":
    main()
