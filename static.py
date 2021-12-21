import pathlib
import sys
from os.path import join
import os
import settings
import markdown
from flask import Flask
from jamstack.api.template import base_context, generate
from livereload import Server

context = base_context()


base_path = pathlib.Path(__file__).parent.absolute()




def article_info(article):
    with open(os.path.join(base_path, 'data', 'articles', article.removesuffix('.md')+'.md'), encoding="utf-8") as f:
        text = f.read()
    md = markdown.Markdown(extensions=["extra", "smarty", "meta"])
    html = md.convert(text)
    metadata = md.Meta
    slug = metadata["slug"][0]
    authors = metadata["authors"]
    title = metadata["title"][0]
    note = metadata["note"][0]
    source = metadata["source"][0]
    tags = metadata["tags"]

    return {
        'html': html,
        'slug': slug,
        'authors': authors,
        'title': title,
        'note': note,
        'source': source,
        'tags': tags
    }



context.update({
    "info": settings.info,
    'article_info': article_info
})



def main(args):
    def gen():
        generate('index.html', join(
            settings.OUTPUT_FOLDER, 'index.html'), **context)

    if len(args) > 1 and args[1] == '--server':
        app = Flask(__name__)

        # remember to use DEBUG mode for templates auto reload
        # https://github.com/lepture/python-livereload/issues/144
        app.debug = True
        server = Server(app.wsgi_app)

        # run a shell command
        # server.watch('.', 'make static')

        # run a function

        server.watch('.', gen, delay=5)
        server.watch('*.py')

        # output stdout into a file
        # server.watch('style.less', shell('lessc style.less', output='style.css'))

        server.serve()
    else:
        gen()


if __name__ == '__main__':
    main(sys.argv)
