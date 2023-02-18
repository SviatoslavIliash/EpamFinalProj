# About project
**"Bicycle Repair" web-application which allows bicycle enthusiasts to maintain, upgrade or repair their beloved bicycles by easy online record**

Application should provide:

- Storing client information, services and orders in database.
- Display list of services
- Client can choose service and make order.
- Sign up and login authentication for client or admin
- Display client's orders for user or admin
- Changing order`s status or delete order for admin
___
## Main page
Client can look at provided services

*main scenario:*

User choose "Log in" or "Sign up"

## Authentication
  
User select "Sign up" or "Log in".
1. For "Log in" user fill  "login", "password" and click submit;
- if entered data valid, then user redirects to "User page";
- if entered data is not valid, error messages occurs.
2. For "Sing up" user fill "login", "password", "email" and click submit;
- if entered data valid, then user redirects to "Log in" page;
- user will be added to database;
- if entered data is not valid, error messages occurs.

## User page

*main scenario:*

1. User look at list of services and choose one or several options;
2. User click "Submit" and order will be added to database;
3. User can see list of his orders in the bottom.

## Admin page

*main scenario:*

1. Admin can choose client
2. Admin can change order status option: "Pending", "In process" or "Done"
3. Admin can delete completed orders