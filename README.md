# Issue Tracker (https://quo-vadimus.herokuapp.com/)

Ticket reporting is a necessary step in the evolution of software and hardware products. Customers want to report issues that they have found or communicate ideas on how to make the product better. Developers and other stakeholders want to hear from customers or else the product becomes stale or frustrating forcing the user to move onto other products. The issue with ticket reporting is that it is often cumbersome and confusing.  

The Issue Tracker bridges the gap between customers and developers while moving towards the goal of making the product better. Customer will be able to communicate their ideas and issues in a streamlined ticket format that developers can distill to form solutions. The Issue Tracker provides a feature-rich UI that allows customers and developers to interact. Issue Tracker offers features such as realtime status updates, messaging and polling boards that allows customers' voices to be heard, and interactive work charts that provide transparency to the customers that tickets are actively being worked on.

## Backstory on Website

Quo Vadimus is a startup that has just released an application called "Destiny" to the world. "Destiny" provides an end-to-end solution for automating daily task management while employess can focus on development instead of management. Embeded in the website is an issue tracker that allows users of "Destiny" to interact with the development team at Quo Vadimus to log bugs and/or feature requests. Customers can voice their needs by voting on bugs to push them up the prioirty list or donating towards new feature requests since Quo Vadimus is still a startup. Quo Vadimus believes that gaining the trust of the customer is of the most importance. Thus, they have a work dashboard that is visible to the customer. The work dashboard provides the total work history of all the bugs and features along with other details such as ticket status and total work hours dedicated to the tickets.

## UX
 
Designing the UX for this project was a balancing act between the customers and the company (developers, managers, other stakeholders).

Customers typically don't want to spend a ton of time describing the issue/idea. They want transparency from the developer that the issue/idea is being worked on. They want to hear that the issue/idea has been fixed/implemented. On top of that, they wanted it done yesterday. 

Developers, on the other hand, want the moon when it comes to debugging issues or creating new features.  They want as much information as possible...Debug logs, screenshots, processes, environment information, etc.  They want to go to their computer, hit the ground running and attack the problem without any distractions like doing status updates or...*gasp* interacting with the customer.

Managers and other stakeholders want to see realtime status updates to see where the bottlenecks are located. They want to get important issues solved ASAP, apease the customers, and move on to the next item.

How do I make this easier on all parties? How can I create a UX that doesn't overwhelm the customer with endless questions while giving the developer enough information. Here are some user stories to demonstrate my point.

### USER STORIES:

#### As a customer:
- I want to create a ticket describing the issue/idea as quickly as possible so that I'm not stuck on a computer all day.
- I want to qickly know the status of my ticket so that I can respond accordingly.
- I want to comment on a ticket so that I can communicate with the developers.
- I want to communicate with other customers to see if they are encountering the same issue so that I can validate my findings.
- I want to know who is working on my ticket so that I can communicate with them directly.
- I want to vote on issues so that developers know which issues are a priority for me.

#### As a developer:
- I want to update tickets as quickly as possible so that I can get back to work on the issue/idea.
- I want to communicate with customers on tickets so that I can ask for more information when I need it.
- I want to see a high level view of MY tickets so that I can update them.
- I want hear as many details as possible to paint me a picture of the issue/idea so that I can come up with the right solution.

#### As a manager:
- I want automated work results so that I don't have to waste valuable time collecting information.
- I want to see which issues/ideas are the most popular among customers so that I have a priority list.
- I want to see a high level view of tickets being worked on so that I can communicate with my team effectively.

## Features

- Home Page: Fictional home page of company, Quo Vadimus, that is marketing their software product, "Destiny".
- About Us Page: Fictional employees of Quo Vadimus.
- FAQ Page: Fictional FAQ page to answer general questions about the company, specific questions about the product, and detailed questions about navigating features of the website.
- Contact Us Page: List of fictional email addresses and phone numbers for different departments in Quo Vadimus.
- Profile Page: Detailed look at the user currently logged in. Displays information such as last login date, credit cards associated with user, the ability to add a new credit card, delete a credit card, and set a credit card to default.	

