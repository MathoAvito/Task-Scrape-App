from venv import create
from website import create_app  # from 'website' folder import 'create_app' function

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # re-run the server anytime the code changes