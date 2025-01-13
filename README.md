# Developing a Single Page App with Flask and Vue.js

### Want to learn how to build this?

Check out the [tutorial](https://testdriven.io/developing-a-single-page-app-with-flask-and-vuejs).

## Want to use this project?

1. Fork/Clone

1. Run the server-side Flask app in one terminal window:

   ```sh
   $ cd server
   $ python3 -m venv env
   $ source env/bin/activate
   (env)$ pip install -r requirements.txt
   (env)$ cd src
   (env)$ python3 app.py
   ```

   Navigate to [http://localhost:5001](http://localhost:5001)

1. Run the client-side Vue app in a different terminal window:

   ```sh
   $ cd client
   $ npm install
   $ npm run dev
   ```

   Navigate to [http://localhost:5173](http://localhost:5173)

打包命令，在 server 目录下，执行

```sh
pyinstaller --onefile \
  --name "my_flask_vue_crud" \
  --add-data "src/static:static" \
  src/app.py
```

```
flask-vue-crud
├─ .gitignore
├─ .nvmrc
├─ .vscode
│  └─ settings.json
├─ LICENSE
├─ README.md
├─ client
│  ├─ .gitignore
│  ├─ .vscode
│  │  └─ extensions.json
│  ├─ README.md
│  ├─ dist
│  │  ├─ assets
│  │  │  ├─ index-a902c170.js
│  │  │  └─ index-c3fe9b93.css
│  │  ├─ favicon.ico
│  │  └─ index.html
│  ├─ index.html
│  ├─ package-lock.json
│  ├─ package.json
│  ├─ public
│  │  └─ favicon.ico
│  ├─ src
│  │  ├─ App.vue
│  │  ├─ assets
│  │  │  └─ logo.svg
│  │  ├─ components
│  │  │  ├─ Alert.vue
│  │  │  ├─ Books.vue
│  │  │  ├─ HelloWorld.vue
│  │  │  └─ Ping.vue
│  │  ├─ main.js
│  │  └─ router
│  │     └─ index.js
│  └─ vite.config.js
└─ server
   ├─ config.py
   ├─ requirements.txt
   └─ src
      ├─ app.py
      ├─ data
      │  └─ books.json
      ├─ static
      │  ├─ assets
      │  │  ├─ index-a902c170.js
      │  │  └─ index-c3fe9b93.css
      │  ├─ favicon.ico
      │  └─ index.html
      └─ utils
         └─ file_handler.py

```
