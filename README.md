# ecommerce-demo
E-Commerce application demo. The application enables users to buy products online.
## Use cases
- select product
- add product to shooping cart
- place order
- view order status
## Install
## Running the Application
Now that the REST API is up and running we can test it.
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
