INSERT INTO cars(id, model, brand, category, quantity, description, price_per_day, location_id) VALUES
(1, 'Logan', 'Reno', 'economy', 5, 'Авто для небольшой и не дальней поездки', 10000, 1),
(2, 'Oktavia', 'Skoda', 'economy', 10, 'Авто для поезки с семьей за город', 12000, 1),
(3, 'CT200h', 'Lexus', 'compact', 3, 'Авто для поездки за продуктами и не только', 17000, 2),
(4, 'Ларгус', 'Lada', 'compact', 7, 'Авто для переезда', 15000, 1),
(5, '5 series', 'BMW', 'luxury', 2, 'Авто для деловых поездок', 35000, 1),
(6, 'S-CLASS', 'Mercedes', 'luxury', 3, 'Авто для состоятельных бизнесменов', 40000, 2),
(7, 'S-CLASS', 'Mercedes', 'luxury', 3, 'Авто для состоятельных бизнесменов', 40000, 3),
(8, 'Ларгус', 'Lada', 'compact', 7, 'Авто для переезда', 15000, 3),
(9, 'Oktavia', 'Skoda', 'economy', 10, 'Авто для поезки с семьей за город', 12000, 3)


INSERT INTO bookings(id, user_id, car_id, start_date, end_date, total_price, status) VALUES
(1, 1, 1, '2024-11-15', '2024-11-25', 100000, 'confirmed'),
(2, 1, 6, '2024-11-26', '2024-11-29', 160000, 'in_process'),
(3, 2, 1, '2024-11-30', '2024-12-02', 30000, 'in_process'),
(4, 2, 1, '2024-11-26', '2024-11-30', 50000, 'canceled')

