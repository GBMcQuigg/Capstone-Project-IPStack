API = https://ipstack.com/

My Site: IP Tracker, https://gbm-ip-tracker.herokuapp.com/

  My website is designed to take in an IPv4 or IPv6 address and return the City, State, and Country of the IP Address. 

  The features I implemented were User authentication, flash messages for better user experience, a simple and clean rerouting system, easy site navigation, and a straight forward response/result system to return the exact data a user is looking for. 

   The user flow for the website starts with a 'Login' form and a message that informs the user they must be logged in or create an account to proceed to the main site. If the user already has an account, they will be stored in the session unless they choose to logout during their previous session. If the user does not have an account yet, there is a straight forward prompt underneath the "Log in" button with a link that redirects to the "Register" page. The user also has the option to click "Sign Up" in the top right corner of the nav bar. 

  Once the user is logged in, they are greeted with a "Welcome" message and redirected to the home page of the site. Here is where the user will see the "Search" form that allows them to input any IPv4 or IPv6 into the search bar and return with the Cityh, State and Country of this input IP Address. Once an IP Address is input and the user clicks the "Search" button next to the input, they will be redirected to a page that clearly lists the information they are looking for!
  
  Underneath the IP Address information, there is a home button to get back to the "Search" input, where the user can go through the whole process again and again!
  
  ***This API is a free trial API, meaning once the maximum number of requests are reached per month, the user will not be able to search anymore until the following          month!***
