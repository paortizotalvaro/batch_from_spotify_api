# Assignment:<br>Extract Data from Spotify API with Python

This is the lab of week 3 of the course Source Systems, Data Ingestion, and Pipelines of DeepLearning.AI in Coursera.
<br>
This lab is to learn 
- how to interact how to interact with the Spotify API 
- how to extract data from the API in a batch way. 
- what pagination means 
- how to send an API request that requires authorization.

##### Copyright notice
The content of this lab was made available by DeepLearning.AI. You may not use or distribute this code for commercial purposes. <br>
I have added my own modifications to the code for learning purposes. <br>
I added my own extra notes and reorganized the structure of the document for my own future reference.

# Table of Contents

- [ 1 - Create a Spotify APP](#1)
- [ 2 - Understand the Basics of APIs](#2)
  - [ 2.1 - Packages to use](#2-1)
  - [ 2.2 - Authentication Process](#2-2)
      - [ Client ID and Client secret](#2-2-a)
      - [ get_token()](#2-2-b)      
      - [ get_auth_header()](#2-2-c)      
  - [ 2.3 - Perform a Request to New Releases](#2-3)

  
  
  
  - [ 2.4 - Optional - API Rate Limits](#2-4)
- [ 3 - Batch pipeline](#3)
  - [ Exercise 4](#ex04)
  - [ Exercise 5](#ex05)
  - [ Exercise 6](#ex06)
- [ 4 - Optional - Spotipy SDK](#4)
  - [ Exercise 7](#ex07)

---


## 1 - Create a Spotify APP

To get access to the API resources, you need to create a Spotify account if you don't already have one. A trial account will be enough to complete this lab.

1. Go to https://developer.spotify.com/, create an account and log in.
2. Click on the account name in the right-top corner and then click on **Dashboard**.
3. Create a new APP using the following details:
   - App name: `dec2w2a1-spotify-app`
   - App description: `spotify app to test the API`
   - Website: leav<a id='1'></a>e empty
   - Redirect URIs: `http://localhost:3000`
   - API to use: select `Web API`
4. Click on **Save** button. If you get an error message saying that your account is not ready, you can log out, wait for a few minutes and then repeat again steps 2-4.
5. In the App Home page click on **Settings** and reveal `Client ID` and `Client secret`. Store them in the `src/env` file provided in this lab. Make sure to save the `src/env` file using `Ctrl + S` or `Cmd + S`.


Here's the link to [the Spotify API documentation](https://developer.spotify.com/documentation/web-api/tutorials/getting-started) that you can refer to while you're working on the lab's exercises. The required information to complete the tasks will be given during the lab. You will interact with two resources: 
- New album releases in the first and second parts ([endpoint](https://developer.spotify.com/documentation/web-api/reference/get-new-releases));
- Album tracks in the second part ([endpoint](https://developer.spotify.com/documentation/web-api/reference/get-an-albums-tracks)).

<a id='2'></a>
## 2 - Understand the Basics of APIs

<a id='2-1'></a>
### 2.1 - Packages to use

#### requests
Several packages in Python allow you to request data from an API; in this lab, you will use the `requests` package, 
which is a popular and versatile library to perform HTTP requests. It provides a simple and easy-to-use way to 
interact with web services and APIs. Let's load the required packages:

```Python
import requests
```

#### dotenv
Source: copilot
The dotenv package is commonly used in Node.js or Python projects to load environment variables from a .env file into your application, and it's especially useful when making API requests to services like Spotify.

```python
from dotenv import load_dotenv
```

*Why Use dotenv with the Spotify API?*
  - Security:
      Spotify API requires sensitive credentials like:
      - CLIENT_ID
      - CLIENT_SECRET
      - REDIRECT_URI (for OAuth flows)
      These are private and should never be exposed in your source code, especially if it's stored in a public repository.Storing these directly in your code is risky.

      Environment variables allow you to keep them hidden and secure.

      dotenv allows you to keep them in a separate .env file, which you can exclude from version control (e.g., via .gitignore).

  - Convenience:
      When using environment variables:
      - You can easily switch between environments (development, testing, production) by changing the .env file without modifying your code.
      - Avoid changing your code when deploying to different systems.
      - Keep your codebase clean and maintainable.


  - Cleaner Code:
      Instead of hardcoding values, you use: process.env.CLIENT_ID


  - Best Practice for API Integration
      When working with APIs like Spotify’s, you often need to:
      - Authenticate using OAuth 2.0
      - Store tokens or secrets
      - Set callback URLs
      All of these are better managed through environment variables to avoid hardcoding and to follow industry best practices.



<a id='2-1'></a>
### 2.1 - Authentication Process

The first step when working with an API is to understand the authentication process. <br>

Since each API is developed with a particular purpose, it is necessary for you to always read and understand the nuances of each API so you can access the data responsibly. 

<a id='2-2-a'></a>
### Client ID and Client secret
The Spotify APP generates a Client ID and a Client secret that you will use to generate an access token. <br> 
The access token is a string that contains the credentials and permissions that you can use to access a given resource. <br>
You can find more about it in the [API documentation](https://developer.spotify.com/documentation/web-api/concepts/access-token). <br>

The values of the client_id and client_secret that you stored in the src/env file are assigned to variables in the main() as enviroment variables:

```python
load_dotenv('./src/env', override=True)

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
```

They should be saved in a file called env which should not be uploaded to github (by using .gitignore) . Example of env:

`CLIENT_ID=XXXXXXXXXXXXXXXXXXXXX` <br>
`CLIENT_SECRET=XYXYXYXYXYXYXYXYXXYXYXY` <br>
`AAP_NAME=spotify-app`


<a id='2-2-b'></a>
### get_token()
The `get_token` function in `authentication.py` takes a Client ID, Client secret and a URL as input, and performs a POST request to that URL to obtain an access token using the client credentials. 

The output of this function is of the form:
`<class 'requests.models.Response'>`

`{'access_token': 'BQAkv5-zBtCzqoVPCO-bRz6xmWCIPrh323m6gvkJbXVTuDQCBjpbQQcFHlyDOiqJwHFe8fxmWDzFBUV1My5JdQxtujvSPhc3Pyv-duA85_zwTWLKwKAKEkjCRmIBjrJsdohoqBcjzgs', 'token_type': 'Bearer', 'expires_in': 3600}`

- It provides a temporary access token. 
- The `expires_in` field tells the duration of this token in seconds. 
  When this token expires, requests will fail and an error object will be returned holding a status code of 401. This status code means that the request is unauthorized.


<a id='2-2-c'></a>  
### get_auth_header()  
Whenever you send an API request to the spotify API, you need to include in the request the access token, as an authorization header following a certain format. <br>
The function `get_auth_header` in `authentication.py` expects the access token and returns the authorization header that can be included in the API request. 



<a id='2-3'></a>
### Perform a Request to New Releases
__Each API manages responses in its own way so it is highly recommended to read the documentation and understand the nuances behind the API endpoints you are working with.__

#### Simple Request: get_new_releases()
The `get_new_releases` function:

1. Calls the function `get_auth_header`and passes to it the access token (which is specified as input to the `get_new_releases` function). 
2. It saves the output of `get_auth_header` to a variable called `headers`.
3. `request_url` variable contains the URL used to perform a `get()` request, together with `headers`
  ```python
  response = requests.get(url=request_url, headers=headers)
  ```
3. Request `response` is an object of type `requests.models.Response`. This object has a method named `json()` that allows you to transform the response content into a JSON object or plain Python dictionary. This method is used on the `response` object to return the content as a Python dictionary.

4. The `URL_NEW_RELEASES` is the URL or endpoint to perform calls to the API. <br>
  It is defined in main()
  
  ```python
  URL_NEW_RELEASES = "https://api.spotify.com/v1/browse/new-releases"
  ```

Usage: pass the URL and the `access_token` value from the `token` object that you obtained before.

`URL_NEW_RELEASES = "https://api.spotify.com/v1/browse/new-releases"`

`releases_response = get_new_releases(url=URL_NEW_RELEASES, access_token=token.get('access_token'))`

##### Result
The result is a JSON object that was trasnformed into a python dictionary. Exploring the structure should give:

