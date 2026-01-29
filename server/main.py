from __init__ import create_app, serialize_json

app = create_app(serialize_json())

if __name__ == '__main__':
    import uvicorn
    
    print('Starting server...')
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
    )