from flask import Flask, render_template, request, send_file, abort
import os
import itertools

app = Flask(__name__)

def get_config_files():
    config_files = [f for f in os.listdir('configs') if f.endswith('.ovpn')]
    if not config_files:
        return None

    config_files.sort()
    return itertools.cycle(config_files)

config_cycle = get_config_files()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/get_ovpn', methods=['POST'])
def get_ovpn():
    if not config_cycle:
        abort(404, description="No OVPN files found")

    file_name = next(config_cycle)
    file_path = os.path.join('configs', file_name)

    try:
        response = send_file(file_path, as_attachment=True)

        def remove_file():
            try:
                os.remove(file_path)
            except Exception as error:
                app.logger.error("Error removing file %s: %s", file_path, error)

        response.call_on_close(remove_file)
        return response
    except Exception as e:
        abort(500, description="Error sending the file")

if __name__ == '__main__':
    app.run()
