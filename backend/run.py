from app import create_app, socketio, db
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = create_app()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
