from django.shortcuts import render
import shopify
from .helpers import *
import datetime
from datetime import timedelta
import time

PRODUCT_MAP_JACKET = {"Blue Estate Herringbone Tweed": 'Blue Estate Herringbone Tweed Jacket',
					"Blue Overcheck Twill Tweed": 'Blue Overcheck Twill Tweed Jacket',
					"Brown Overcheck Twill Tweed": 'Brown Overcheck Twill Tweed Jacket',
					"Brown Prince of Wales Tweed": 'Brown Prince of Wales Tweed Jacket',
					"Brown Red Houndstooth Tweed": 'Brown Red Houndstooth Tweed Jacket',
					"Classic Brown Barleycorn Tweed": 'Classic Brown Barleycorn Tweed Jacket',
					"Classic Grey Barleycorn Tweed": 'Classic Grey Barleycorn Tweed Jacket',
					"Country Estate Herringbone Tweed": 'Country Estate Herringbone Tweed Jacket',
					"Dark Green Overcheck Twill Tweed": 'Dark Green Overcheck Twill Tweed Jacket',
					"Dark Grey Estate Herringbone Tweed": 'Dark Grey Estate Herringbone Tweed Jacket',
					"Grey Blue Prince of Wales Tweed": 'Grey Blue Prince of Wales Tweed Jacket',
					"Grey Prince of Wales Check Worsted Wool": 'Grey Prince of Wales Check Worsted Wool Jacket',
					"Navy Worsted Wool": 'Navy Worsted Wool Jacket',
					"Retro Brown Plaid Tweed": 'Retro Brown Plaid Tweed Jacket',
					"Traditional Brown Estate Herringbone Tweed": 'Traditional Brown Estate Herringbone Tweed Jacket',
					"Traditional Grey Estate Herringbone Tweed": 'Traditional Grey Estate Herringbone Tweed Jacket',}

PRODUCT_MAP_WAISTCOAT = {"Blue Estate Herringbone Tweed": 'Blue Estate Herringbone Tweed Waistcoat',
					"Blue Overcheck Twill Tweed": 'Blue Overcheck Twill Tweed Waistcoat',
					"Brown Overcheck Twill Tweed": 'Brown Overcheck Twill Tweed Waistcoat',
					"Brown Prince of Wales Tweed": 'Brown Prince of Wales Tweed Waistcoat',
					"Brown Red Houndstooth Tweed": 'Brown Red Houndstooth Tweed Waistcoat',
					"Classic Brown Barleycorn Tweed": 'Classic Brown Barleycorn Tweed Waistcoat',
					"Classic Grey Barleycorn Tweed": 'Classic Grey Barleycorn Tweed Waistcoat',
					"Country Estate Herringbone Tweed": 'Country Estate Herringbone Tweed Waistcoat',
					"Dark Green Overcheck Twill Tweed": 'Dark Green Overcheck Twill Tweed Waistcoat',
					"Dark Grey Estate Herringbone Tweed": 'Dark Grey Estate Herringbone Tweed Waistcoat',
					"Grey Blue Prince of Wales Tweed": 'Grey Blue Prince of Wales Tweed Waistcoat',
					"Grey Prince of Wales Check Worsted Wool": 'Grey Prince of Wales Check Worsted Wool Waistcoat',
					"Navy Worsted Wool": 'Navy Worsted Wool Waistcoat',
					"Retro Brown Plaid Tweed": 'Retro Brown Plaid Tweed Waistcoat',
					"Traditional Brown Estate Herringbone Tweed": 'Traditional Brown Estate Herringbone Tweed Waistcoat',
					"Traditional Grey Estate Herringbone Tweed": 'Traditional Grey Estate Herringbone Tweed Waistcoat',}

