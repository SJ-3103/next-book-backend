import os
from market import app

if __name__ == 'main':
    PORT = os.getenv("PORT")
    print('Server in running on port', PORT)
    app.run(debug=True)
