# Issue Tracker (https://quo-vadimus.herokuapp.com/)

Ticket reporting is a necessary step in the evolution of software and hardware products. Customers want to report issues that they have found or communicate ideas on how to make the product better. Developers and other stakeholders want to hear from customers or else the product becomes stale or frustrating forcing the user to move onto other products. The issue with ticket reporting is that it is often cumbersome and confusing.  

The Issue Tracker (aka Quo Vadimus) provides a bridges the gap between customers and developers while moving towards the goal of making the product better. Customer will be able to communicate their ideas and issues in a streamlined ticket format that developers can distill to form solutions. Quo Vadimus provides a feature-rich UI that allows customers and developers to interact.

Talking points:
Message board
Realtime status
Voting and Results
Work Dashboard

have Quo Vadimus also provides transparency between the customer and the developeer by providing realtime status updates, poll 

## UX
 
Designing the UX for this project was a balancing act between the customers and the company (developers, managers, other stakeholders).

Customers typically don't want to spend a ton of time describing the issue/idea. They want transparency from the developer that the issue/idea is being worked on. They want to hear that the issue/idea has been fixed/implemented. On top of that, they wanted it done yesterday. 

Developers, on the other hand, want the moon when it comes to debugging issues or creating new features.  They want as much information as possible...Debug logs, screenshots, processes, environment information, etc.  They want to go to their computer, hit the ground running and attack the problem without any distractions like doing status updates or...*gasp* interacting with the customer.

Managers and other stakeholders want to see realtime status updates to see where the bottlenecks are located. They want to get important issues solved ASAP, apease the customers, and move on to the next item.

How do I make this easier on all parties? How can I create a UX that doesn't overwhelm the customer with endless questions while giving the developer enough information. Here are some user stories to demonstrate my point.

USER STORIES:

As a customer:
I want to create a ticket describing the issue/idea as quickly as possible so that I'm not stuck on a computer all day.
I want to qickly know the status of my ticket so that I can respond accordingly.
I want to comment on a ticket so that I can communicate with the developers.
I want to communicate with other customers to see if they are encountering the same issue so that I can validate my findings.
I want to know who is working on my ticket so that I can communicate with them directly.
I want to vote on issues so that developers know which issues are a priority for me.

As a developer:
I want to update tickets as quickly as possible so that I can get back to work on the issue/idea.
I want to communicate with customers on tickets so that I can ask for more information when I need it.
I want to see a high level view of MY tickets so that I can update them.
I want hear as many details as possible to paint me a picture of the issue/idea so that I can come up with the right solution.

As a manager:
I want automated work results so that I don't have to waste valuable time collecting information.
I want to see which issues/ideas are the most popular among customers so that I have a priority list.
I want to see a high level view of tickets being worked on so that I can communicate with my team effectively.


This section is also where you would share links to any wireframes, mockups, diagrams etc. that you created as part of the design process. These files should themselves either be included in the project itself (in an separate directory), or just hosted elsewhere online and can be in any format that is viewable inside the browser.

## Features

Home Page - Fictional home page of company, Quo Vadimus, that is marketing their software product, "Destiny".
About Us Page - Fictional employees of Quo Vadimus.
FAQ Page - Fictional FAQ page to answer general questions about the company, specific questions about the product, and detailed questions about navigating features of the website.
Contact Us Page - List of fictional email addresses and phone numbers for different departments in Quo Vadimus.
Profile Page - Detailed look at the user currently logged in. Displays information such as last login date, credit cards associated with user, the ability to add a new credit card, delete a credit card, and set a credit card to default.	

Bug Tracker Page - Table view of all bug tickets logged by customers against the "Destiny" product. Details include Title, Description, Reporter, Last Poster, Last Updated, Status, and Voting.
Feature Tracker Page - Table view of all feature tickets logged by customers of what they would like to be included in the "Destiny" product. Details include Title, Description, Reporter, Last Poster, Last Updated, Status, and Donating.
Ticket Details Page - Specific details about the ticket including description, creation date, owner, last post date, voting rank, donation status (Features ONLY), ticket status, ability to vote or donate, and comments associated with ticket.

