# my-workspace-6

A simple full-stack Todo app built with:

- HTML, CSS, and JavaScript for the frontend
- Flask for the Python backend
- SQLite for persistent task storage

## Project structure

```text
my-workspace-6/
├── main.py
├── index.html
├── style.css
├── script.js
├── requirements.txt
├── .gitignore
└── todo.db          # created automatically when the app runs; not committed
```

## Run locally

```bash
pip install -r requirements.txt
python main.py
```

Then open `http://127.0.0.1:5000` in your browser.

Tasks are stored in `todo.db`, so they persist when the Flask server restarts.
