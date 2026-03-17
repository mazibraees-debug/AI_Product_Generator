import os
from flask import Flask, render_template, request
import pandas as pd
from generator import generate_content

app = Flask(__name__)

# -------------------------
# Cloudinary config
# -------------------------
CLOUD_NAME = "dbgpn8lq8"
CLOUD_FOLDER = "products"

# -------------------------
# Load Excel file safely
# -------------------------
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_FILE = os.path.join(BASE_DIR, "swag_products.xlsx")
    data = pd.read_excel(DATA_FILE, dtype=str)
    print("✅ Dataset Loaded Successfully")
    print("Total products:", len(data))
except Exception as e:
    print("❌ Failed to load dataset:", e)
    data = pd.DataFrame()  # empty DataFrame to prevent crashes

# -------------------------
# Home route
# -------------------------
@app.route('/')
def home():
    try:
        products = data.to_dict(orient="records")
        print("\n=== HOMEPAGE LOADED ===")
        print("Products sent to frontend:", len(products))
        return render_template("index.html", products=products)
    except Exception as e:
        return f"Error loading homepage: {e}", 500

# -------------------------
# Generate route
# -------------------------
@app.route('/generate', methods=['POST'])
def generate():
    try:
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

        # Product info
        product_name = product['ItemName']
        brand = product['Brand']
        category = product['MainCategory']
        subcategory = product['SubCategory']
        color = product['Color']
        description = product['LongDescription']

        # AI content generation
        content = generate_content(
            product_name,
            brand,
            category,
            subcategory,
            color,
            description
        )
        print("✅ AI content generated")

        # Color variants
        colors = data[data['ItemCode'] == product_code]['Color'].dropna().unique().tolist()
        print("Available colors:", colors)

        # Printing options
        print_technique = product.get('DefaultPrintTechnique', '')
        print_location = product.get('DefaultPrintLoc', '')
        print_area = product.get('MaxPrintAreaDefault', '')

        # Cloudinary image URL
        image_file = f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/{CLOUD_FOLDER}/{product_code}.png"
        print("🖼 Image URL sent to UI:", image_file)

        # Render result page
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
        print("❌ Error in /generate route:", e)
        return f"Error generating product: {e}", 500

# -------------------------
# Run locally
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)