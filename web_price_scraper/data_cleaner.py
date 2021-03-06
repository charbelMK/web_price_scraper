import json


final_products = []
production = []

def jumia_clean():
    # Open file with jumia products
    with open('./jumia.json') as jumia_json:
        data = json.load(jumia_json)

        # Data cleaning loop
        for item in data:
            # Drop null entries
            if item == {}:
                pass
            else:
                product_name = item['name']
                price = item['price']
                image_url = item['img_link']
                product_url = item['product_link']
                vendor = 'ea24722d-4aca-4ea3-987e-71d8d6fa239c' # Jumia Vendor id
                categories = list(item['category'].split('/'))

                # Product Definition / Dictionary
                jumia_products = {
                    'name': product_name,
                    'price': price,
                    'images': image_url,
                    'product_url': product_url,
                    'vendor': vendor,
                    'category': categories
                }

                final_products.append(jumia_products)
        


def shopit_clean():
    # Open shopit.json
    with open('./shopit.json') as shopit_json:
        data = json.load(shopit_json)

        for item in data:
            # Drop null entries
            if item == {'name': None, 'price': None, 'product_link': None, 'img_link': None}:
                pass
            else:
                product_name = item['name']
                price = item['price']
                image_url = item['img_link']
                product_url = item['product_link']
                vendor = '2d5bee0c-c23c-4459-af27-9f5573dc5bbf'# Shopit Vendor id

                # Product Definition / Dictionary
                shopit_products = {
                    'name': product_name,
                    'price': price,
                    'images': image_url,
                    'product_url': product_url,
                    'vendor': vendor
                }

                final_products.append(shopit_products)


def kilimall_clean():
    with open('./kilimall.json') as kilimall_json:
        data = json.load(kilimall_json)

        for item in data:
            url = 'https://www.kilimall.co.ke/new/goods/'
            product_name = item['name']
            price = item['price']
            image_url = item['images']['ORIGIN']
            vendor = '29179fc6-5e74-4d70-8b77-ef2594c93ddd' # Kilimall Vendor id
            product_url = [str(item['goods_id'])] + list(str(item['name']).split())

            # Product Definition / Dictionary
            kilimall_products = {
                'name': product_name,
                'price': price,
                'images': image_url,
                'product_url': url + '-'.join(product_url),
                'vendor': vendor
            }

            final_products.append(kilimall_products)

jumia_clean()
shopit_clean()
kilimall_clean()

# Data Preparation
def data_prep(final_products):
    for idx, item in enumerate(final_products):
        production_dict = {
            '_id' : str(idx),
            '_type' : 'product',
            'title' : item['name'],
            'defaultProductVariant' : {
                '_type' : 'productVariant',
                'price' : item['price'],
                'image' : item['images'],
               
            },
            'product_url' : item['product_url'],
            'vendor' : {
            	'_type': 'reference',
            	'_ref' : item['vendor'],
            },

        }
        
        production.append(production_dict)


data_prep(final_products)

# Convertion to NDJson
with open('./production_data.ndjson', 'w') as f:
    # Writing items to a ndjson file
    for item in production:
        json.dump(item, f)
        f.write('\n')     
