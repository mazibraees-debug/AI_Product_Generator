import os
from flask import Flask, render_template, request
import pandas as pd
from generator import generate_content

app = Flask(__name__)

# Cloudinary config
CLOUD_NAME = "dbgpn8lq8"
CLOUD_FOLDER = "products"

# Load Excel file safely
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FILE = os.path.join(BASE_DIR, "swag_products.xlsx")
    data = pd.read_excel(DATA_FILE, dtype=str)
    print("✅ Dataset Loaded Successfully")
    print("Total products:", len(data))
except Exception as e:
    print("❌ Failed to load dataset:", e)
    data = pd.DataFrame()

@app.route('/')
def home():
    try:
        products = data.to_dict(orient="records")
        return render_template("index.html", products=products)
    except Exception as e:
        return f"Error loading homepage: {e}", 500

@app.route('/generate', methods=['POST'])
def generate():
    try:
        product_code = str(request.form.get('code')).strip()

        product_row = data[data['ItemCode'] == product_code]
        if product_row.empty:
            return "Product not found", 404

        product = product_row.iloc[0]

        product_name = product['ItemName']
        brand = product['Brand']
        category = product['MainCategory']
        subcategory = product['SubCategory']
        color = product['Color']
        description = product['LongDescription']

        content = generate_content(
            product_name,
            brand,
            category,
            subcategory,
            color,
            description
        )

        colors = data[data['ItemCode'] == product_code]['Color'].dropna().unique().tolist()

        print_technique = product.get('DefaultPrintTechnique', '')
        print_location = product.get('DefaultPrintLoc', '')
        print_area = product.get('MaxPrintAreaDefault', '')

        image_file = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/{CLOUD_FOLDER}/{product_code}.png"

        return render_template(
            "result.html",
            product_name=product_name,
            brand=brand,
            category=category,
            subcategory=subcategory,
            colors=colors,
            description=description,
            print_technique=print_technique,
            print_location=print_location,
            print_area=print_area,
            image_file=image_file,
            content=content
        )
    except Exception as e:
        return f"Error generating product: {e}", 500

if __name__ == "__main__":
    app.run(debug=True)