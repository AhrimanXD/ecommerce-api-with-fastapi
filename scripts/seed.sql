-- scripts/seed.sql
-- First, ensure the tables are empty to avoid duplicates if this script is run multiple times
TRUNCATE TABLE products, categories RESTART IDENTITY CASCADE;

-- Insert Categories
INSERT INTO categories (name) VALUES
('Fruits & Vegetables'),
('Dairy & Eggs'),
('Bakery'),
('Meat & Seafood'),
('Beverages'),
('Snacks'),
('Frozen Foods'),
('Personal Care'),
('Household'),
('Electronics');

-- Insert Products with corrected unit values (KG, G, LITER, PIECE)
INSERT INTO products (
    name,
    description,
    category_id,
    price,
    stock,
    size,
    unit,
    is_available
) VALUES
-- Fruits & Vegetables (Category 1)
('Organic Red Apple', 'Crisp and sweet organic red apples, perfect for snacking or baking.', 1, 2.99, 150, 1, 'KG', TRUE),
('Banana Bunch', 'A ripe bunch of fresh yellow bananas, a great source of potassium.', 1, 1.49, 200, 1, 'KG', TRUE),
('Fresh Broccoli', 'Green, fresh broccoli crowns, ideal for steaming or stir-fries.', 1, 3.49, 75, 1, 'KG', TRUE),
('California Avocado', 'Creamy Hass avocados, perfect for guacamole or salads.', 1, 1.99, 60, 1, 'PIECE', TRUE),

-- Dairy & Eggs (Category 2)
('Whole Milk 1L', 'Fresh, pasteurized whole milk in a 1-liter bottle.', 2, 2.29, 50, 1, 'LITER', TRUE),
('Free-Range Eggs (12pk)', 'A dozen large free-range chicken eggs.', 2, 4.99, 40, 12, 'PIECE', TRUE),
('Greek Yogurt 500g', 'Creamy, high-protein plain Greek yogurt.', 2, 5.49, 30, 500, 'G', TRUE),
('Cheddar Cheese Block', 'Aged sharp cheddar cheese, 200g block.', 2, 4.25, 25, 200, 'G', TRUE),

-- Bakery (Category 3)
('Sourdough Baguette', 'Freshly baked artisan sourdough baguette.', 3, 3.99, 20, 1, 'PIECE', TRUE),
('Chocolate Chip Cookies (6pk)', 'Soft and chewy cookies with milk chocolate chips.', 3, 4.50, 35, 6, 'PIECE', TRUE),
('Whole Grain Bread', 'Healthy whole grain sandwich bread loaf.', 3, 3.25, 40, 1, 'PIECE', TRUE),

-- Meat & Seafood (Category 4)
('Skinless Chicken Breast', 'Boneless, skinless chicken breast fillets.', 4, 8.99, 30, 1, 'KG', TRUE),
('Fresh Salmon Fillet', 'Atlantic salmon fillet, perfect for grilling or baking.', 4, 12.99, 15, 1, 'KG', TRUE),
('Lean Ground Beef', '90% lean ground beef, great for burgers or pasta sauce.', 4, 7.49, 25, 1, 'KG', TRUE),

-- Beverages (Category 5)
('Sparkling Mineral Water 500ml', 'Naturally carbonated mineral water.', 5, 1.75, 100, 500, 'G', TRUE), -- Using G for grams as ml is not in enum
('Orange Juice 1L', '100% pure squeezed orange juice, not from concentrate.', 5, 3.99, 45, 1, 'LITER', TRUE),
('Premium Coffee Beans', 'Dark roast whole coffee beans, 500g bag.', 5, 14.99, 20, 500, 'G', TRUE),

-- Snacks (Category 6)
('Potato Chips', 'Classic salted potato chips, 200g bag.', 6, 2.99, 80, 200, 'G', TRUE),
('Granola Bars (5pk)', 'Pack of 5 oat and honey granola bars.', 6, 3.50, 60, 5, 'PIECE', TRUE),
('Dark Chocolate Bar', '70% cocoa dark chocolate bar, 100g.', 6, 2.25, 50, 100, 'G', TRUE),

-- Frozen Foods (Category 7)
('Vanilla Ice Cream', 'Creamy vanilla bean ice cream, 1L tub.', 7, 5.99, 30, 1, 'LITER', TRUE),
('Mixed Vegetables', 'A blend of frozen peas, corn, carrots, and green beans.', 7, 3.25, 40, 1, 'KG', TRUE),
('Pepperoni Pizza', 'Frozen pepperoni pizza, family size.', 7, 6.49, 22, 1, 'PIECE', TRUE),

-- Personal Care (Category 8) - Using G for items originally in ml
('Shampoo', 'Moisturizing shampoo for all hair types, 500ml bottle.', 8, 6.99, 35, 500, 'G', TRUE),
('Toothpaste', 'Fluoride toothpaste for cavity protection, 100ml tube.', 8, 3.49, 60, 100, 'G', TRUE),

-- Household (Category 9) - Using G for items originally in ml
('Dish Soap', 'Lemon-scented dishwashing liquid, 750ml bottle.', 9, 2.99, 40, 750, 'G', TRUE),
('Paper Towels (6 rolls)', 'Absorbent paper towels, 6-roll pack.', 9, 8.99, 30, 6, 'PIECE', TRUE),

-- Electronics (Category 10)
('Wireless Earbuds', 'Bluetooth 5.0 wireless earbuds with charging case.', 10, 79.99, 15, 1, 'PIECE', TRUE),
('USB-C Charging Cable', 'Durable 2m USB-C to USB-C fast charging cable.', 10, 19.99, 50, 1, 'PIECE', TRUE); -- Changed from 'm' to 'PIECE'