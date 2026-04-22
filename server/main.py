from __init__ import create_app

app = create_app()

if __name__ == '__main__':
    import uvicorn
    
    print('Starting server...')
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
    )