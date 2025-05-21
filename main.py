import json

from flask import Flask, render_template, request

app = Flask(__name__)

data = json.load(open('./db.json'))


@app.route('/', methods=['GET', 'POST'])
def find_app():
    # Show the form and handle submission
    pasted_ids = []
    if request.method == 'POST':
        ids_raw = request.form.get('app_ids', '')
        pasted_ids = [i.strip() for i in ids_raw.split(',') if i.strip().isdigit()]
    return render_template('find_app.html', pasted_ids=pasted_ids)

@app.route('/badges')
def badges():
    # Get app_ids from query or session
    app_ids = request.args.get('app_ids', '')
    app_ids = [int(i) for i in app_ids.split(',') if i.isdigit()]
    preview_url_template = data.get('preview_url')
    filtered_apps = []
    for app in data['apps']:
        if app['app_id'] in app_ids:
            for badge in app['badges']:
                badge['img_url'] = data['badge_url'].format(app_id=app['app_id'], hash=badge['hash'])
            app['preview_url'] = preview_url_template.format(app_id=app['app_id'])
            filtered_apps.append(app)
    return render_template('badges.html', apps=filtered_apps, app_ids=','.join(str(i) for i in app_ids))

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
