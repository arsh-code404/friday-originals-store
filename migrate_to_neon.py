import os
import sys
import sqlite3
import django
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'friday.settings')
django.setup()

from django.conf import settings
from django.core.files.base import ContentFile
from hii.models import Product

def migrate():
    # Path to local SQLite db
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
    if not os.path.exists(db_path):
        print(f"Error: SQLite database not found at {db_path}")
        return

    # Check database connection (should be Neon Postgres if DATABASE_URL is set)
    current_db = settings.DATABASES['default']
    print(f"Current Target Database Engine: {current_db.get('ENGINE')}")
    print(f"Current Target Database Host: {current_db.get('HOST') or 'Local'}")
    
    if 'sqlite' in current_db.get('ENGINE') and not os.environ.get('DATABASE_URL'):
        print("\nWARNING: Target database is local SQLite. Set the DATABASE_URL environment variable to target Neon Postgres.")
        confirm = input("Do you want to run the migration on local SQLite? (y/N): ")
        if confirm.lower() != 'y':
            print("Aborted.")
            return

    # Connect to SQLite
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT name, price, descp, \"set\", image1, image2 FROM hii_product")
        rows = cursor.fetchall()
        print(f"Found {len(rows)} products in SQLite database.")
    except Exception as e:
        print(f"Error reading from SQLite: {e}")
        conn.close()
        return

    success_count = 0
    skipped_count = 0

    for row in rows:
        name = row['name']
        price = row['price']
        descp = row['descp']
        prod_set = row['set']
        img1_path = row['image1']
        img2_path = row['image2']

        # Avoid duplicates in the target database
        try:
            if Product.objects.filter(name=name).exists():
                print(f"Product '{name}' already exists in target database. Skipping.")
                skipped_count += 1
                continue
        except Exception as e:
            print(f"Error querying target database: {e}")
            print("Make sure you have run migrations using 'python manage.py migrate' on the target database first.")
            conn.close()
            return

        print(f"Migrating '{name}'...")
        product = Product(
            name=name,
            price=price,
            descp=descp,
            set=prod_set
        )

        # Process image 1
        if img1_path:
            full_img1_path = os.path.join(settings.MEDIA_ROOT, img1_path)
            if os.path.exists(full_img1_path):
                print(f"  Uploading image1: {img1_path} to Cloudinary...")
                with open(full_img1_path, 'rb') as f:
                    product.image1.save(os.path.basename(img1_path), ContentFile(f.read()), save=False)
            else:
                print(f"  Warning: Local image file not found at {full_img1_path}")

        # Process image 2
        if img2_path:
            full_img2_path = os.path.join(settings.MEDIA_ROOT, img2_path)
            if os.path.exists(full_img2_path):
                print(f"  Uploading image2: {img2_path} to Cloudinary...")
                with open(full_img2_path, 'rb') as f:
                    product.image2.save(os.path.basename(img2_path), ContentFile(f.read()), save=False)
            else:
                print(f"  Warning: Local image file not found at {full_img2_path}")

        try:
            product.save()
            print(f"Successfully migrated '{name}' (ID: {product.id})")
            success_count += 1
        except Exception as e:
            print(f"Error migrating '{name}': {e}")

    print(f"\nMigration complete. Success: {success_count}, Skipped: {skipped_count}, Total: {len(rows)}")
    conn.close()

if __name__ == '__main__':
    migrate()
