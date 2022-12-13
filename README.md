# [TallyBill](https://www.tallybill.online)


## Application Overview 

The application streamlines the process of splitting bills when a group of people go out to a restaurant or bar. It has a clean and simple design and uses visual colors to allow the users to split the bill quickly and easily among multiple people. It uses Veryfi OCR API to read the bill that the user scans with their mobile device, this enables the items to be entered into the database automatically. The user can enter items manually and edit items. 

It is a web application that has the look and feel of a native mobile app by using the JavaScript fetch API extensively with csrftoken to create a seamless experience for the user without reloading the page. I have incorporated Django forms, models, templates for unified development. The application uses the bootstrap library to ensure that it is mobile responsive.

##  What's contained in each file

### Files:
- Python
    - `tally/views.py` - Contains the view functions: 
        - index - Index page, upload scanned bill and add the line items.
        - login_view- Login into the application.
        - logout_view - Logout of the application.
        - register - Register a new user. 
        - settings - Change the logged in user's setting.  
        - password_update - Update the logged in user's password. 
        - bill_header - Create a bill header. 
        - bill_header_update - Update a bill header. 
        - bill_view - View the bill header. 
        - line_json - Fetch API, post a new item. 
        - bill_view_json - Fetch API, view the bill items and users. 
        - line_edit_json - Fetch API, edit or delete an item. 
        - bill_users_json - Fetch API, add a bill user or fetch all bill users.
        - user_edit_json - Fetch API, edit or delete bill user. 
        - add_line_user_json - Fetch API, add or remove bill user(s) from an item. 
        - bill_totals - Fetch API, get the bill totals and bill users totals.
        - my_bills - Show the logged in user's list of bills.
    - `tally/helpers.py` - Contains helper functions:
        - get_ip_currency - Call API to get the user's currency based on their IP
        - rev_sentence_word - Reverse sentence to right to left for languages such as Hebrew and Arabic 
        - veryfi - Call API to read scanned receipts.
    - `tally/url.py` - Application routing paths for views  
    - `tally/models.py` -Model Tables  
        - User - Inherits the  AbstractUser class and changes the attributes of fields. Changes the user's unique identifier from usrname to email. 
        - Bill_Header - Contains the Bill header data and a serialize function. 
        - Bill_User - Contains the bill user data and a serialize function. 
        - Bill_Lines - Contains the bill line items data and a serialize function.        
    - `tally/forms.py` - Model forms
        - CreateRegisterForm - Form for user registration, settings and password update.
        - BillForm - Form for a new bill or update bill header.
        - BillDetailForm - Form to add, edit or delete a line item.
        - BillUserForm - Form to add, edit or delete a bill user. 
    - `tally/templatetags/filters.py` - Custom tags  
        - label_with_classes - filter to add classes to Django templates form labels. 
    - `admin.py` - Register the models for the admin interface
- JavaScript
    - `tally/static/tally bill.js` - JavaScript for bill.html template -contains the functions:  
        - DOMContentLoaded - Load the bill items and users, add event listeners and create observers.
        - create_row- Create the bill item lines. 
        - get_bill_lines - Fetch the bill items and call the create_row function.
        - new_bill_line - Fetch Post a new bill item and call the create_row function.
        - line_edit - Fetch the item in the edit form.
        - line_update - Fetch Put the item to update it.
        - line_delete - Fetch Delete an item.
        - add_line_user - Fetch Post to add or remove a user from a line item and change the colors accordingly.
        - create_line_user_button- Create a bill user button on each line item.
        - get_bill_line_users - Fetch bill line item users, update the colors if the user was added to the item and call the create_line_user_button function.
        - create_user_button - Create the bill user button.
        - get_bill_users - Fetch the bill users and call the create_user_button function.
        - add_bill_users - Fetch Post to add a new bill user and call the the create_user_button and the create_line_user_button functions.
        - edit_bill_user - Fetch the bill user in the edit form.
        - update_bill_user - Fetch Put to update the bill user. 
        - delete_bill_user - Fetch Delete the bill user. 
        - get_bill_totals - Fetch the bill and user's totals.     
