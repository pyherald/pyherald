import pathlib
import calendar
import sys
import datetime
from os.path import join
import os
import settings
import markdown
from flask import Flask
from jamstack.api.template import base_context, generate
from livereload import Server
from email import utils as emailutils
from data.data import infos as data_infos
import time
import urllib.parse
import html

context = base_context()
context.update({'path': '/'})


base_path = pathlib.Path(__file__).parent.absolute()


def get_description(article_ref):
    titles = []
    with open(f'data/editions/{article_ref}/main.md') as f:
        markdown = f.read().split('\n')
        for line in markdown:
            if line.strip().startswith('##'):
                title = line.strip().split()[1]
                titles.append(title)
    with open(f'data/editions/{article_ref}/sidebar.md') as f:
        markdown = f.read().split('\n')
        for line in markdown:
            if line.strip().startswith('##'):
                title = line.strip().split()[1]
                titles.append(title)

    return 'Main titles for this edition: '+ ', '.join(titles)

def day_name_from_article_ref(folder_name):
    date = datetime.datetime.strptime(folder_name, "%d_%m_%Y")

    day_name = calendar.day_name[date.weekday()]
    month_name = calendar.month_name[date.month]
    date_edition = f'{day_name} {month_name} {date.day}, {date.year}'

    return date_edition




context.update({
    "info": settings.info
})


def gen_articles():
    directory = "./data/editions/"  
    folders = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    for folder in folders:
        try:
            os.mkdir(os.path.join(settings.OUTPUT_FOLDER, 'articles'))
        except Exception as e:
            # print(e)
            pass
        try:
            os.mkdir(os.path.join(settings.OUTPUT_FOLDER, 'articles', folder))
        except Exception as e:
            # print(e)
            pass

        md = markdown.Markdown(extensions=["extra", "smarty", "meta"])
        with open(f'./data/editions/{folder}/main.md') as f:
            text = f.read()
            html = md.convert(text)
            article = html
        with open(f'data/editions/{folder}/sidebar.md') as f:
            text = f.read()
            html = md.convert(text)
            sidebar = html

        # date_list = article_folder.split('_')
        date_edition = day_name_from_article_ref(folder)
        context.update({
            'permalink': f'/articles/{folder}', 
            'display_home': True, 
            'date_edition': date_edition, 
            'path': '../../', 
            'article': article,
            'sidebar': sidebar 
            })
        generate(f'articles/article.html', 
            join(settings.OUTPUT_FOLDER, 'articles', f'{folder}', 'index.html'), **context)


def gen_archives():
    try:
        os.mkdir(os.path.join(settings.OUTPUT_FOLDER, 'archives'))
    except Exception as e:
        # print(e)
        pass

    directory = "./data/editions/"  
    folders = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    folders = sorted(folders, key=lambda date: datetime.datetime.strptime(date, "%d_%m_%Y"), reverse=True)
    context.update({'archive_articles': folders, 'day_name_from_article_ref':day_name_from_article_ref})
    generate(f'archives.html', 
        join(settings.OUTPUT_FOLDER, 'archives', 'index.html'), **context)


def gen_rss():
    directory = "./data/editions/"  
    folders = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    
    articles = folders
    items = []
    for article in articles:
        article_ref = article.removesuffix('.html')


        # %Y-%m-%dT%H:%M:%S.%f%z
        now = datetime.datetime.strptime(article_ref, f'%d_%m_%Y')
        nowtuple = now.timetuple()
        nowtimestamp = time.mktime(nowtuple)
        rfc822 = emailutils.formatdate(nowtimestamp)
        pub_date = rfc822

        items.append({
            'link': f'https://pyherald.com/articles/{article_ref}',
            'title': day_name_from_article_ref(article_ref),
            'description': get_description(article_ref),
            'pub_date': pub_date,
            'media': 'https://picsum.photos/200/300',
            })

        context = {}
        now = datetime.datetime.now()
        nowtuple = now.timetuple()
        nowtimestamp = time.mktime(nowtuple)
        rfc822 = emailutils.formatdate(nowtimestamp)
        last_build_date = rfc822
        context.update({'items': items, 'last_build_date': last_build_date})
        generate('rss.xml', 
            join(settings.OUTPUT_FOLDER, 'rss.xml'), **context)

def gen_homepage():
    md = markdown.Markdown(extensions=["extra", "smarty", "meta"])
    folder = settings.current_edition
    with open(f'./data/editions/{folder}/main.md') as f:
        text = f.read()
        html = md.convert(text)
        article = html
    with open(f'data/editions/{folder}/sidebar.md') as f:
        text = f.read()
        html = md.convert(text)
        sidebar = html
    context.update({
        'display_home': False, 
        'date_edition': day_name_from_article_ref(settings.current_edition),
        'permalink': f'/articles/{settings.current_edition}',
        'article': article,
        'sidebar': sidebar
        })

    generate(f'articles/article.html', join(
        settings.OUTPUT_FOLDER, 'index.html'), **context)



def main(args):
    def gen():
        gen_articles()

        gen_homepage()
        gen_archives()
        gen_rss()

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
