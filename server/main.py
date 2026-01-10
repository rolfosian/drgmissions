from __init__ import create_app, serialize_json

app = create_app(serialize_json())

if __name__ == '__main__':
    print('Starting server...')
    app.run(threaded=True, host='0.0.0.0', debug=True, port=5000, use_reloader=False)
