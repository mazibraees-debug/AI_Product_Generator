import random

def generate_content(product_name, brand, category, subcategory, color, long_description):
    """
    Generate AI-style content for a product.
    Returns a dictionary with title, description, and features.
    """

    # -------------------------
    # Title Templates
    # -------------------------
    title_templates = [
        f"{brand} {product_name} – Premium {subcategory} in {color}",
        f"{product_name} by {brand} | Stylish {category} for Promotions",
        f"Custom {product_name} – High Quality {subcategory}",
        f"{brand} {product_name} – Perfect Promotional {category}",
        f"{product_name} ({color}) | Premium {subcategory} for Corporate Gifts"
    ]

    # -------------------------
    # Description Templates
    # -------------------------
    description_templates = [
        f"The {brand} {product_name} is a premium {subcategory} designed for modern promotional campaigns. "
        f"This {color} {category} offers durability, style, and excellent branding opportunities. "
        f"{long_description}",

        f"Enhance your promotional strategy with the {product_name} from {brand}. "
        f"This high-quality {subcategory} in {color} is perfect for corporate giveaways, marketing events, "
        f"and brand promotions. {long_description}",

        f"Our {brand} {product_name} combines modern design with practical functionality. "
        f"This {color} {category} is ideal for businesses looking to create memorable promotional gifts. "
        f"{long_description}"
    ]

    # -------------------------
    # Feature Templates
    # -------------------------
    features = [
        f"Premium quality {subcategory}",
        f"Elegant {color} design",
        f"Trusted brand: {brand}",
        "Ideal for promotional campaigns",
        "Perfect for corporate giveaways",
        "Durable and lightweight construction"
    ]

    # -------------------------
    # Random Selection
    # -------------------------
    title = random.choice(title_templates)
    description = random.choice(description_templates)

    return {
        "title": title,
        "description": description,
        "features": features
    }