PRODUCT_MAP_TROUSER = {"Blue Estate Herringbone Tweed": 'Blue Estate Herringbone Tweed Trousers',
					"Blue Overcheck Twill Tweed": 'Blue Overcheck Twill Tweed Trousers',
					"Brown Overcheck Twill Tweed": 'Brown Overcheck Twill Tweed Trousers',
					"Brown Prince of Wales Tweed": 'Brown Prince of Wales Tweed Trousers',
					"Brown Red Houndstooth Tweed": 'Brown Red Houndstooth Tweed Trousers',
					"Classic Brown Barleycorn Tweed": 'Classic Brown Barleycorn Tweed Trousers',
					"Classic Grey Barleycorn Tweed": 'Classic Grey Barleycorn Tweed Trousers',
					"Country Estate Herringbone Tweed": 'Country Estate Herringbone Tweed Trousers',
					"Dark Green Overcheck Twill Tweed": 'Dark Green Overcheck Twill Tweed Trousers',
					"Dark Grey Estate Herringbone Tweed": 'Dark Grey Estate Herringbone Tweed Trousers',
					"Grey Blue Prince of Wales Tweed": 'Grey Blue Prince of Wales Tweed Trousers',
					"Grey Prince of Wales Check Worsted Wool": 'Grey Prince of Wales Check Worsted Wool Trousers',
					"Navy Worsted Wool": 'Navy Worsted Wool Trousers',
					"Retro Brown Plaid Tweed": 'Retro Brown Plaid Tweed Trousers',
					"Traditional Brown Estate Herringbone Tweed": 'Traditional Brown Estate Herringbone Tweed Trousers',
					"Traditional Grey Estate Herringbone Tweed": 'Traditional Grey Estate Herringbone Tweed Trousers',}

# Create your views here.
def index(request):
	
	shop = shopify.Shop.current()
	products = get_all_resources(shopify.Product)

	return render(request, 'index.html', {'products': products})


def view_product(request, pid):
	
	shop = shopify.Shop.current()
	product = shopify.Product.find(pid)

	return render(request, 'product.html', {'product': product})


