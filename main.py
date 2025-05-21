import json

from flask import Flask, render_template

app = Flask(__name__)

data = json.load(open('./db.json'))


@app.route('/')
def index():
    # Pass all apps and their badges to the template, and format preview_url for each app
    preview_url_template = data.get('preview_url')
    for app in data['apps']:
        for badge in app['badges']:
            badge['img_url'] = data['badge_url'].format(appid=app['appid'], hash=badge['hash'])
        # Always set preview_url for each app using the template
        app['preview_url'] = preview_url_template.format(appid=app['appid'])
    return render_template('index.html', apps=data['apps'])

if __name__ == '__main__':
    app.run(debug=True)
