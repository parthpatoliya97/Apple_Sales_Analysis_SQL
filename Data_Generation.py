import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# Set random seed for reproducibility
random.seed(42)

# Apple-specific data
APPLE_CATEGORIES = [
    ("CAT001", "iPhone"),
    ("CAT002", "iPad"),
    ("CAT003", "Mac"),
    ("CAT004", "Apple Watch"),
    ("CAT005", "AirPods"),
    ("CAT006", "Apple TV"),
    ("CAT007", "HomePod"),
    ("CAT008", "Accessories"),
    ("CAT009", "Services"),
    ("CAT010", "Software"),
    ("CAT011", "Beats")
]

# Generate 100 Apple stores
APPLE_STORES = []
for i in range(100):
    store_id = f"ST{str(i+1).zfill(3)}"
    store_name = f"Apple {fake.city()}"
    city = fake.city()
    country = fake.country()
    APPLE_STORES.append((store_id, store_name, city, country))

# Apple products with realistic names and pricing
APPLE_PRODUCTS = [
    # iPhone
    ("P001", "iPhone 15 Pro Max", "CAT001", 1199.00),
    ("P002", "iPhone 15 Pro", "CAT001", 999.00),
    ("P003", "iPhone 15 Plus", "CAT001", 899.00),
    ("P004", "iPhone 15", "CAT001", 799.00),
    ("P005", "iPhone 14 Pro Max", "CAT001", 1099.00),
    ("P006", "iPhone 14 Pro", "CAT001", 899.00),
    ("P007", "iPhone 14", "CAT001", 699.00),
    ("P008", "iPhone SE", "CAT001", 429.00),
    
    # iPad
    ("P009", "iPad Pro 12.9\"", "CAT002", 1099.00),
    ("P010", "iPad Pro 11\"", "CAT002", 799.00),
    ("P011", "iPad Air", "CAT002", 599.00),
    ("P012", "iPad 10.2\"", "CAT002", 329.00),
    ("P013", "iPad mini", "CAT002", 499.00),
    
    # Mac
    ("P014", "MacBook Pro 16\"", "CAT003", 2499.00),
    ("P015", "MacBook Pro 14\"", "CAT003", 1999.00),
    ("P016", "MacBook Air", "CAT003", 1099.00),
    ("P017", "iMac 24\"", "CAT003", 1299.00),
    ("P018", "Mac Studio", "CAT003", 1999.00),
    ("P019", "Mac Pro", "CAT003", 5999.00),
    ("P020", "Mac mini", "CAT003", 599.00),
    
    # Apple Watch
    ("P021", "Apple Watch Ultra 2", "CAT004", 799.00),
    ("P022", "Apple Watch Series 9", "CAT004", 399.00),
    ("P023", "Apple Watch SE", "CAT004", 249.00),
    
    # AirPods
    ("P024", "AirPods Pro 2", "CAT005", 249.00),
    ("P025", "AirPods 3", "CAT005", 169.00),
    ("P026", "AirPods Max", "CAT005", 549.00),
    
    # Apple TV
    ("P027", "Apple TV 4K", "CAT006", 129.00),
    
    # HomePod
    ("P028", "HomePod mini", "CAT007", 99.00),
    ("P029", "HomePod 2", "CAT007", 299.00),
    
    # Accessories
    ("P030", "Magic Keyboard", "CAT008", 299.00),
    ("P031", "Magic Mouse", "CAT008", 99.00),
    ("P032", "Apple Pencil 2", "CAT008", 129.00),
    ("P033", "Smart Folio", "CAT008", 79.00),
    ("P034", "Lightning Cable", "CAT008", 19.00),
    ("P035", "USB-C Cable", "CAT008", 19.00),
    
    # Services (represented as products)
    ("P036", "Apple Music 1 Year", "CAT009", 99.00),
    ("P037", "Apple TV+ 1 Year", "CAT009", 69.00),
    ("P038", "Apple Arcade 1 Year", "CAT009", 49.00),
    ("P039", "iCloud+ 2TB", "CAT009", 9.99),
    
    # Software
    ("P040", "Final Cut Pro", "CAT010", 299.99),
    ("P041", "Logic Pro", "CAT010", 199.99),
    
    # Beats
    ("P042", "Beats Studio Pro", "CAT011", 349.99),
    ("P043", "Beats Fit Pro", "CAT011", 199.99),
    ("P044", "Beats Solo 4", "CAT011", 199.99)
]

