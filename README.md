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



  - [ 2. - Get Token](#2-1)
  - [ 2.2 - Get New Releases](#2-2)
    - [ Exercise 1](#ex01)
  - [ 2.3 - Pagination](#2-3)
    - [ Exercise 2](#ex02) 
    - [ Exercise 3](#ex03)
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
### 2.1 - Get Token

The first step when working with an API is to understand the authentication process. <br>
For that, the Spotify APP generates a Client ID and a Client secret that you will use to generate an access token. <br> 
The access token is a string that contains the credentials and permissions that you can use to access a given resource. <br>
You can find more about it in the [API documentation](https://developer.spotify.com/documentation/web-api/concepts/access-token). <br>

Since each API is developed with a particular purpose, it is necessary for you to always read and understand the nuances of each API
 so you can access the data responsibly. 

Let's create some variables to hold the values of the client_id and client_secret that you stored in the src/env file.


In this package, the environment variables are loaded in the main() 
```python
load_dotenv('./src/env', override=True)

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
```

and should be saved in a file called env which should not be uploaded to github (by using .gitignore) . Example of env:

`CLIENT_ID=XXXXXXXXXXXXXXXXXXXXX
CLIENT_SECRET=XYXYXYXYXYXYXYXYXXYXYXY
AAP_NAME=spotify-app`


