# import cloudinary
# import cloudinary.uploader
# import os

# cloudinary.config(
#     cloud_name="dbgpn8lq8",
#     api_key="313243732582479",
#     api_secret="Pzxywvj1rOdrfbjn6IghbTKBNK0"
# )

# folder = "static/products"

# for img in os.listdir(folder):
#     path = os.path.join(folder, img)

#     if img.endswith((".jpg",".png",".jpeg")):
#         result = cloudinary.uploader.upload(path, folder="products")
#         print(result["secure_url"])

import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name="dbgpn8lq8",
    api_key="313243732582479",
    api_secret="Pzxywvj1rOdrfbjn6IghbTKBNK0"
)

folder = "static/products"

for img in os.listdir(folder):

    path = os.path.join(folder, img)

    if img.lower().endswith((".jpg", ".png", ".jpeg")):

        # remove extension to keep clean name
        filename = os.path.splitext(img)[0]

        result = cloudinary.uploader.upload(
            path,
            folder="products",
            public_id=filename,   # keeps same name
            overwrite=True        # replace if exists
        )

        print(f"{img} uploaded → {result['secure_url']}")