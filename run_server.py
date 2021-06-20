from app import create_app
from global_var import _init, init_load

app = create_app()

# # global_var
# _init()
# init_load()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port='20000', debug=True)