- CSS/SASS
    - tally/static/bootswatch/united directory - Theme for bootstrap.
    - tally/static/node_modules/bootstrap directory - bootstrap files.
    - tally/static/tally/bootstrap.sass -  Create bootstrap united themed CSS file.
    - tally/static/tally/bootstrap.css - Bootstrap 5 CSS.
    - tally/static/tally/styles.scss - Styles SASS.
    - tally/static/tally/styles.css - Styles CSS.
- Images
    - tally/static/tally/images directory - Contains images used in the application. 
    - tally/static/tally/favicon directory - Contains the favicon files.
- HTML Templates
    - tally/templates/tally/layout.html - Main nav bar and layout.
    - tally/templates/tally/index.html - Index home page and receipt scanner button.
    - tally/templates/tally/register.html - User registration.
    - tally/templates/tally/login.html - User login.
    - tally/templates/tally/bill.html - Create, edit and view bill.  Uses Django templates and forms.
- Media
    -media/documents directory - Temporarily stores the scanned receipts.

## How to run the application 
1. Clone the git repository <https://github.com/mimifishman/TallyBill>
1. Install project dependencies by running pip install -r requirements.txt.
2. Make and apply migrations by running python `manage.py` makemigrations and python `manage.py` migrate.
3. Create superuser for Django admin by running python `manage.py` createsuperuser.
4. Run the Django server using python `manage.py` runserver to enter the homepage of the web application.

## How to use the application
 <https://www.youtube.com/watch?v=HQybl9dGI7w>

1. **Register**
    - Register a new user
2. **Login**
    - User login 
3. **Scan Receipt Camera Button**
    - Click on the camera button to open the phone camera.
    - Take a picture of the receipt.
    - Wait for the receipt lines to load.
    - Fill out the bill header form.
    - Bill view will be shown.
4. **New Bill**
    - Only logged in users can create a new bill.
    - Enter a bill title, tip, discount and tax if applicable and submit the form.
    - Bill view will be shown.
5. **Bill View**
    - Logged in user will be added to the bill view.
    - Display the bill header details by clicking on the chevron double right.
    - Edit the bill header details by clicking on the Edit link. 
    - Share the bill by clicking on the Share icon. Users do not have to be logged in to view or modify a bill.
    - Clicking on "+ Add Item link"  will display a modal form to add an item. Fill out the form fields and click save. 
    - Clicking on the item pencil or trash can icons will allow the user to Edit or Delete the item.
    - Each time an item is added, edited or deleted the Total on the page will change. 
    - Clicking on the circular Add button will display a modal form to add a new person to the bill. The default tip will be the main bill tip but can be  modified for each person. Fill out the form field and click Save.
    - Each person will be added to each item line for selection. Click on the main people icon to the display the people for each line or click on the item people icon to only display the people for that specific item.
    - Click on the main person button to edit or delete a person. 
    - Click on the people who shared an item on each item line. When an item person is selected, the person's button will change to their assigned  color. Clicking on the person again will unselect the person and the button will revert to grey. 
    - Clicking on the item's All button will select all the people, clicking again will unselect all people. 
    - Clicking on the Total link will display the bill and user totals.
6. **Bill Totals View** 
    - Click on the details button to display the details of each person or bill totals.
    - Each item will show the people the item was split with.
    - Click the back arrow to continue to edit the bill. 
7. **Join Bill**
    - Click on the navigation link "Join Bill" and enter the bill number to join. Users does not have to be logged in to join a bill. 
8. **My Bills**  
    - Click on the navigation link "My Bills" to see all the bills that the logged in user created. Click on the bill to see the bill details and edit it.  User must be logged in to use this feature. 