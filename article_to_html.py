import markdown
import frontmatter
import os

articles = os.listdir('articles')
md = markdown.Markdown()

for article_name in articles[0]:
    with open(os.path.join('articles', article_name), 'r') as article:
        article = frontmatter.load(article)
        html = md.convert(article.content)
        print(html[0:100])
