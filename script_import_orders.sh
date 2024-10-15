export PGPASSWORD='1234'

# In zsh chmod +x script_import.sh and run ./script_import.sh

# the code -c "TRUNCATE shop2_coursesession;" will delete all records 
# in the table before importing


echo "Start import "

# Truncate tables with CASCADE
echo "Truncating tables..."
psql -U dbadmin -h localhost -d myshop_prod -c "TRUNCATE TABLE orders_order, orders_orderitem CASCADE;"

# Importing data
echo "Importing data into order..."
psql -U dbadmin -h localhost -d myshop_prod -c "\COPY orders_order FROM 'output_file_orders_order.csv' WITH (FORMAT csv, HEADER);"

echo "Importing data into orderitem..."
psql -U dbadmin -h localhost -d myshop_prod -c "\COPY orders_orderitem FROM 'output_file_orders_orderitem.csv' WITH (FORMAT csv, HEADER);"

# Reset the ID sequence
psql -U dbadmin -h localhost -d myshop_prod -c "SELECT setval('orders_order_id_seq', (SELECT COALESCE(MAX(id), 0) FROM orders_order));"
psql -U dbadmin -h localhost -d myshop_prod -c "SELECT setval('orders_orderitem_id_seq', (SELECT COALESCE(MAX(id), 0) FROM orders_orderitem));"

echo "Import completed."