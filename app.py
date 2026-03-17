import os
import json
from flask import Flask, render_template, request
from generator import generate_content

app = Flask(__name__)

# -------------------------
# Load JSON dataset (UTF-8)
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "swag_products.json")

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

print("✅ Dataset loaded:", len(data), "products")

# -------------------------
# Homepage
# -------------------------
@app.route('/')
def home():
    return render_template("index.html", products=data)

# -------------------------
# Generate product content
# -------------------------
@app.route('/generate', methods=['POST'])
def generate():
    product_code = request.form.get('code')
    product = next((p for p in data if p["ItemCode"] == product_code), None)
    
    if not product:
        return "Product not found", 404

    content = generate_content(
        product["ItemName"],
        product["Brand"],
        product["MainCategory"],
        product["SubCategory"],
        product["Color"],
        product["LongDescription"]
    )

    return render_template(
        "result.html",
        product_name=product["ItemName"],
        brand=product["Brand"],
        category=product["MainCategory"],
        subcategory=product["SubCategory"],
        colors=[product["Color"]],
        description=product["LongDescription"],
        print_technique=product.get("DefaultPrintTechnique", ""),
        print_location=product.get("DefaultPrintLoc", ""),
        print_area=product.get("MaxPrintAreaDefault", ""),
        image_file=f"https://res.cloudinary.com/dbgpn8lq8/image/upload/products/{product_code}.png",
        content=content
    )

# -------------------------
# Run locally
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)