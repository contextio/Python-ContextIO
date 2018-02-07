Context.IO API Python Library
==================================

This is the python client library the Context.IO API (Lite and v2.0)!

Supports Python 2.7 (2.7.9 and up) and 3.

### NOTICE
The 2.0 version of the API will be partially deprecated starting on June 15th, 2018, and will be completely deprecated on December 15th, 2018.

[READ MORE HERE](https://blog.context.io/important-announcement-deprecation-of-2-0-api-8f73488a8c0e)

##Dependencies
If you plan on contributing to this project you will want to clone this repo and then use `pip` to install the dependencies.

    pip install -r requirements.txt
    pip install -r dev-requirements.txt


This library relies on the following projects:

- RAUTH - If you do not have that, snag it with
```$ pip install rauth```
or
```$ easy_install rauth```
, or “Use the [Source](https://github.com/litl/rauth), Luke”

- REQUESTS - rauth is built on top of the requests module
```$ pip install requests```
or
```$ easy_install requests```
or [Source](https://github.com/kennethreitz/requests)

- SIX - six is a python compatability library for having python2 and python3 in a common codebase
```$ pip install six```
or
```$ easy_install six```
or [Source](https://bitbucket.org/gutworth/six)

##Installation
You can use pip to install the latest release (**recommended**):

    pip install contextio

Check out / download the module from git, change directory to the folder with setup.py and run:

    python setup.py install

**NOTE:** To install from source you may need to use *_sudo_*

##Usage
You first need to instantiate the main ContextIO object with your API credentials:

	import contextio as c

    CONSUMER_KEY = 'YOUR_API_KEY'
    CONSUMER_SECRET = 'YOUR_API_SECRET'
    API_VERSION = 'SOME_VERSION' # "lite" or "2.0"

    context_io = c.ContextIO(
      consumer_key=CONSUMER_KEY,
      consumer_secret=CONSUMER_SECRET,
      api_version=API_VERSION
    )

Modifying the `api_version` will give you access the methods associated with the different versions of the ContextIO API.  **By default the `ContextIO` factory returns the 2.0 API interface**

The ContextIO class can optionally accept a debug keyword parameter that prints or logs more info about the request and response.

The module is fully docstringed out, so feel free to jump into the python interpreter and help(foo) on stuff. Explore the resource classes and methods!

Here's how you can query the API for an account:

    accounts = context_io.get_accounts(email='johndoe@gmail.com')
    # since we return a list, let's be sure we have a result
    if accounts:
        account = accounts[0]

The Account class has methods to represent all the kinds of requests you can make under that resource.

If you store account ids, message ids, file ids, or anything else like that on your server, you can instantiate these objects without touching the API, for increased speed. Here's an example of how you do that.

	params = {
		'id': 'ACCOUNT_ID_HERE'
	}
	account = c.Account(context_io, params)

`account` will be an empty object, but you need to pass in the "id" since that's used to form the URL for API endpoints for the account resource. If you want to query the API and populate that account object, you can simply perform:

	account.get()

You can use this same technique to populate sub-resource objects too.

	params = {
		'message_id': 'MESSAGE_ID_HERE'
	}
	message = c.Message(account, params)
	# populate the message object with data from the API
	message.get()

Notice how the Message class needs an Account object as a parent? That's because the library uses an object's ancestors to build the URL.

##Tests

There are now unit tests for this library.  If you would like to submit a PR against this project please ensure that you include the appropriate unit tests.

In order to run the tests make sure you install the `dev-dependencies`

    pip install -r dev-requirements.txt

##Questions?

If you have any questions, don't hesitate to contact support@context.io
