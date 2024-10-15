export PGPASSWORD='1234'

# In zsh chmod +x script_import.sh and run ./script_import.sh

# the code -c "TRUNCATE shop2_coursesession;" will delete all records 
# in the table before importing


echo "Start import shop"

# Truncate tables with CASCADE
echo "Truncating tables..."
psql -U dbadmin -h localhost -d myshop_prod -c "TRUNCATE TABLE shop_product, shop_category CASCADE;"

# Importing data
echo "Importing data into category..."
psql -U dbadmin -h localhost -d myshop_prod -c "\COPY shop_category FROM 'output_file_shop_category.csv' WITH (FORMAT csv, HEADER);"

echo "Importing data into product..."
psql -U dbadmin -h localhost -d myshop_prod -c "\COPY shop_product FROM 'output_file_shop_product.csv' WITH (FORMAT csv, HEADER);"

# Reset the ID sequence
psql -U dbadmin -h localhost -d myshop_prod -c "SELECT setval('shop_category_id_seq', (SELECT COALESCE(MAX(id), 0) FROM shop_category));"
psql -U dbadmin -h localhost -d myshop_prod -c "SELECT setval('shop_product_id_seq', (SELECT COALESCE(MAX(id), 0) FROM shop_product));"

echo "Import completed."