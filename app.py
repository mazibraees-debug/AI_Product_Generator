import os
from flask import Flask, render_template, request
import pandas as pd
from generator import generate_content

app = Flask(__name__)

# Cloudinary config
CLOUD_NAME = "dbgpn8lq8"
CLOUD_FOLDER = "products"

# Load Excel file (force string)
data = pd.read_excel("swag_products.xlsx", dtype=str)

print("Dataset Loaded Successfully")
print("Total products:", len(data))


@app.route('/')
def home():

    products = data.to_dict(orient="records")

    print("\n=== HOMEPAGE LOADED ===")
    print("Products sent to frontend:", len(products))

    return render_template("index.html", products=products)


@app.route('/generate', methods=['POST'])
def generate():

    product_code = str(request.form.get('code')).strip()

    print("\n==============================")
    print("Product requested:", product_code)

    # Find product in dataset
    product_row = data[data['ItemCode'] == product_code]

    if product_row.empty:
        print("❌ ERROR: Product not found in dataset")
        return "Product not found", 404

    product = product_row.iloc[0]

    print("✅ Product found:", product['ItemName'])

    # -------------------------
    # Product Basic Info
    # -------------------------

    product_name = product['ItemName']
    brand = product['Brand']
    category = product['MainCategory']
    subcategory = product['SubCategory']
    color = product['Color']
    description = product['LongDescription']

    # -------------------------
    # Generate AI Content
    # -------------------------

    content = generate_content(
        product_name,
        brand,
        category,
        subcategory,
        color,
        description
    )

    print("✅ AI content generated")

    # -------------------------
    # Color Variants
    # -------------------------

    colors = data[data['ItemCode'] == product_code]['Color'].dropna().unique().tolist()

    print("Available colors:", colors)

    # -------------------------
    # Printing Options
    # -------------------------

    print_technique = product['DefaultPrintTechnique']
    print_location = product['DefaultPrintLoc']
    print_area = product['MaxPrintAreaDefault']

    # -------------------------
    # Product Image (Cloudinary)
    # -------------------------

    print("\n🔎 Generating Cloudinary image path...")

    image_file = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/{CLOUD_FOLDER}/{product_code}.png"

    print("🖼 Image URL sent to UI:", image_file)

    # -------------------------
    # Render Result Page
    # -------------------------

    print("📄 Rendering result page")

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


if __name__ == "__main__":
    app.run(debug=True)