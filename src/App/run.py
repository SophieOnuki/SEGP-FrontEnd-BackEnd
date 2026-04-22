import os
import sys

#add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, init_db

if __name__ == '__main__':
    app = create_app()
    init_db()
    app.run(debug=True, host='127.0.0.1', port=5000)

#C:\Users\Navya\AppData\Local\Programs\Python\Python310\python.exe run.py