- Bug Tracker Page: Table view of all bug tickets logged by customers against the "Destiny" product. Details include Title, Description, Reporter, Last Poster, Last Updated, Status, and Voting.
- Feature Tracker Page: Table view of all feature tickets logged by customers of what they would like to be included in the "Destiny" product. Details include Title, Description, Reporter, Last Poster, Last Updated, Status, and Donating.
- Ticket Details Page: Specific details about the ticket including description, creation date, owner, last post date, voting rank, donation status (Features ONLY), ticket status, ability to vote or donate, and comments associated with ticket.

- Bug Voting Results Page: Chart of all bug tickets in descending order according to vote count.
- Feature Voting Results Page: Chart of all feature tickets in descending order according to vote count. Also displays progress bars for each ticket of the amount donated and donation goal.
- Work Dashboard Page: Multiple charts displaying different type of ticket information such as:
	- Ticket History: Historical view of all tickets in the database
	- Ticket Type: Breakdown of how many tickets are bugs vs. features
	- Ticket Status: Breakdown of how many tickets are open, new, assigned, fixed, closed, verified, or in the retest status.
	- Ticket Hours Logged: Breakdown of how many hours have been dedicated to each ticket.
 
### Existing Features

User Type: Unregistered User
- Home: Allows user to view the "Home" page by having them click on [link](https://quo-vadimus.herokuapp.com/).
- About Us: Allows user to view the "About Us" page by having them click on [link](https://quo-vadimus.herokuapp.com/about/).
- FAQ: Allows user to view the "Frequently Asked Questions (FAQ)" page by having them click on [link](https://quo-vadimus.herokuapp.com/faq/).
- Contact Us: Allows user to view the "Contact Us" page by having them click on [link](https://quo-vadimus.herokuapp.com/contact/).
- Bug Tracker: Allows user to view the "Bug Tracker" page by having them click on [link](https://quo-vadimus.herokuapp.com/tickets/1/).
- Bug Ticket Details: Allows user to view the "Bug Ticket Details" page by having them click on a ticket name in [link](https://quo-vadimus.herokuapp.com/tickets/1/).
- Back to Bug Tracker button: Allows user to go back to the "Bug Tracker" page by clicking on the "Back to Bug Tracker" button.
- Feature Tracker: Allows user to view the "Feature Tracker" page by having them click on [link](https://quo-vadimus.herokuapp.com/tickets/2/).
- Feature Ticket Details: Allows user to view the "Ticket Details" page by having them click on a ticket name in [link](https://quo-vadimus.herokuapp.com/tickets/2/).
- Back to Feature Tracker button: Allows user to go back to the "Feature Tracker" page by clicking on the "Back to Feature Tracker" button.
- Search: Allows user to enter a string to filter results in either the Bug or Feature tracker by having them enter text in the "Search" field.
- Bug Voting Results: Allows user to view the "Bug Voting Results" page by having them click on [link](https://quo-vadimus.herokuapp.com/report/voting/1/).
	- Bug Ticket Details Shortcut: Allows user to view the "Bug Ticket Details" page by having them click on a ticket name in the chart.
- Feature Voting Results: Allows user to view the "Feature Voting Results" page by having them click on [link](https://quo-vadimus.herokuapp.com/report/voting/2/).
	- Feature Ticket Details Shortcut: Allows user to view the "Feature Ticket Details" page by having them click on a ticket name in the chart.
- Work Dashboard: Allows user to view the "Work Dashboard" page by having them click on [link](https://quo-vadimus.herokuapp.com/report/dashboard/).
- Registration: Allows anyone to create an account by having them fill out the registration [form](https://quo-vadimus.herokuapp.com/register/).

User Type: Registered User (General)
- Includes all features of "Unregistered User"
- Log In:  Allows user to log in to the website by having them fill out the login [form](https://quo-vadimus.herokuapp.com/login/).
- Create a New Bug Ticket button: Allows user to view the "New Bug Ticket" form by having them click on the "New Bug Ticket" button in the Bug Tracker [page](https://quo-vadimus.herokuapp.com/tickets/1/).
- Create a New Bug Ticket: Allows user to create a new bug ticket by having them fill out the Ticket Details [form](https://quo-vadimus.herokuapp.com/ticket/new/1/). 
- Up Vote a Bug button (Bug Tracker) : Allows user to upvote a bug by clicking on the "thumbs up" button on the specific bug in the Bug Tracker [page](https://quo-vadimus.herokuapp.com/tickets/1/).
- Up Vote a Bug button (Ticket Details): Allows user to upvote a bug by clicking on the "thumbs up" button in the "Ticket Details" page.
- Create a New Feature Ticket button: Allows user to view the "New Feature Ticket" form by having them click on the "New Feature Ticket" button in the Feature Tracker [page](https://quo-vadimus.herokuapp.com/tickets/2/).
	- Create a New Feature Ticket: Allows user to create a new feature ticket by having them fill out the Ticket Details [form](https://quo-vadimus.herokuapp.com/ticket/new/2/).  
- Donate button (Feature Tracker): Allows user to view the donation form by having them click on the "gift" button on the specific feature in the Feature Tracker [page](https://quo-vadimus.herokuapp.com/tickets/2/).
- Donate button (Ticket Details): Allows user to view the donation form by having them click on the "gift" button in the "Ticket Details" page.
	- Donate: Allows user to confirm donation amount by having them fill out the donation form.
- Add Post button: Allows user to view the "Add Post" form by clicking on the "Add Post" button.
	- Add Post: Allows user to add a post to the currently selected ticket by filling out the "Post Details" form.
- Edit Post button: Allows authorized user to view the "Edit Post" form by clicking on the edit button.
	- Edit Post: Allows authorized user to edit a post to the currently selected ticket by modifying the "Post Details" form.
- Delete Post button: Allows authorized user to view the "Delete Post" modal by clicking on the trash can button.
	- Delete Post Modal: Allows authorized user to delete a post from the currently selected ticket by clicking the "Confirm" button.		 
- Add Credit Card button: Allows user to view the "Add Credit Card" form by clicking on the "Add Credit Card" button.
	- Add Credit Card: Allows user to add a credit card to their profile by filling out the "Add Credit Card" form embedded in the profile [page](https://quo-vadimus.herokuapp.com/profile/).
- Set Default Credit Card button: Allows user to set a default credit card to be used for donations by click on the empty star button in the registered credit card row. 
- Delete Credit Card button: Allows user to view the delete credit card confirmation modal by click on the trash can button in the registered credit card row.
	- Delete Credit Card: Allows user to confirm the deletion of a credit card by clicking "Confirm" in the modal.
- Log Out: Allows user to log out of the website by having them click on the "Log Out" link in the user submenu of the navigation bar.

NOTE: An authorized used is either the owner of the original post or a user that is designated as staff or administrator.

User Type: Registered User (Staff or Administrator)
- Includes all features of "Registered User"
- Update (Bug or Feature) Ticket button: Allows user to view the "Update Ticket" form by having them click on the "Update Ticket" button in the Ticket details page.
- Update (Bug or Feature) Ticket: Allows user to update a ticket by having them modify the fields in the "Ticket Details" form.

## Technologies Used

- [JQuery](https://jquery.com)
    - The project uses **JQuery** to simplify DOM manipulation.
- [Django](https://www.djangoproject.com/)
	- The project uses **Django** for rapid Web development using [Python](https://www.python.org/).
- [Javascript](https://www.javascript.com/)
	- The project uses **Javascript** libraries for chart development and data manipulation.
- [Django REST Framework](https://www.django-rest-framework.org/)
	- The project uses **Django REST Framework** to access the database and serialize the data using JSON.
- [Django Choices](https://pypi.org/project/django-choices/)
	- The project uses **Django Choices** as a way of declaring choices on Django fields.
- [Django TinyMCE](https://pypi.org/project/django-tinymce/)
	- The project uses **Django TinyMCE** to create a form field using the TinyMCE editor.
- [Django Forms Bootstrap](https://pypi.org/project/django-forms-bootstrap/)
	- The project uses **Django Forms Bootstrap** to render Django forms using Bootstrap.
- [Stripe](https://stripe.com/)
	- The project uses **Stripe** to process payments (donations).
- [DotENV](https://pypi.org/project/python-dotenv/)
	- The project uses **DotENV** to manage environment variables in the project.
- [Whitenoise](https://pypi.org/project/whitenoise/)
	- The project uses **Whitenoise** to serve static files.
- [Bootstrap](https://getbootstrap.com/)
	- The project uses **Bootstrap** to create a responsive and mobile-first thinking website. 
- [Font Awesome](https://fontawesome.com/)
	- The project uses **Font Awesome** for the graphical icons.
- [Bootstrap Table](http://bootstrap-table.wenzhixin.net.cn/)
	- The project uses **Boostrap Table** to create interactive Bootstrap tables that can be sorted or filtered.
- [DC.js](https://dc-js.github.io/dc.js/)
- [D3.js](https://d3js.org/)
- [Crossfilter.js](http://square.github.io/crossfilter/)
	- The project uses these Javascript libraries to create charts using large datasets.
- [Keen Dashboards](https://keen.github.io/dashboards/)
	- The project uses **Keen Dashboards** to create responsive dashboards in Bootstrap. 
- [Google Fonts](https://fonts.google.com/)
	- The project uses **Google Fonts** for web-friendly readable fonts.
- [Popper.js](https://popper.js.org/)
	- The project uses the **Popper.js** Javascript library as a requirement for Bootstrap.

## Testing

Go to this [page](https://docs.google.com/spreadsheets/d/15andB1vSunuoaMmfTk3OKhxBeOaI7kUSEpR_Bol_C5Q/edit?usp=sharing) to see test cases.

## Deployment

The project is hosted on Heroku and is deployed through Github.

### Differences bewtween Development and Production Versions

|                                 | Development          | Production |
| ------------                    | -----------          | ---------- |
| Debug Mode                      | True                 | False      |
| Database                        | MySQL                | MySQL      |
| Database Version                | 5.7.21               | 5.7.23-log |
| Database Host                   | Local                | JawsDB     |
| Web Host                        | Local                | Heroku     |
| Site URL                        | localhost            | https://quo-vadimus.herokuapp.com/ |
| Config File (/root/settings/)   | dev.py               | staging.py |

| Environment Variables           | Locally in .env file   | Config vars in Heroku |
| ------------                    | -----------            | ---------- |
| Database                        | LOCALHOST_DATABASE_URL | JAWSDB_URL |
| Stripe Secret                   | STRIPE_SECRET          | STRIPE_SECRET |
| Stripe Publishable              | STRIPE_PUBLISHABLE     | STRIPE_PUBLISHABLE |


### Resources

- JawsDB MySQL
	- The project uses the JawsDB MySQL add-on to host the MySQL database.
	- NOTE: Needed to use JawsDB over ClearDB because I am using Django 2.1 which is only supported with MySQL 5.6+.

## Credits

Various details of this website uses companies and characters from some of my favorite shows and movies:
- Quo Vadimus is the name of the company the character Calvin Trager founded in the show, "[Sports Night](https://www.imdb.com/title/tt0165961/)".
- Pied Piper and Hooli are from the amazing HBO show, "[Silicon Valley](https://www.hbo.com/silicon-valley)". Check it out!
- Wayne Enterprises is from the [Batman](https://www.dccomics.com/characters/batman) and DC franchises.
- Stark Industries is from the [Iron Man](https://www.marvel.com/characters/iron-man-tony-stark) and Marvel franchises.
- Dunder Mifflin is the ficticious company from the NBC show, "[The Office](https://www.nbc.com/the-office)".
- Entertainment 720 is a hilariously failed company from the NBC show, "[Parks and Recreation](https://www.nbc.com/parks-and-recreation)".

### Content

### Media
The photos used in this site were obtained from:
- https://www.wallpaperup.com/
- https://www.icon100.com/
- https://www.pinterest.com/
- https://www.google.com/ (Image Search)

### Acknowledgements

- I received inspiration for this project from X