Bug Voting Results Page - Chart of all bug tickets in descending order according to vote count.
Feature Voting Results Page - Chart of all feature tickets in descending order according to vote count. Also displays progress bars for each ticket of the amount donated and donation goal.
Work Dashboard Page - Multiple charts displaying different type of ticket information such as:
	Ticket History: Historical view of all tickets in the database
	Ticket Type: Breakdown of how many tickets are bugs vs. features
	Ticket Status: Breakdown of how many tickets are open, new, assigned, fixed, closed, verified, or in the retest status.
	Ticket Hours Logged: Breakdown of how many hours have been dedicated to each ticket.
 
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

For some/all of your features, you may choose to reference the specific project files that implement them, although this is entirely optional.

In addition, you may also use this section to discuss plans for additional features to be implemented in the future:

### Features Left to Implement
- Another feature idea

## Technologies Used

In this section, you should mention all of the languages, frameworks, libraries, and any other tools that you have used to construct this project. For each, provide its name, a link to its official site and a short sentence of why it was used.

- [JQuery](https://jquery.com)
    - The project uses **JQuery** to simplify DOM manipulation.
- [Django](https://www.djangoproject.com/)
- [Python](https://www.python.org/)
- [Javascript](https://www.javascript.com/)

- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Choices](https://pypi.org/project/django-choices/)
- [Django Tiny MCE](https://pypi.org/project/django-tinymce/)
- [Django Emoticons](https://pypi.org/project/django-emoticons/)
- [Django Forms Bootstrap](https://pypi.org/project/django-forms-bootstrap/)
- [Stripe](https://stripe.com/)
- [Dot ENV](https://pypi.org/project/python-dotenv/)
- [Whitenoise](https://pypi.org/project/whitenoise/)

- [Bootstrap](https://getbootstrap.com/)
- [Font Awesome](https://fontawesome.com/)
- [Bootstrap Table](http://bootstrap-table.wenzhixin.net.cn/)
- [DC.js](https://dc-js.github.io/dc.js/)
- [D3.js](https://d3js.org/)
- [Crossfilter.js](http://square.github.io/crossfilter/)
- [Keen Dashboards](https://keen.github.io/dashboards/)
- [Google Fonts](https://fonts.google.com/)
- [Popper.js](https://popper.js.org/)

## Testing

In this section, you need to convince the assessor that you have conducted enough testing to legitimately believe that the site works well. Essentially, in this part you will want to go over all of your user stories from the UX section and ensure that they all work as intended, with the project providing an easy and straightforward way for the users to achieve their goals.

Whenever it is feasible, prefer to automate your tests, and if you've done so, provide a brief explanation of your approach, link to the test file(s) and explain how to run them.

For any scenarios that have not been automated, test the user stories manually and provide as much detail as is relevant. A particularly useful form for describing your testing process is via scenarios, such as:

1. Contact form:
    1. Go to the "Contact Us" page
    2. Try to submit the empty form and verify that an error message about the required fields appears
    3. Try to submit the form with an invalid email address and verify that a relevant error message appears
    4. Try to submit the form with all inputs valid and verify that a success message appears.

In addition, you should mention in this section how your project looks and works on different browsers and screen sizes.

You should also mention in this section any interesting bugs or problems you discovered during your testing, even if you haven't addressed them yet.

If this section grows too long, you may want to split it off into a separate file and link to it from here.

## Deployment

This section should describe the process you went through to deploy the project to a hosting platform (e.g. GitHub Pages or Heroku).

In particular, you should provide all details of the differences between the deployed version and the development version, if any, including:
- Different values for environment variables (Heroku Config Vars)?
- Different configuration files?
- Separate git branch?

In addition, if it is not obvious, you should also describe how to run your code locally.


## Credits

### Content
- The text for section Y was copied from the [Wikipedia article Z](https://en.wikipedia.org/wiki/Z)

### Media
- The photos used in this site were obtained from ...

### Acknowledgements

- I received inspiration for this project from X