def generate_category_data():
    """Generate category data"""
    with open('apple_category.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['category_id', 'category_name'])
        writer.writerows(APPLE_CATEGORIES)
    print(f"Generated category data: {len(APPLE_CATEGORIES)} records")

def generate_store_data():
    """Generate store data"""
    with open('apple_store.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['store_id', 'store_name', 'city', 'country'])
        writer.writerows(APPLE_STORES)
    print(f"Generated store data: {len(APPLE_STORES)} records")

def generate_products_data():
    """Generate products data with realistic launch dates"""
    products = []
    current_date = datetime.now()
    
    # Add predefined products
    for product_id, product_name, category_id, price in APPLE_PRODUCTS:
        # Generate realistic launch dates based on product type
        if "iPhone 15" in product_name:
            start_date = current_date - timedelta(days=180)  # 6 months ago
            end_date = current_date - timedelta(days=90)     # 3 months ago
        elif "iPhone 14" in product_name:
            start_date = current_date - timedelta(days=540)  # 18 months ago
            end_date = current_date - timedelta(days=360)    # 12 months ago
        elif "iPhone SE" in product_name:
            start_date = current_date - timedelta(days=720)  # 24 months ago
            end_date = current_date - timedelta(days=540)    # 18 months ago
        elif "MacBook" in product_name:
            start_date = current_date - timedelta(days=360)  # 12 months ago
            end_date = current_date - timedelta(days=180)    # 6 months ago
        else:
            start_date = current_date - timedelta(days=1080) # 36 months ago
            end_date = current_date - timedelta(days=30)     # 1 month ago
        
        launch_date = fake.date_between(start_date=start_date, end_date=end_date)
        products.append([product_id, product_name, category_id, launch_date, price])
    
    # Generate additional products to reach 900
    for i in range(45, 901):
        category = random.choice(APPLE_CATEGORIES)
        category_id = category[0]
        category_name = category[1]
        
        # Generate product names based on category
        if category_name == "iPhone":
            product_name = f"iPhone {random.choice(['13', '12', '11'])} {random.choice(['Pro', '', 'mini'])}"
        elif category_name == "iPad":
            product_name = f"iPad {random.choice(['9th Gen', '8th Gen', 'Air 4'])}"
        elif category_name == "Mac":
            product_name = f"MacBook {random.choice(['Pro 13\"', 'Air M1'])}"
        else:
            product_name = f"Apple {category_name} {fake.word().capitalize()}"
        
        product_id = f"P{str(i).zfill(3)}"
        price = round(random.uniform(49.99, 999.99), 2)
        
        # Random launch date between 4 years ago and 1 month ago
        start_date = current_date - timedelta(days=1460)  # 4 years ago
        end_date = current_date - timedelta(days=30)      # 1 month ago
        launch_date = fake.date_between(start_date=start_date, end_date=end_date)
        
        products.append([product_id, product_name, category_id, launch_date, price])
    
    with open('apple_products.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['product_id', 'product_name', 'category_id', 'launch_date', 'price'])
        writer.writerows(products)
    
    print(f"Generated products data: {len(products)} records")
    return products

def generate_sales_data(products, num_records=20000):
    """Generate sales data with realistic patterns"""
    sales = []
    
    # Create date range for sales (last 2 years)
    current_date = datetime.now()
    end_date = current_date
    start_date = current_date - timedelta(days=730)  # 2 years ago
    
    # Convert string dates to datetime objects for products
    product_details = []
    for product in products:
        product_id, product_name, category_id, launch_date_str, price = product
        launch_date = datetime.strptime(str(launch_date_str), '%Y-%m-%d').date()
        product_details.append({
            'product_id': product_id,
            'category_id': category_id,
            'price': price,
            'launch_date': launch_date
        })
    
    for i in range(num_records):
        sale_id = f"SALE{str(i+1).zfill(6)}"
        sale_date = fake.date_between(start_date=start_date, end_date=end_date)
        store_id = random.choice(APPLE_STORES)[0]
        
        # Weight product selection towards newer products
        weights = []
        for product in product_details:
            days_since_launch = (end_date.date() - product['launch_date']).days
            weight = max(1, 365 - days_since_launch)  # Newer products have higher weight
            weights.append(weight)
        
        # Select product based on weights
        total_weight = sum(weights)
        rand_val = random.uniform(0, total_weight)
        cumulative_weight = 0
        selected_product = None
        
        for j, weight in enumerate(weights):
            cumulative_weight += weight
            if rand_val <= cumulative_weight:
                selected_product = product_details[j]
                break
        
        if selected_product is None:
            selected_product = random.choice(product_details)
        
        product_id = selected_product['product_id']
        
        # Generate quantity based on product type and price
        base_quantity = 1
        if selected_product['price'] < 100:
            base_quantity = random.randint(1, 5)
        elif selected_product['price'] < 500:
            base_quantity = random.randint(1, 3)
        
        # Seasonal adjustment
        sale_date_obj = datetime.strptime(str(sale_date), '%Y-%m-%d')
        month = sale_date_obj.month
        if month in [11, 12]:  # Holiday season
            base_quantity = min(base_quantity * 2, 10)
        elif month in [6, 7]:  # Back to school
            if selected_product['category_id'] in ['CAT002', 'CAT003']:  # iPad and Mac
                base_quantity = min(base_quantity * 3, 8)
        
        quantity = base_quantity
        
        sales.append([sale_id, sale_date, store_id, product_id, quantity])
    
    with open('apple_sales.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['sale_id', 'sale_date', 'store_id', 'product_id', 'quantity'])
        writer.writerows(sales)
    
    print(f"Generated sales data: {len(sales)} records")
    return sales

def generate_warranty_data(sales, num_records=15000):
    """Generate warranty claims data"""
    warranty = []
    
    # Sample sales for warranty claims
    if len(sales) > num_records:
        sales_with_warranty = random.sample(sales, num_records)
    else:
        sales_with_warranty = sales
    
    for i, sale in enumerate(sales_with_warranty):
        claim_id = f"CLAIM{str(i+1).zfill(5)}"
        sale_id, sale_date, store_id, product_id, quantity = sale
        
        # Warranty claim date is typically within 1 year of sale
        sale_date_obj = datetime.strptime(str(sale_date), '%Y-%m-%d')
        claim_start = sale_date_obj
        claim_end = min(datetime.now(), sale_date_obj + timedelta(days=365))
        
        claim_date = fake.date_between(start_date=claim_start, end_date=claim_end)
        
        repair_status = random.choices(
            ['Completed', 'In Progress', 'Pending Parts', 'Replaced'],
            weights=[0.6, 0.2, 0.15, 0.05],
            k=1
        )[0]
        
        warranty.append([claim_id, claim_date, sale_id, repair_status])
    
    with open('apple_warranty.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['claim_id', 'claim_date', 'sale_id', 'repair_status'])
        writer.writerows(warranty)
    
    print(f"Generated warranty data: {len(warranty)} records")

def main():
    """Main function to generate all data"""
    print("Generating Apple sales data...")
    
    # Generate data
    generate_category_data()
    generate_store_data()
    products = generate_products_data()
    sales = generate_sales_data(products)
    generate_warranty_data(sales)
    
    print("Data generation completed!")

if __name__ == "__main__":
    main()