def view_orders(request, oid):
	
	line_items = {}
	stock_status = {}
	d = 'no'
	jacket_size_in_stock = False
	jacket_length_in_stock = False
	waistcoat_size_in_stock = False
	waistcoat_length_in_stock = False
	trouser_size_in_stock = False
	trouser_length_in_stock = False
	trouser_fit_in_stock = False
	# Need to hold a variable for the actual order string for trousers (34 / Regular / Regular)
	orig_values = {}


	shop = shopify.Shop.current()
	order = shopify.Order.find(oid)
	products = get_all_resources(shopify.Product)

	for o in order.line_items:
		product_trousers = PRODUCT_MAP_TROUSER.get(o.title)
		product_waistcoat = PRODUCT_MAP_WAISTCOAT.get(o.title)
		product_jacket = PRODUCT_MAP_JACKET.get(o.title)
		for k in o.properties:
			is_in_stock = is_it_in_stock(order, products, k.name, k.value)
			line_items[k.name] = is_in_stock
			orig_values[k.name] = k.value

	keys, values = line_items.keys(), line_items.values()

	# Here we set the original order values into 3 strings, concatenate them further down to make string to compare against later with stock items
	n1 = orig_values['Trouser Size']
	n2 = orig_values['Trouser Length (inseam)']
	n3 = orig_values['Trouser Fit']
	# Same for Jackets
	j1 = orig_values['Jacket Size']
	j2 = orig_values['Jacket Length']
	j3 = ''
	j4 = ''
	# Same for Waistcoats
	w1 = orig_values['Waistcoat Size']
	w2 = orig_values['Waistcoat Length']
	w3 = ''
	w4 = ''
	# Now split each so that we don't have (33") or Fit in the strings to check
	s1, s2 = n2.split()
	t1, t2 = n3.split()
	x1 = ''
	x2 = ''
	x3 = ''

	# Here we are looping through each line item (eg. Jacket Size, Waistcoat Size, Trouser Size. X = Jacket Size, Y = 42)
	for x, y in line_items.items():
		# Need to unpack dictionary sent to us from Shopify
		for line_name, line_value in y.items():
			# Here we have problem. Eg. any size 34, any regular fit, and any regular length in stock would cause 34 / Regular / Regular to show in stock when it actually isnt.
			# Need to compare what is sent back to us by the is_it_in_stock() method with the original order values. 
			# We do this by assigning an empty string to the line_value and then create our own string to form the variant title required
			if line_name == 'Jacket Size' and line_value == j1:
				j3 = line_value
			if line_name == 'Jacket Length' and line_value == j2:
				j4 = line_value
			if line_name == 'Waistcoat Size' and line_value == w1:
				w3 = line_value
			if line_name == 'Waistcoat Length' and line_value == w2:
				w4 = line_value
			if line_name == 'Trouser Size' and line_value == n1:
				x1 = line_value
			if line_name == 'Trouser Length' and line_value == s1:
				x2 = line_value
			if line_name == 'Trouser Fit' and line_value == t1:
				x3 = line_value

	# String of original order
	orig_t = n1 + " / " + s1 + " / " + t1
	# String of given values from is_it_in_stock()
	jacket_string = j1 + " / " + j2
	waistcoat_string = w1 + " / " + w2
	trouser_string = x1 + " / " + x2 + " / " + x3


	# JACKET LOGIC
	# Now we need to check that jacket_string is equal to a variant title
	for x in products:
		# But only if the title of the product is equal to the jacket we are looking for
		if x.title == product_jacket:
			for y in x.variants:
				# Continue only when the variant title matches our created jacket string from is_it_in_stock()
				if y.title == jacket_string:
					if product_jacket == x.title:
						if y.inventory_quantity > 0:
							jacket_size_in_stock = True
							jacket_length_in_stock = True
	# WAISTCOAT LOGIC
	for x in products:
		if x.title == product_waistcoat:
			for y in x.variants:
				if y.title == waistcoat_string:
					if product_waistcoat == x.title:
						if y.inventory_quantity > 0:
							waistcoat_length_in_stock = True
							waistcoat_size_in_stock = True


	# TROUSER LOGIC
	# Now need to check that x1, x2, x3 is equal to a variant title, then check it has stock.
	for x in products:
		# But ONLY if this product title is equal to the lookup of the original orders product name as defined in PRODUCT_MAP_X
		if x.title == product_trousers:
			for y in x.variants:
				if y.title == trouser_string:
					# Now we need to make sure the variant we're looking up is the same as the original order product
					if product_trousers == x.title:
						if y.inventory_quantity > 0:
							trouser_size_in_stock = True
							trouser_length_in_stock = True
							trouser_fit_in_stock = True


	# stock_status[] is sent to the web page. Now to send it value if in stock or not based on above logic.
	if jacket_size_in_stock and jacket_length_in_stock:
		stock_status['Jacket'] = 'In Stock'
	else:
		stock_status['Jacket'] = 'Not In Stock'

	if waistcoat_size_in_stock and waistcoat_length_in_stock:
		stock_status['Waistcoat'] = 'In Stock'
	else:
		stock_status['Waistcoat'] = 'Not In Stock'

	if trouser_size_in_stock and trouser_fit_in_stock and trouser_length_in_stock:
		stock_status['Trousers'] = 'In Stock'
	else:
		stock_status['Trousers'] = 'Not In Stock'


					

	return render(request, 'orders.html', {'order': order, 'line_items': line_items, 'is_in_stock': is_in_stock, 'd': d, 'keys': keys, 'values': values, 
											'jacket_size_in_stock': jacket_size_in_stock, 'jacket_length_in_stock': jacket_length_in_stock, 'stock_status': stock_status, 
											'n1': n1, 'n2': n2, 'n3': n3, 'orig_t': orig_t,})


