#!/usr/bin/env python3
#
# A buggy web service in need of a database.
from flask import Flask, request, redirect, url_for

from logtooldb import get_article, get_author, get_error

app = Flask(__name__)

# HTML template for the tool
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>DB Tool</title>
    <style>
      h1, form { text-align: center; }
      textarea { width: 400px; height: 100px; }
      div.post { border: 1px solid #999;
                 padding: 10px 10px;
                 margin: 10px 20%%; }
      hr.postbound { width: 50%%; }
      em.date { color: #999 }
    </style>
  </head>
  <body>
    <h1>Queries processadas com sucesso!</h1>
    </br>
    <h2>Verifique o seu concole.</h2>
  </body>
</html>
'''


@app.route('/', methods=['GET'])
def main():
    articles = get_article()
    authors = get_author()
    errors = get_error()
    print "\n\n"
    print "Artigos mais lidos."
    print "\n"
    for art_name, art_views in articles:
        print art_name, "-", art_views, "views"
    print "\n\n"
    print "Autores mais lidos."
    print "\n"
    for aut_name, aut_views in authors:
        print aut_name, "-", aut_views, "views"
    print "\n\n"
    print "Erros de requisicao."
    print "\n"
    for er_date, er_value in errors:
        print "{:%b %d, %Y}".format(er_date), "-", er_value, "%% erros"
    print "\n\n"
    html = HTML_WRAP
    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
