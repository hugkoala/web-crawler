from flask import Flask, render_template
from reddit_web_crawler import RedditWebCrawler

# Flask
app = Flask(__name__, template_folder='templates')


@app.route('/WebCrawler/<web>/<board>')
def index(web, board):
    web_crawler = web_to_crawler(web)

    return render_template('articles.html', articles=web_crawler.parse_articles(board=board), board=board)


def web_to_crawler(web):
    switcher = {
        'reddit' : RedditWebCrawler
    }

    crawler = switcher.get(web)
    return crawler()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
