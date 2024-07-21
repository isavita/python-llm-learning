import os
import chardet
import argparse
import glob
import gitignore_parser
from litellm import completion

# Constants
IGNORE_PATTERNS = [
    # Directories
    '*build*', 'bin', '*cache*', 'node_modules', 'venv', '.git', 'tmp', 'log', 'temp',
    # File types
    '*.json', '.xml', '*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp', '*.tiff', '*.ico',
    '*.mp3', '*.mp4', '*.wav', '*.avi', '*.mov', '*.flv', '*.wmv',
    '*.pdf', '*.doc', '*.docx', '*.xls', '*.xlsx', '*.ppt', '*.pptx',
    '*.zip', '*.tar', '*.gz', '*.rar',
    '*.exe', '*.dll', '*.so', '*.dylib',
    '*.pyc', '*.pyo', '*.pyd',  # Python compiled files
    '*.class',  # Java compiled files
    '*.o', '*.a', '*.lib'  # C/C++ object files and libraries
]
CODE_EXTENSIONS = [
    '.py',   # Python
    '.ex', '.exs',  # Elixir
    '.rb',   # Ruby
    '.java', # Java
    '.cpp', '.cc', '.cxx', '.c++', '.h', '.hh', '.hpp', '.hxx', '.h++', # C++
    '.js',   # JavaScript
    '.ts',   # TypeScript
    '.go',   # Go
    '.rs',   # Rust
    '.php',  # PHP
    '.cs',   # C#
    '.c', '.h', # C
    '.kt', '.kts', # Kotlin
    '.swift', # Swift
    '.m', '.mm', # Objective-C
    '.sh', # Shell script
    '.pl', '.pm', '.t', '.pod', # Perl
    '.rb', # Ruby
    '.r', # R
    '.jl', # Julia
    '.dart', # Dart
    '.lua', # Lua
    '.sc', '.scala', # Scala
    '.groovy', '.gvy', '.gy', '.gsh', # Groovy
    '.hs', # Haskell
    '.erl', '.hrl', # Erlang
    '.ml', '.mli', # OCaml
    '.fs', '.fsi', '.fsx', '.fsscript', # F#
    '.clj', '.cljs', '.cljc', '.edn', # Clojure
    '.elm', # Elm
    '.jl', # Julia
    '.rkt', # Racket
    '.coffee', # CoffeeScript
    '.tsx', # TypeScript JSX
    '.jsx', # JavaScript JSX
    # Additional extensions
    '.md',  # Markdown
    '.eex', '.leex', '.heex',  # Phoenix (Elixir)
    '.erb', '.haml', '.slim',  # Rails (Ruby on Rails)
    '.hbs', '.handlebars',  # Handlebars
    '.jinja', '.jinja2',  # Jinja
    '.ejs',  # EJS
    '.pug', '.jade',  # Pug
    # CSS, HTML, Sass, etc.
    '.css',  # CSS
    '.html', '.htm',  # HTML
    '.scss', '.sass',  # Sass/SCSS
    '.less',  # Less
    '.yaml', '.yml',  # YAML
]

def get_gitignore_matcher(root_dir):
    gitignore_file = os.path.join(root_dir, '.gitignore')
    if os.path.exists(gitignore_file):
        return gitignore_parser.parse_gitignore(gitignore_file)
    return lambda _: False

def should_ignore(path, gitignore_matcher):
    # Convert path to relative path
    rel_path = os.path.relpath(path, start=os.path.dirname(path))
    
    # Check if any part of the path matches the ignore patterns
    path_parts = path.split(os.sep)
    for pattern in IGNORE_PATTERNS:
        if any(glob.fnmatch.fnmatch(part, pattern) for part in path_parts):
            return True
    
    # Check with gitignore matcher
    return gitignore_matcher(path)

def get_file_summary(file_path, model, api_key, base_url):
    try:
        with open(file_path, 'rb') as file:
            raw_content = file.read()
        
        # Detect the file encoding
        detected = chardet.detect(raw_content)
        encoding = detected['encoding']

        # Decode the content, ignoring errors
        content = raw_content.decode(encoding=encoding, errors='ignore')
        
        if len(content) > 8000:
            content = content[:8000]
        
        prompt = f"Please provide a one-sentence summary of what this file does. Here's the file content:\n\n{content}\n\nOne sentence summary:"
        
        completion_kwargs = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "api_key": api_key
        }
        if base_url:
            completion_kwargs["base_url"] = base_url
        
        response = completion(**completion_kwargs)
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error processing file: {str(e)}"

def get_code_structure(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()
    
    structure = []
    for line in content:
        if line.strip().startswith(('def ', 'class ')):
            structure.append(line.strip())
    
    return structure

def process_directory(root_dir, output_dir, model, api_key, base_url):
    gitignore_matcher = get_gitignore_matcher(root_dir)
    file_structure = []
    code_structure = []
    
    for root, dirs, files in os.walk(root_dir):
        # Use list comprehension to filter out ignored directories
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), gitignore_matcher)]
        
        for file in files:
            file_path = os.path.join(root, file)
            if should_ignore(file_path, gitignore_matcher):
                continue
            
            rel_path = os.path.relpath(file_path, root_dir)
            summary = get_file_summary(file_path, model, api_key, base_url)
            file_structure.append(f"{rel_path}: {summary}")
            
            _, ext = os.path.splitext(file)
            if ext in CODE_EXTENSIONS:
                code_structure.append(f"File: {rel_path}")
                code_structure.extend(get_code_structure(file_path))
                code_structure.append("")  # Empty line for readability
    
    # Write file structure (overwrite if exists)
    with open(os.path.join(output_dir, 'file_structure.txt'), 'w') as f:
        f.write("\n".join(file_structure))
    
    # Write code structure (overwrite if exists)
    with open(os.path.join(output_dir, 'code_structure.txt'), 'w') as f:
        f.write("\n".join(code_structure))
    
    # Generate project summary
    file_structure_text = "\n".join(file_structure)
    prompt = f"Based on the following file structure and summaries, provide a 4-5 sentence summary of the entire project:\n\n{file_structure_text}\n\nProject summary:"
    
    completion_kwargs = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "api_key": api_key
    }
    if base_url:
        completion_kwargs["base_url"] = base_url
    
    response = completion(**completion_kwargs)
    
    project_summary = response.choices[0].message.content.strip()
    
    # Write project summary (overwrite if exists)
    with open(os.path.join(output_dir, 'project_summary.txt'), 'w') as f:
        f.write(project_summary)

def main():
    parser = argparse.ArgumentParser(description="Process a project directory and generate summaries.")
    parser.add_argument("root_dir", help="Path to the project directory")
    parser.add_argument("--output_dir", default=".", help="Path to the output directory")
    parser.add_argument("--api_key", default=os.environ.get('MISTRAL_API_KEY'), help="API key for Mistral")
    parser.add_argument("--model", default="mistral/open-mistral-nemo", help="Name of the Mistral model to use")
    parser.add_argument("--base_url", default=None, help="Base URL for Mistral API")
    
    args = parser.parse_args()
    
    if not args.api_key:
        raise ValueError("API key must be provided either through --api_key argument or MISTRAL_API_KEY environment variable")
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    process_directory(args.root_dir, args.output_dir, args.model, args.api_key, args.base_url)

if __name__ == "__main__":
    main()
