export PGPASSWORD='1234'

# In zsh chmod +x script_import.sh and run ./script_import.sh

# the code -c "TRUNCATE shop2_coursesession;" will delete all records 
# in the table before importing


echo "Start import shop1"
echo "shop2 coursesession"

# Truncate tables with CASCADE
echo "Truncating tables..."
psql -U dbadmin -h localhost -d myshop_prod -c "TRUNCATE TABLE shop1_cakes, shop1_ordering, shop1_productdetail CASCADE;"

# Importing data
echo "Importing data into cakes..."
psql -U dbadmin -h localhost -d myshop_prod -c "\COPY shop1_cakes FROM 'output_file_shop1_cakes.csv' WITH (FORMAT csv, HEADER);"


#echo "Importing data into ordering.."
#psql -U dbadmin -h localhost -d myshop_prod -c "\COPY shop1_ordering FROM 'output_file_shop1_ordering.csv' WITH (FORMAT csv, HEADER);"


echo "Importing data into ordering.."
psql -U dbadmin -h localhost -d myshop_prod -c "\COPY shop1_productdetail FROM 'output_file_shop1_productdetail.csv' WITH (FORMAT csv, HEADER);"


# Reset the ID sequence
psql -U dbadmin -h localhost -d myshop_prod -c "SELECT setval('shop1_cakes_id_seq', (SELECT COALESCE(MAX(id), 0) FROM shop1_cakes));"
psql -U dbadmin -h localhost -d myshop_prod -c "SELECT setval('shop1_ordering_id_seq', (SELECT COALESCE(MAX(id), 0) FROM shop1_ordering));"
psql -U dbadmin -h localhost -d myshop_prod -c "SELECT setval('shop1_productdetail_id_seq', (SELECT COALESCE(MAX(id), 0) FROM shop1_productdetail));"


echo "Import completed."