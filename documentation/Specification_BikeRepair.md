# About project
**Bicycle Repair Web Service allows bike enthusiasts to service, upgrade or repair their vehicles with a simple online application**

Application provides:

- storing clients' information, services and orders in database;
- displaying the list of services;
- choice of services and ability to make orders;
- sign up and login authentication for clients and admin;
- displaying clients' orders for users and admin;
- changing order statuses or deleting orders by admin.
___
## Main page
Client can look at provided services

![Home](../bikerepair/static/images/HomePage.png "Pic.1 Home page")
*Pic.1 Home page*

*main scenario:*

User chooses "Log in" or "Sign up"

## Authentication
  
User selects "Sign up" or "Log in".

![Sign up](../bikerepair/static/images/SignUp.png "Pic.2 Sign up page")
*Pic.2 Sign up page*

![Log in]( ../bikerepair/static/images/LogIn.png "Pic.3 Log in page")
*Pic.3 Log in page*

*main scenario:*

1. For "Log in" user fills  "login", "password" and clicks submit;
- if entered data is valid, then user is redirected to "User page";
- if entered data is not valid, error message occurs.
2. For "Sign up" user fills "login", "password", "email" and clicks submit;
- if entered data is valid, then user is redirected to "Log in" page;
- user is added to database;
- if entered data is not valid, error message occurs.

## User page

![User page]( ../bikerepair/static/images/AccountPage.png "Pic.4 User page")
*Pic.4 User page*

*main scenario:*

1. User looks at the list of services and chooses one or several options;
2. User clicks "Submit", and the order will be added to the database;
3. User can see the list of his orders in the bottom.

## Admin page

![Admin](../bikerepair/static/images/AminPage.png "Pic.5 Admin page")
*Pic.5 Admin page*

*main scenario:*

1. Admin can select the client, which made an order; 
2. Admin can select the order status option: "Pending", "In process" or "Done";
3. Admin can delete completed orders;
4. All changes commits by pushing "confirm".
5. Admin can find orders by the date, after that choose users and browse order information. 