def is_it_in_stock(iorder, products, name, value):
	# first set shopify shop and get the order id
	shop = shopify.Shop.current()
	order = iorder
	jacket_size = ''
	jacket_length = ''
	in_stock = False
	results = {}



	# IDEAS FOR SOLUTION
	# 1. Pass the "products" in as a variable to make more efficient
	# 2. Get all variable as below (ie. Jacket Length, Size etc.)
	# 3. This will make the dict appear on page as {"Jacket/Waistcoat": "48, True"} if in stock and "48, False" if not in stock
	# 4. On the web browser, or maybe in the view. Compare that Jacket Length & Jacket Size to both equal True, then return a variable which means the Jacket is in stock or not.



	# check to see if the line property is Jacket Size
	if name == 'Jacket Size':
		# loop through each product until we find the product type we want
		for p in products:
			if p.product_type == 'Clearance - Jacket':
				# now we loop through each of the products variants
				for v in p.variants:
					 # Now get the first 2 chars of the jacket size (ie. 38)
					jacket_size = str(v.title[0:2])
					# if this value equals our value passed through the order then assign it to required size variable
					if jacket_size == value:
						if v.inventory_quantity > 0:
							results['Jacket Size'] = jacket_size


	# check to see if the line property is Jacket Length
	if name == 'Jacket Length':
		# loop through each product until we find the product type we want
		for j in products:
			if j.product_type == 'Clearance - Jacket':
				# now we loop through each of the products variants and set jacket_length equal to the variant title (eg. 36 / Long)
				for l in j.variants:
					# split the variants title (36 / Short to '36', '/', 'Short' and assign the last to jacket_length)
					title = l.title
					# Make sure we are not checking the bundle variants
					if "Bundle" not in title: 
						w1, w2, jacket_length = title.split()
						# check if this value equals our value passed through the order. (ie. Jacket Size: 40 on order, is this equal to the variant title. If Yes, we have the right one to check stock)
						if jacket_length == value:
							if l.inventory_quantity > 0:
								results['Jacket Length'] = jacket_length
					
	# check to see if the line property is Jacket Size
	if name == 'Waistcoat Size':
		# loop through each product until we find the product type we want
		for p in products:
			if p.product_type == 'Clearance - Waistcoat':
				# now we loop through each of the products variants
				for v in p.variants:
					 # Now get the first 2 chars of the jacket size (ie. 38)
					waistcoat_size = str(v.title[0:2])
					# if this value equals our value passed through the order then assign it to required size variable
					if waistcoat_size == value:
						if v.inventory_quantity > 0:
							results['Waistcoat Size'] = waistcoat_size

					
	# check to see if the line property is Jacket Length
	if name == 'Waistcoat Length':
		# loop through each product until we find the product type we want
		for j in products:
			if j.product_type == 'Clearance - Waistcoat':
				# now we loop through each of the products variants and set jacket_length equal to the variant title (eg. 36 / Long)
				for l in j.variants:
					# split the variants title (36 / Short to '36', '/', 'Short' and assign the last to jacket_length)
					title = l.title
					# Make sure we are not checking the bundle variants
					if "Bundle" not in title:
						w1, w2, waistcoat_length = title.split()
						# check if this value equals our value passed through the order. (ie. Jacket Size: 40 on order, is this equal to the variant title. If Yes, we have the right one to check stock)
						if waistcoat_length == value:
							if l.inventory_quantity > 0:
								results['Waistcoat Length'] = waistcoat_length
		

	# check to see if the line property is Jacket Size
	if name == 'Trouser Size':
		# loop through each product until we find the product type we want
		for p in products:
			if p.product_type == 'Clearance - Trousers':
				# now we loop through each of the products variants
				for v in p.variants:
					 # Now get the first 2 chars of the jacket size (ie. 38)
					trouser_size = str(v.title[0:2])
					# if this value equals our value passed through the order then assign it to required size variable
					if trouser_size == value:
						if v.inventory_quantity > 0:
							results['Trouser Size'] = value
					
					
	# check to see if the line property is Jacket Length
	if name == 'Trouser Length (inseam)':
		# loop through each product until we find the product type we want
		for j in products:
			if j.product_type == 'Clearance - Trousers':
				# now we loop through each of the products variants and set jacket_length equal to the variant title (eg. 36 / Long)
				for l in j.variants:
					# split the variants title (36 / Short to '36', '/', 'Short' and assign the last to jacket_length)
					title = l.title
					# Make sure we are not checking the bundle variants
					if "Bundle" not in title:
						w1, w2, w3, w4, w5 = title.split()
						n1, n2 = value.split()
						# check if this value equals our value passed through the order. (ie. Jacket Size: 40 on order, is this equal to the variant title. If Yes, we have the right one to check stock)
						if w3 == n1:
							if l.inventory_quantity > 0:
								results['Trouser Length'] = n1

	# check to see if the line property is Jacket Length
	if name == 'Trouser Fit':
		# loop through each product until we find the product type we want
		for j in products:
			if j.product_type == 'Clearance - Trousers':
				# now we loop through each of the products variants and set jacket_length equal to the variant title (eg. 36 / Long)
				for l in j.variants:
					# split the variants title (36 / Short to '36', '/', 'Short' and assign the last to jacket_length)
					title = l.title
					# Make sure we are not checking the bundle variants
					if "Bundle" not in title:
						w1, w2, w3, w4, w5 = title.split()
						n1, n2 = value.split()
						# check if this value equals our value passed through the order. (ie. Jacket Size: 40 on order, is this equal to the variant title. If Yes, we have the right one to check stock)
						if w5 == n1:
							if l.inventory_quantity > 0:
								results['Trouser Fit'] = n1



	return results
	



