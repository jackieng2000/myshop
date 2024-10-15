export PGPASSWORD='1234'

# In zsh chmod +x script_import.sh and run ./script_import.sh

# the code -c "TRUNCATE shop2_coursesession;" will delete all records 
# in the table before importing


echo "Start import shop3"

# Truncate tables with CASCADE
echo "Truncating tables..."
psql -U dbadmin -h localhost -d myshop_prod -c "TRUNCATE TABLE shop3_booking, shop3_studio, shop3_timeslot CASCADE;"

echo "Importing data into booking..."
psql -U dbadmin -h localhost -d myshop_prod -c "\COPY shop3_booking FROM 'output_file_shop3_booking.csv' WITH (FORMAT csv, HEADER);"

echo "Importing data into studio..."
psql -U dbadmin -h localhost -d myshop_prod -c "\COPY shop3_studio FROM 'output_file_shop3_studio.csv' WITH (FORMAT csv, HEADER);"

echo "Importing data into timeslot..."
psql -U dbadmin -h localhost -d myshop_prod -c "\COPY shop3_timeslot FROM 'output_file_shop3_timeslot.csv' WITH (FORMAT csv, HEADER);"

# Reset the ID sequence
psql -U dbadmin -h localhost -d myshop_prod -c "SELECT setval('shop3_booking_id_seq', (SELECT COALESCE(MAX(id), 0) FROM shop3_booking));"
psql -U dbadmin -h localhost -d myshop_prod -c "SELECT setval('shop3_studio_id_seq', (SELECT COALESCE(MAX(id), 0) FROM shop3_studio));"
psql -U dbadmin -h localhost -d myshop_prod -c "SELECT setval('shop3_timeslot_id_seq', (SELECT COALESCE(MAX(id), 0) FROM shop3_timeslot));"


echo "Import completed."