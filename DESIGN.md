# File structure
**templates**
Within the final folder there is a static folder, a templates folder, and a bunch of files. Within the templates folder are several html files, each holding a different website page's basic html structure.

**static folder**
Within the static folder is the styles.css file, which contains all of the css styling for the elements of the various html pages.

**application.py**
All of the pages are linked via the application.py folder, which uses a flask app structure to dynamically adjust what each of the different pages inside of the templates folder display.

**dbfunctions.py**
The dbfunctions.py  is a file full of functions that are called within the application.py folder with the purpose of making the application.py folder clutter-free.

**events.db**
This is the sqlite3 database that stores all of the data that we want.

# General structure
**General HTML CSS structure**
The structure of the entire site is based in the layout.html file, which contains the elements that are universal to all pages of the website. Specifically this includes the navigation bar and the footer. Both are inspired by bootstrap's existing designs and modified and given properties (like stickiness, color, size, position) that are specific to our project's unique needs.

The other pages are individualized using the block structure.

**helpers.py**
This is the helpers function file that contains the apology displayed in case of an error.

#def search_sports_events()
**overview**
The sports events search bar function takes in the user's search query as a string and returns a list.

It first declares and empty list of data, runs a sql command, and returns a list of json data that is then displayed on the page.

**connection**
First, an empty list of json data is declared, then a connection is created to the database and stored as a connection variable. Then, a cursor is created and stored as another variable called cur. Then the sql command is executed using cur.execute(sql_query_1).

After the desired data is recieved, the cursor is closed, the connection is committed, and then the connection is closed. This allows us to access the sql data.

**sql requests**
Essentially, the sql commands have to be dynamic and dependent on the search request. Thus, the way the sql command is structured is so:

first, a variable called sql_common_like_statement is set to equal the string "LIKE '%'" and concatenated with the input of the function (which is the searched string) and then concatenated with "%' '"

next, to a variable called sql_query_1 another string is assigned. The string "SELECT * FROM Sports WHERE Gender" is concatenated with the sql_common_like_statement. This is then concatenated with OR SPORTS WHERE (any of the other columns) + sql_common_like_statement.

**json data handling**
First, a list called json_data is initialized. Then, after the sql query is executed, the columns's names are retrieved via a for loop that accesses the description property of the cursor.

Then a variable called data is declared and initalized to the result of what the cursor fetches via cur.fetchall().

Afterwards, a for loop is created whereby the program goes row by row through the data (called data). Within the loop, each column name and row are zipped together using a zip function, which is then cast as a list, and appended to the json list.

**closing**
Afterwards, the cursor is closed, the data is committed (allowing us to access it), and the connection is closed.

#Home page search bar
The search bar on the home page applies the same logic as the search_sports_events bar, only it instead needs to search through multiple different tables with different types of fields and different amounts of fields.

**combining json lists**
the way the home search bar works is by getting the results of all the different search functions (sports, acapella, theater, comedy).

Since the product of these functions is a json list, home page search bar works by appending all of the other lists to the EventList.

#Register/LogIn
Logging in is a pre-requisite to adding events, allowing for a verification of who can add things to the database.

The register and login pages follow the same logic as for those pages in Finance.

**login**
In /login it clears the session so the site does not have any prior user info disrupting the new user’s info, then once you input your username and password, it checks to ensure that both a username and password were input using request.form.get. If they were not, it redirects to an apology and explanation of the error. It then checks if the the username is in the database using db.execute and a SQL select query and checks that the password hash matches (using check_password_hash). If they do not, it redirects to an apology. Once you are logged in, it remembers that you specifically are logged in using session, and redirects you to /add_event.

**register**
/register has the same setup, but also with a form for password confirmation. It ensures that inputs were made for all three forms using request.form.get then checks that the confirmation matches the first password, also using request.form.get. After that, using any(i.isdigit) and any(i.isalpha), it checks that the password includes at least one number and letter, and using len, checks that the password is at least 8 characters. After that, it uses db.execute and a SQL select query, to check that the username does not already exist. Once it is ensured that all the entered registration information is valid, it Inserts the username and a hash of the password into a registration table in the database using SQL. Also, it remembers which user registered and logged in using session. Lastly, it redirects to /add_event.

#Insert Events
When the user has logged in, inserts their event, and presses submit, the data is inserted into the database.

**sports events**
To standardize the way sports events are entered, the insert function enters in a unique query into the database that is different from what the user types in. For example, the user will type in gender, sport name, and opposing team and these three fields will be integrated in the add_events function to create one common event title in the format (Men's Hockey vs. Brown). The title after this information is integrated is what gets entered into the database.

This standardization makes it easier to display the information on the html page later, especially when we need to display acapella events (which don't have genders or sport names).

#Dates
The website gives users the option to filter events by “today” or “future.”

**display**
The dates dropdown menu, when clicked has 3 buttons: one called all that displays all events, one called today that displays events happening today, and one called future that displays future events.

**today**
If typesearch is current (meaning that “today” is clicked), it saves in the variable sql_query_1 a SQL query that queries the database in question for events where the date is the same as today, using the DATE() function to get the current date and = to check if it is the same as the date of each event in the database.

**later**
If typesearch is later (meaning that “future” is clicked), it saves in the variable sql_query_1 a SQL query that queries the database in question for events where the date is the same or after today, using the DATE() function and >=. The sequel query, which depends on whether today or future is clicked, is executed using cur.execute.

#Dynamic Display
Based on what a user searches, the results of their query are displayed dynamically.

**Display aesthetic**
The searched results are displayed in a card structure (from bootstrap) that is embedded within a table. Additionally, the elements are customized based on what we needed (image position, centering, font, font-size, etc.)

**dynamic elements**
The elements are uniquely and dynamically displayed by using a for loop in jinja that inserts things like links and event names, descriptions, etc into the card skeleton dynamically based on the search query.
