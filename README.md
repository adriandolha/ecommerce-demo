# ecommerce-demo
E-Commerce application demo. The application enables users to buy products online.
## Use cases
- select product
- add product to shooping cart
- place order
- view order status
## Install
The application is deployed using terraform. It was tested on Ubuntu 18.4
Run the following command inside terraform folders:
```
./deploy.sh apply master dev
```
## Running the Application
Now that the REST API is up and running we can test it.
### Get Products
GET /products
Response:
```
[
  {
    "product_id": "67689cbd-f560-4556-bf69-f630d58d00b1",
    "name": "Headset",
    "category": "Electronics",
    "price": 160
  },
  {
    "product_id": "9794751c-01c5-49ce-9562-85a0e051a768",
    "name": "Laptop",
    "category": "Computers",
    "price": 2000
  }
]
```
### Add Product to Shopping Cart
POST /shoppingcarts
```
{
	"user_id": "1",
	"items": [{
		"product_id": "67689cbd-f560-4556-bf69-f630d58d00b1",
		"name": "Headset",
		"category": "Electronics",
		"price": 160
	}]
}
```

### Place Order
POST /orders
```
{
	"user_id": "1",
	"items": [{
		"product_id": "67689cbd-f560-4556-bf69-f630d58d00b1",
		"name": "Headset",
		"category": "Electronics",
		"count": 2,
		"price": 160
	}]
}
```
Response:
```
{
  "order_id": "32a7b899-0468-450a-8ee3-7772ac222095",
  "user_id": "1",
  "items": [
    {
      "product_id": "67689cbd-f560-4556-bf69-f630d58d00b1",
      "name": "Headset",
      "category": "Electronics",
      "count": 2,
      "price": 160,
      "total": 320
    }
  ],
  "status": "CREATED",
  "total": 320
}
```
Notice the order status is **CREATED**.

### View Orders
Once the order is created, dynamodb streams trigger the order update lambda function which updates the status to **COMPLETED**.
GET /orders
