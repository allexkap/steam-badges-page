from flask import Flask, render_template, request

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['GET'])
def process():
    input_data = request.args.get('input')
    return f'<h1>Processed Input</h1><p>{input_data}</p>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
