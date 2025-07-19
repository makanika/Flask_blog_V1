# run.py

# Import the 'app' variable from your 'app' package (__init__.py)
from app import app

if __name__ == '__main__':
    # This block ensures the server only runs when the script is executed directly
    # debug=True will automatically reload the server when you make code changes
    app.run(debug=True)

