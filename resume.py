import yaml
from jinja2 import Environment, FileSystemLoader
from zipfile import ZipFile, ZIP_DEFLATED
import os
import shutil
import subprocess

CONFIG_FILE = "config.yaml"

RESUME_DIR = "resume"
RESUME_DATA = "resume/master-resume.yaml"


def load_config():
    with open(CONFIG_FILE, "r", encoding = "utf-8") as file:
        config = yaml.safe_load(file)
    
    return config


def render_docx():

    config = load_config()
    paths = config['output']['docx']
    templates = paths['templates']
    build = paths['build']

    # Import the resume data
    with open(RESUME_DATA, "r", encoding = "utf-8") as file:
        resume_data = yaml.safe_load(file)

    env = Environment(loader = FileSystemLoader('.'))

    doc_template = env.get_template(templates["document-template"])
    doc_content = doc_template.render(resume_data)

    styles_template = env.get_template(templates["styles-template"])
    styles_content = styles_template.render(resume_data)

    num_template = env.get_template(templates["numbering-template"])
    num_content = num_template.render(resume_data)
    

    # Clean the archive directory
    if os.path.isdir(build["archive"]):
        shutil.rmtree(build["archive"])

    shutil.copytree(templates["template"], build["archive"])

    # Write the document content to word/document.xml
    with open(os.path.join(build["archive"], "word/document.xml"), 'w', encoding = 'utf-8') as file:
        file.write(doc_content)

    with open(os.path.join(build["archive"], "word/styles.xml"), 'w', encoding = 'utf-8') as file:
        file.write(styles_content)

    with open(os.path.join(build["archive"], "word/numbering.xml"), 'w', encoding = 'utf-8') as file:
        file.write(num_content)

    # Compress the archive
    with ZipFile(build["output-file"], 'w', ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(build["archive"]):
            for file in files:
                pathname = os.path.join(root, file)
                arcname = os.path.relpath(pathname, build["archive"])
                zipf.write(pathname, arcname)


def render_text():

    config = load_config()
    paths = config['output']['text']
    templates = paths['templates']
    build = paths['build']

    # Import the resume data
    with open(RESUME_DATA, "r", encoding = "utf-8") as file:
        resume_data = yaml.safe_load(file)

    env = Environment(loader = FileSystemLoader('.'),
                      trim_blocks = True, lstrip_blocks = True)
    text_template = env.get_template(templates["template"])

    content = text_template.render(resume_data)

    with open(build["output-file"], 'w', encoding = 'utf-8') as file:
        file.write(content)


def latexify(text):

    escape = {
        '\\' : r'\textbackslash',
        '&' : r'\&',
        '%' : r'\%',
        '$' : r'\$',
        '#' : r'\#'
    }

    for char, repl in escape.items():
        text = text.replace(char, repl)

    return text


def render_latex():

    config = load_config()
    paths = config['output']['latex']
    templates = paths['templates']
    build = paths['build']

    # Import the resume data
    with open(RESUME_DATA, "r", encoding = "utf-8") as file:
        resume_data = yaml.safe_load(file)

    env = Environment(loader = FileSystemLoader('.'),
                      trim_blocks = True, lstrip_blocks = True,
                      block_start_string = '<%',
                      block_end_string = '%>',
                      variable_start_string = '<<',
                      variable_end_string = '>>',
                      comment_start_string = '<#',
                      comment_end_string = '#>')
    env.filters['latexify'] = latexify

    template = env.get_template(templates["template"])
    content = template.render(resume_data)

    with open(build["tex-output-file"], 'w', encoding = 'utf-8') as file:
        file.write(content)

    subprocess.run(["pdflatex", build["tex-output-file"], 
                    "-output-directory=" + build["build-dir"]]) 


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument("--type", help="The output file type ('text', 'txt', 'docx', 'latex', 'pdf', 'all')")
    args = parser.parse_args()

    if args.type == 'txt' or args.type == 'text':
        render_text()

    elif args.type == 'docx':
        render_docx()
        
    elif args.type == 'latex' or args.type == 'pdf':
        render_latex()

    elif args.type == 'all':
        render_text()
        render_docx()
        render_latex()
    else:
        print("Not a supported output type.", file = sys.stderr)