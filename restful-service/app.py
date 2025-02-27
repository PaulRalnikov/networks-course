#!flask/bin/python
from flask import Flask
from flask import request
from flask import abort
from pathlib import Path
from flask import send_file
import os


app = Flask(__name__)

products = {}

next_id = 1

def generate_id():
    global next_id
    result = next_id
    next_id += 1
    return result

@app.route('/')
def index():
    return "Hello, World!"


@app.route('/product', methods=["POST"])
def create_product():
    global products
    if not request.json or not "name" in request.json or not "description" in request.json:
        abort(400)

    id = generate_id()

    product = {
        "id": id,
        "name": request.json["name"],
        "description": request.json["description"]
    }
    products[id] = product
    return product, 201

@app.route('/product/<int:product_id>', methods=["GET"])
def get_product(product_id):
    global products

    if products.get(product_id, None) == None:
        abort(404)
    return products[product_id], 200

@app.route('/product/<int:product_id>', methods=["PUT"])
def update_product(product_id):
    global products

    if products.get(product_id, None) == None:
        abort(404)

    if not request.json:
        abort(400)

    # do not change icon field not to broke
    if "name" in request.json:
        products[product_id]["name"] = request.json.get("name")

    if "description" in request.json:
        products[product_id]["description"] = request.json.get("description")

    return products[product_id], 202

@app.route('/product/<int:product_id>', methods=["DELETE"])
def delete_product(product_id):
    global products

    if products.get(product_id, None) == None:
        abort(404)

    return products.pop(product_id), 200

@app.route('/products', methods=["GET"])
def get_products():
    global products

    return list(products.values())

@app.route('/product/<int:product_id>/image', methods=["POST"])
def load_icon(product_id):
    global products

    if products.get(product_id, None) == None:
        abort(404)

    if not "icon" in request.files:
        abort(400)

    icon = request.files.get("icon", "")

    icon_path = f"icons/{product_id}/icon.png"

    dirlist = icon_path.split("/")[:-1]
    dir_prefix = ""

    for dir in dirlist:
        new_dir_prefix = f"{dir_prefix}/{dir}" if len(dir_prefix) != 0 else dir
        if not dir in os.listdir(dir_prefix if len(dir_prefix) != 0 else None):
            os.mkdir(new_dir_prefix)
        dir_prefix = new_dir_prefix

    icon.save(icon_path)

    products[product_id]["icon"] = icon_path
    return products[product_id], 200

@app.route('/product/<int:product_id>/image', methods=["GET"])
def get_icon(product_id):
    global products

    if products.get(product_id, None) == None:
        abort(404)

    icon_path = products[product_id]["icon"]

    icon = Path(icon_path)

    if icon.is_file():
        return send_file(icon)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