def view_todays_orders(request):
	xlist = {}
	shop = shopify.Shop.current()
	date = datetime.datetime.now() - datetime.timedelta(days=3)
	orders = shopify.Order.find(limit=250, created_at_min=date)
	products = get_all_resources(shopify.Product)
	for o in orders:
		a = check_stock(shop, o, products)
		xlist[o.name] = a
		time.sleep(1)
	return render(request, 'view_todays_orders.html', {'orders': orders, 'date': date, 'a': a, 'xlist': xlist})



def check_stock(shop, order, products):
	line_items = {}
	stock_status = {}
	d = 'no'
	jacket_size_in_stock = False
	jacket_length_in_stock = False
	waistcoat_size_in_stock = False
	waistcoat_length_in_stock = False
	trouser_size_in_stock = False
	trouser_length_in_stock = False
	trouser_fit_in_stock = False
	# Need to hold a variable for the actual order string for trousers (34 / Regular / Regular)
	orig_values = {}

	for o in order.line_items:
		product_trousers = PRODUCT_MAP_TROUSER.get(o.title)
		product_waistcoat = PRODUCT_MAP_WAISTCOAT.get(o.title)
		product_jacket = PRODUCT_MAP_JACKET.get(o.title)
		for k in o.properties:
			if k.value == 'Custom Measurements':
				return 'Custom Measurements Order'
			else:
				is_in_stock = is_it_in_stock(order, products, k.name, k.value)
				line_items[k.name] = is_in_stock
				orig_values[k.name] = k.value

	# Here we set the original order values into 3 strings, concatenate them further down to make string to compare against later with stock items
	try:
		n1 = orig_values['Trouser Size']
		n2 = orig_values['Trouser Length (inseam)']
		n3 = orig_values['Trouser Fit']
		# Same for Jackets
		j1 = orig_values['Jacket Size']
		j2 = orig_values['Jacket Length']
		j3 = ''
		j4 = ''
		# Same for Waistcoats
		w1 = orig_values['Waistcoat Size']
		w2 = orig_values['Waistcoat Length']
		w3 = ''
		w4 = ''
	except KeyError:
		return 'Custom Measurements Order'
	# Now split each so that we don't have (33") or Fit in the strings to check
	s1, s2 = n2.split()
	t1, t2 = n3.split()
	x1 = ''
	x2 = ''
	x3 = ''

	# Here we are looping through each line item (eg. Jacket Size, Waistcoat Size, Trouser Size. X = Jacket Size, Y = 42)
	for x, y in line_items.items():
		# Need to unpack dictionary sent to us from Shopify
		for line_name, line_value in y.items():
			# Here we have problem. Eg. any size 34, any regular fit, and any regular length in stock would cause 34 / Regular / Regular to show in stock when it actually isnt.
			# Need to compare what is sent back to us by the is_it_in_stock() method with the original order values. 
			# We do this by assigning an empty string to the line_value and then create our own string to form the variant title required
			if line_name == 'Jacket Size' and line_value == j1:
				j3 = line_value
			if line_name == 'Jacket Length' and line_value == j2:
				j4 = line_value
			if line_name == 'Waistcoat Size' and line_value == w1:
				w3 = line_value
			if line_name == 'Waistcoat Length' and line_value == w2:
				w4 = line_value
			if line_name == 'Trouser Size' and line_value == n1:
				x1 = line_value
			if line_name == 'Trouser Length' and line_value == s1:
				x2 = line_value
			if line_name == 'Trouser Fit' and line_value == t1:
				x3 = line_value

	# String of original order
	orig_t = n1 + " / " + s1 + " / " + t1
	# String of given values from is_it_in_stock()
	jacket_string = j1 + " / " + j2
	waistcoat_string = w1 + " / " + w2
	trouser_string = x1 + " / " + x2 + " / " + x3


	# JACKET LOGIC
	# Now we need to check that jacket_string is equal to a variant title
	for x in products:
		# But only if the title of the product is equal to the jacket we are looking for
		if x.title == product_jacket:
			for y in x.variants:
				# Continue only when the variant title matches our created jacket string from is_it_in_stock()
				if y.title == jacket_string:
					if product_jacket == x.title:
						if y.inventory_quantity > 0:
							jacket_size_in_stock = True
							jacket_length_in_stock = True
	# WAISTCOAT LOGIC
	for x in products:
		if x.title == product_waistcoat:
			for y in x.variants:
				if y.title == waistcoat_string:
					if product_waistcoat == x.title:
						if y.inventory_quantity > 0:
							waistcoat_length_in_stock = True
							waistcoat_size_in_stock = True


	# TROUSER LOGIC
	# Now need to check that x1, x2, x3 is equal to a variant title, then check it has stock.
	for x in products:
		# But ONLY if this product title is equal to the lookup of the original orders product name as defined in PRODUCT_MAP_X
		if x.title == product_trousers:
			for y in x.variants:
				if y.title == trouser_string:
					# Now we need to make sure the variant we're looking up is the same as the original order product
					if product_trousers == x.title:
						if y.inventory_quantity > 0:
							trouser_size_in_stock = True
							trouser_length_in_stock = True
							trouser_fit_in_stock = True


	# stock_status[] is sent to the web page. Now to send it value if in stock or not based on above logic.
	if jacket_size_in_stock and jacket_length_in_stock:
		stock_status['Jacket'] = 'In Stock'
	else:
		stock_status['Jacket'] = 'Not In Stock'

	if waistcoat_size_in_stock and waistcoat_length_in_stock:
		stock_status['Waistcoat'] = 'In Stock'
	else:
		stock_status['Waistcoat'] = 'Not In Stock'

	if trouser_size_in_stock and trouser_fit_in_stock and trouser_length_in_stock:
		stock_status['Trousers'] = 'In Stock'
	else:
		stock_status['Trousers'] = 'Not In Stock'

	return stock_status