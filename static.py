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
    infos = data_infos[article_ref]['article']
    titles = []
    for info in infos:
        title = article_info(info)['title']
        titles.append(title)
    return 'Main titles for this edition: '+ ', '.join(titles)
def day_name_from_article_ref(folder_name):
    date = datetime.datetime.strptime(folder_name, "%d_%m_%Y")

    day_name = calendar.day_name[date.weekday()]
    month_name = calendar.month_name[date.month]
    date_edition = f'{day_name} {month_name} {date.day}, {date.year}'

    return date_edition


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


def gen_articles():
    for file in os.listdir(os.path.join(base_path, 'templates', 'articles')):
        article_folder = file.strip('.html')
        try:
            os.mkdir(os.path.join(settings.OUTPUT_FOLDER, 'articles'))
        except Exception as e:
            # print(e)
            pass
        try:
            os.mkdir(os.path.join(settings.OUTPUT_FOLDER, 'articles', article_folder))
        except Exception as e:
            # print(e)
            pass

        # date_list = article_folder.split('_')
        date_edition = day_name_from_article_ref(article_folder)
        article_data = data_infos[article_folder]['article']
        sidebar_data = data_infos[article_folder]['sidebar']
        context.update({
            'permalink': f'/articles/{article_folder}', 
            'display_home': True, 
            'date_edition': date_edition, 
            'path': '../../', 
            'articles': [article_info(a) for a in article_data],
            'sidebar': [article_info(a) for a in sidebar_data]
            })
        generate(f'articles/{file}', 
            join(settings.OUTPUT_FOLDER, 'articles', f'{article_folder}', 'index.html'), **context)


def gen_archives():
    try:
        os.mkdir(os.path.join(settings.OUTPUT_FOLDER, 'archives'))
    except Exception as e:
        # print(e)
        pass

    articles = os.listdir(os.path.join(base_path, 'templates', 'articles'))
    context.update({'archive_articles': articles})
    generate(f'archives.html', 
        join(settings.OUTPUT_FOLDER, 'archives', 'index.html'), **context)


def gen_rss():
    articles = os.listdir(os.path.join(base_path, 'templates', 'articles'))
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
            'author': html.escape(data_infos[article_ref]['author']),
            'media': urllib.parse.quote_plus(data_infos[article_ref]['media']),
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
    article_data = data_infos[settings.current_edition]['article']
    sidebar_data = data_infos[settings.current_edition]['sidebar']
    context.update({
        'display_home': False, 
        'date_edition': day_name_from_article_ref(settings.current_edition),
        'permalink': f'/articles/{settings.current_edition}',
        'articles': [article_info(a) for a in article_data],
        'sidebar': [article_info(a) for a in sidebar_data]
        })
    generate(f'articles/{settings.current_edition}.html', join(
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
