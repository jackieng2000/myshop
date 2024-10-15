export PGPASSWORD='1234'

# In zsh chmod +x script_import.sh and run ./script_import.sh

# the code -c "TRUNCATE shop2_coursesession;" will delete all records 
# in the table before importing


echo "Start import"
echo "shop2 coursesession"

# Truncate tables with CASCADE
echo "Truncating tables..."
psql -U dbadmin -h localhost -d myshop_prod -c "TRUNCATE TABLE shop2_coursesession, shop2_instructor, shop2_menuitem CASCADE;"

# Importing data
echo "Importing data into instructor..."
psql -U dbadmin -h localhost -d myshop_prod -c "\COPY shop2_instructor FROM 'output_file_shop2_instructor.csv' WITH (FORMAT csv, HEADER);"

echo "Importing data into menuitem..."
psql -U dbadmin -h localhost -d myshop_prod -c "\COPY shop2_menuitem FROM 'output_file_shop2_menuitem.csv' WITH (FORMAT csv, HEADER);"

echo "Importing data into coursesession..."
psql -U dbadmin -h localhost -d myshop_prod -c "\COPY shop2_coursesession FROM 'output_file_shop2_coursesession.csv' WITH (FORMAT csv, HEADER);"


# Reset the ID sequence
psql -U dbadmin -h localhost -d myshop_prod -c "SELECT setval('shop2_coursesession_id_seq', (SELECT COALESCE(MAX(id), 0) FROM shop2_coursesession));"
psql -U dbadmin -h localhost -d myshop_prod -c "SELECT setval('shop2_instructor_id_seq', (SELECT COALESCE(MAX(id), 0) FROM shop2_instructor));"
psql -U dbadmin -h localhost -d myshop_prod -c "SELECT setval('shop2_menuitem_id_seq', (SELECT COALESCE(MAX(id), 0) FROM shop2_menuitem));"


echo "Import completed."