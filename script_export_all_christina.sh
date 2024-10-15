#!/bin/bash

# Define global environment variables
export PGPASSWORD='1234'
export PGUSER='postgres'
export PGHOST='localhost'
export PGDATABASE='myshop_prod'

echo "Starting export"

# Exporting data from various tables
echo "Catalog"
psql -c "COPY (SELECT * FROM shop_category) TO STDOUT WITH CSV HEADER" > output_file_shop_category.csv

echo "Product"
psql -c "COPY (SELECT * FROM shop_product) TO STDOUT WITH CSV HEADER" > output_file_shop_product.csv

echo "Shop1 Cakes"
psql -c "COPY (SELECT * FROM shop1_cakes) TO STDOUT WITH CSV HEADER" > output_file_shop1_cakes.csv

echo "Shop1 Ordering"
psql -c "COPY (SELECT * FROM shop1_ordering) TO STDOUT WITH CSV HEADER" > output_file_shop1_ordering.csv

echo "Shop1 Product Detail"
psql -c "COPY (SELECT * FROM shop1_productdetail) TO STDOUT WITH CSV HEADER" > output_file_shop1_productdetail.csv

echo "Shop2 Course Session"
psql -c "COPY (SELECT * FROM shop2_coursesession) TO STDOUT WITH CSV HEADER" > output_file_shop2_coursesession.csv

echo "Shop2 Instructor"
psql -c "COPY (SELECT * FROM shop2_instructor) TO STDOUT WITH CSV HEADER" > output_file_shop2_instructor.csv

echo "Shop2 Menu Item"
psql -c "COPY (SELECT * FROM shop2_menuitem) TO STDOUT WITH CSV HEADER" > output_file_shop2_menuitem.csv

echo "Shop3 Booking"
psql -c "COPY (SELECT * FROM shop3_booking) TO STDOUT WITH CSV HEADER" > output_file_shop3_booking.csv

echo "Shop3 Studio"
psql -c "COPY (SELECT * FROM shop3_studio) TO STDOUT WITH CSV HEADER" > output_file_shop3_studio.csv

echo "Shop3 Time Slot"
psql -c "COPY (SELECT * FROM shop3_timeslot) TO STDOUT WITH CSV HEADER" > output_file_shop3_timeslot.csv

echo "Orders Order"
psql -c "COPY (SELECT * FROM orders_order) TO STDOUT WITH CSV HEADER" > output_file_orders_order.csv

echo "Orders Order Item"
psql -c "COPY (SELECT * FROM orders_orderitem) TO STDOUT WITH CSV HEADER" > output_file_orders_orderitem.csv

echo "Completed"
