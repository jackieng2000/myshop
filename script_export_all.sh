export PGPASSWORD='1234'

echo "start export"

echo "catalog"
psql -U dbadmin -h localhost -d myshop_prod -c "COPY (SELECT * FROM shop_category) TO STDOUT WITH CSV HEADER" > output_file_shop_category.csv;
echo "product"
psql -U dbadmin -h localhost -d myshop_prod -c "COPY (SELECT * FROM shop_product) TO STDOUT WITH CSV HEADER" > output_file_shop_product.csv;

echo "shop1 cakes"
psql -U dbadmin -h localhost -d myshop_prod -c "COPY (SELECT * FROM shop1_cakes) TO STDOUT WITH CSV HEADER" > output_file_shop1_cakes.csv;
echo "shop1 ordering"
psql -U dbadmin -h localhost -d myshop_prod -c "COPY (SELECT * FROM shop1_ordering) TO STDOUT WITH CSV HEADER" > output_file_shop1_ordering.csv;
echo "shop1 productdetail"
psql -U dbadmin -h localhost -d myshop_prod -c "COPY (SELECT * FROM shop1_productdetail) TO STDOUT WITH CSV HEADER" > output_file_shop1_productdetail.csv;

echo "shop2 coursesession"
psql -U dbadmin -h localhost -d myshop_prod -c "COPY (SELECT * FROM shop2_coursesession) TO STDOUT WITH CSV HEADER" > output_file_shop2_coursesession.csv;
echo "shop2 instructor"
psql -U dbadmin -h localhost -d myshop_prod -c "COPY (SELECT * FROM shop2_instructor) TO STDOUT WITH CSV HEADER" > output_file_shop2_instructor.csv;
echo "shop2 menuitem"
psql -U dbadmin -h localhost -d myshop_prod -c "COPY (SELECT * FROM shop2_menuitem) TO STDOUT WITH CSV HEADER" > output_file_shop2_menuitem.csv;

echo "shop3 booking"
psql -U dbadmin -h localhost -d myshop_prod -c "COPY (SELECT * FROM shop3_booking) TO STDOUT WITH CSV HEADER" > output_file_shop3_booking.csv;
echo "shop3 studio"
psql -U dbadmin -h localhost -d myshop_prod -c "COPY (SELECT * FROM shop3_studio) TO STDOUT WITH CSV HEADER" > output_file_shop3_studio.csv;
echo "shop3 timeslot"
psql -U dbadmin -h localhost -d myshop_prod -c "COPY (SELECT * FROM shop3_timeslot) TO STDOUT WITH CSV HEADER" > output_file_shop3_timeslot.csv;

echo "orders order"
psql -U dbadmin -h localhost -d myshop_prod -c "COPY (SELECT * FROM orders_order) TO STDOUT WITH CSV HEADER" > output_file_orders_order.csv;
echo "orders orderitem"
psql -U dbadmin -h localhost -d myshop_prod -c "COPY (SELECT * FROM orders_orderitem) TO STDOUT WITH CSV HEADER" > output_file_orders_orderitem.csv;


echo "completed"