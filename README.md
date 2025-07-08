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
  - [ 2.3 - Simple Request to New Releases](#2-3)
      - [ get_new_releases()](#2-3-a)
      - [ Result](#2-3-b)
  - [ 2.4 - Paginated Request to New Releases](#2-4)
      - [ Pagination)](#2-4-a)  
      - [ paginated_with_offset_new_releases())](#2-4-b)    
      - [ paginated_with_next_new_releases())](#2-4-b)         
            
- [ 3 - Batch pipeline](#3)
  - [ 3.1 - get_paginated_new_releases](#3-1)
      - [ Handle Token Refresh)](#3-1-a)  
  - [ 3.2 - get_paginated_album_tracks](#3-2)
      - [ Extract Info of Tracks in Each Album)](#3-2-a)  
        
  
- [ 4 - Optional](#4)  
  - [ 4.1 - Optional - API Rate Limits](#4-1)
  - [ 4.2 - Optional - Spotipy SDK](#4-2)
      - [ Paginated Request with SDK](#4-2-a)


---


## <center> 1 - CREATE A SPOTIFY APP </center>

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
## 2 - <center> UNDERSTAND THE BASICS OF APIs </center>

<a id='2-1'></a>
### 2.1 - Packages to Use

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



<a id='2-2'></a>
### 2.2 - Authentication Process

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

The output of this function is of the form:<br>
`<class 'requests.models.Response'>` <br>
`{'access_token': 'BQAkv5-zBtCzqoVPCO-bRz6xmWCIPrh323m6gvkJbXVTuDQCBjpbQQcFHlyDOiqJwHFe8fxmWDzFBUV1My5JdQxtujvSPhc3Pyv-duA85_zwTWLKwKAKEkjCRmIBjrJsdohoqBcjzgs', 'token_type': 'Bearer', 'expires_in': 3600}`

- It provides a temporary access token. 
- The `expires_in` field tells the duration of this token in seconds. 
  When this token expires, requests will fail and an error object will be returned holding a status code of 401. This status code means that the request is unauthorized.


<a id='2-2-c'></a>  
### get_auth_header()  
Whenever you send an API request to the spotify API, you need to include in the request the access token, as an authorization header following a certain format. <br>
The function `get_auth_header` in `authentication.py` expects the access token and returns the authorization header that can be included in the API request. 



<a id='2-3'></a>
### 2.3 - Simple Request to New Releases
*__Each API manages responses in its own way so it is highly recommended to read the documentation and understand the nuances behind the API endpoints you are working with.__*


<a id='2-3-a'></a>
#### get_new_releases()
The `get_new_releases` function in `endpoint_requests_less_efficient`:

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

To Run: <br>
pass the URL and the `access_token` value from the `token` object that you obtained before.

`URL_NEW_RELEASES = "https://api.spotify.com/v1/browse/new-releases"`

`releases_response = get_new_releases(url=URL_NEW_RELEASES, access_token=token.get('access_token'))`


<a id='2-3-b'></a>
##### Result
The result is a JSON object that was trasnformed into a python dictionary. Exploring the structure should give:

```python
releases_response.keys()
```
output: `dict_keys(['albums'])`

```python
releases_response.get('albums').keys()
```
output: dict_keys(['href', 'items', 'limit', 'next', 'offset', 'previous', 'total'])

  - `'href'`: this is the URL used for the request just sent
  - `'items'`:list of items returned
  - `'limit'`: maximum number of items that can be returned in this request.
  - `'offset'`: 
  - `'total'`: total number available items to be returned in this endpoint
  - `'previous'` and `'next'` will return the URL to the previous or next page respectively and they are based on the `offset` and `limit` parameters

  

<a id='2-4'></a>
### 2.3 - Paginated to New Releases

<a id='2-4-a'></a>
#### Pagination
`'limit'` and `'offset'` are the base of pagination in this API endpoint.

This limit on the number of elements returned is a common feature of several APIs and although in some cases you can modify such a limit, **a good practice is to use it with pagination** to get all the elements that can be returned. 

Each API handles pagination differently. 

For Spotify, the requests response provides you with two fields that allow you to query the different pages of your request: `previous` and `next`. In this case, there are two ways for you to explore the rest of the data:

- you can use the value from the next parameter to get the direct URL for the next page of requests, or 

- you can build the URL for the next page from scratch using the offset and limit parameters (make sure to update the offset parameter for the request). 

<br>
If you compare the URLs provided by the `href` and `next` fields, you can see that while the `limit` parameter remains the same, the `offset` parameter has increased with the same value as the one stored in `limit`.
```
{
...,
'href': 'https://api.spotify.com/v1/browse/new-releases?offset=0&limit=20',
...,
'next': 'https://api.spotify.com/v1/browse/new-releases?offset=20&limit=20',
...
}
```

And for the next one it is:

```
{
...,
'href': 'https://api.spotify.com/v1/browse/new-releases?offset=20&limit=20',
...,
'next': 'https://api.spotify.com/v1/browse/new-releases?offset=40&limit=20',
...
}
```

==> the `offset` increases by the value of the `limit`. 

As the responses show that the `total` value is 100, this means that you can access the last page of responses by using an `offset` of 80, while keeping the `limit` value as 20.

```
{
...,
'href': 'https://api.spotify.com/v1/browse/new-releases?offset=60&limit=20',
...,
'next': None,
...
}
```

In this case, the value of the `next` field is `None`, indicating that you reached the last page. On the other hand, you can see that `previous` contains the URL to request the data from the previous page, so you can even go backward if required.


<a id='2-4-b'></a>
#### paginated_with_offset_new_releases()

Two options: 
- make the endpoint request directly inside of the function
- use the previous function get_new_releases() as Callable to perform the endpoint request.

Basic logic used in both options: <br>
1. The first page is retrieved using requests.get(). <br>
    This page is addeded to the list new_releases_data.
2. The value of the offset is updated with the output of step 1
3. While loop: continue retrieving data from the endpoint as long as the offset is smaller than (total number of elemets - limit). <br>
  Append all the new data to the list new_releases_data
  
__Usage option 2__
```
responses = paginated_with_offset_new_releases_option_2(endpoint_request=get_new_releases,
                                   url=URL_NEW_RELEASES, 
                                   access_token=token.get('access_token'), 
                                   offset=0, limit=20)
```



<a id='2-4-b'></a>
#### paginated_with_next_new_releases()
Similar to get_paginated_with_offset_new_releases but instead of using a while loop over the offset-limit value, the url for the next page is used:

```python
# update the url to make the next request
request_url = response_json["albums"]["next"]
```


This allows for a much simpler logic

1. The first page is retrieved through the callable function endpoint_request (it uses requests.get() ). <br>
    This page is addeded to the list new_releases_data.
2. The value of the next_page variable is updated with the output of step 1
3. While loop: continue retrieving data from the endpoint as long as the value of next_page is not null. <br>
  Append all the new data to the list new_releases_data


__Usage__
```
responses_with_next = paginated_with_next_new_releases(endpoint_request=get_new_releases, 
                                                             url=URL_NEW_RELEASES, 
                                                             access_token=token.get('access_token'))
```


<a id='3'></a>
## <center> 3 - BATCH PIPELINE </center>

Pipeline that extracts the track information for the new released albums.

This pipeline uses two endpoints:
* [Get New Releases endpoint](https://developer.spotify.com/documentation/web-api/reference/get-new-releases) 
* [Get Album Tracks endpoint](https://developer.spotify.com/documentation/web-api/reference/get-an-albums-tracks): this endpoint allows you to get Spotify catalog information about an album’s tracks.

This pipeline uses three scripts that allow you to perform such extraction.
- The `endpoint.py` file contains two paginated api calls. 
    - The first one `get_paginated_new_releases`allows you get the list of new album releases using the same paginated call you used in the first part. 
    - The second one `get_paginated_album_tracks` allows you to get Spotify catalog information about an album’s tracks using the Get Album Tracks endpoint. 
- The `authentication.py` file contains the script of the `get_token` function that returns an access token.
- The `main.py` file calls the first paginated API call to get the ids of the new albums. Then for each album id, the second paginated API call is performed to extract the catalog information for each album id. 



<a id='3-1'></a>
### 3.1 - get_paginated_new_releases

<a id='3-1-a'></a>
#### Handle Token Refresh

In `endpoint_requests_less_efficient`, most of the functions manage paginated requests but without taking into account that the access token has a limited time. <br>
If your pipeline requests last more than 3600 seconds, you can get a 401 status code error. 

The first step in `get_paginated_new_releases` is to handle token refresh in case it expires:
* Check the status of the requests response. If it is 401 then get a new token
* The token has three keys: `access_token`, `token_type`, `expires_in`. Check that the response has the key `access_token` and get the header for the request, otherwise exit with a failing message.

```python
            if response.status_code == 401:  # Unauthorized
            
                # Handle token expiration and update
                token_response = get_token(**kwargs)
                if "access_token" in token_response:
                    headers = get_auth_header(
                        access_token=token_response["access_token"]
                    )
                    print("Token has been refreshed")
                    continue  # Retry the request with the updated token
                else:
                    print("Failed to refresh token.")
                    return []
```

<a id='3-2'></a>
### 3.2 - get_paginated_album_tracks

<a id='3-2-a'></a>
#### Extract info of tracks in each album

The following information will be passed to the function `get_paginated_album_tracks` to construct the full endpoint for the API call:

- Get Album Tracks Endpoint
    - To extract the information of the tracks that compose each album, the [Get Album Tracks endpoint Documentation](https://developer.spotify.com/documentation/web-api/reference/get-an-albums-tracks) is used.
    - `URL_ALBUM_TRACKS`: The base URL to get information from a particular album. 
    Looking at the documentation: you will have to complement that URL with the album ID and with the `tracks` string to complete the endpoint.

- In `main.py`: after the call to the `get_paginated_new_releases` function, 
the albums' IDs are extracted from the response and are saved into the `albums_ids` list. Those IDs will be used in the request. 

```python
    # Getting albums IDs
    albums_ids = [album["id"] for album in new_releases]
```


The function `get_paginated_album_tracks` has basically the same logic as `get_paginated_new_releases` 


<a id='4'></a>
## <center> 4 - OPTIONAL </center>

<a id='4-1'></a>
### 4.1 - Optional - API Rate Limits

Another important aspect to take into account when working with APIs is regarding the rate limits. Rate limiting is a mechanism used by APIs to control the number of requests that a client can make within a specified period of time. It helps prevent abuse or overload of the API by limiting the frequency or volume of requests from a single client. Here's how rate limiting typically works:

- Request Quotas: APIs may enforce a maximum number of requests that a client can make within a given time window, for example, 100 requests per minute.

- Time Windows: The time window specifies the duration over which the request quota is measured. For example, a rate limit of 100 requests per minute means that the client can make up to 100 requests in any 60-second period.

- Response to Exceeding Limits: When a client exceeds the rate limit, the API typically responds with an error code (such as 429 Too Many Requests) or a message indicating that the rate limit has been exceeded. This allows clients to adjust their behavior accordingly, such as by implementing [exponential backoff](https://medium.com/bobble-engineering/how-does-exponential-backoff-work-90ef02401c65) and other retry strategies. (Check [here](https://harish-bhattbhatt.medium.com/best-practices-for-retry-pattern-f29d47cd5117) or [here](https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/)). 

- Rate Limit Headers: APIs may include headers in the response to indicate the client's current rate limit status, such as the number of requests remaining until the limit resets or the time at which the limit will reset.

Rate limiting helps maintain the stability and reliability of APIs by ensuring fair access to resources and protecting against abusive or malicious behavior. It also allows API providers to allocate resources more effectively and manage traffic loads more efficiently.

You can also see more of the specifics of the rate limits of the Spotify Web API in the [documentation](https://developer.spotify.com/documentation/web-api/concepts/rate-limits). Particularly, this API doesn't enforce a hard limit for the number of requests done but it works dynamically based on the number of calls within a rolling 30 seconds window. You can find some [blogs](https://medium.com/mendix/limiting-your-amount-of-calls-in-mendix-most-of-the-time-rest-835dde55b10e#:~:text=The%20Spotify%20API%20service%20has,for%2060%20requests%20per%20minute) where experiments have been done to identify the average number of requests per minute. 

Below you are provided with a code that benchmarks the API calls; you can play with the number of requests and the request interval to see the average time of a request. In case you perform too many requests so that you violate the rate limits, you will get a 429 status code.

*Note*: This code may take a few minutes to run.

```Python

import time

# Define the Spotify API endpoint
endpoint = 'https://api.spotify.com/v1/browse/new-releases'

headers = get_auth_header(access_token=token.get('access_token'))

# Define the number of requests to make
num_requests = 200

# Define the interval between requests (in seconds)
request_interval = 0.1  # Adjust as needed based on the API rate limit

# Store the timestamps of successful requests
success_timestamps = []

# Make repeated requests to the endpoint
for i in range(num_requests):
    # Make the request
    response = requests.get(url=endpoint, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        success_timestamps.append(time.time())
    else:        
        print(f'Request {i+1}: Failed with code {response.status_code}')
    
    # Wait for the specified interval before making the next request
    time.sleep(request_interval)

# Calculate the time between successful requests
if len(success_timestamps) > 1:
    time_gaps = [success_timestamps[i] - success_timestamps[i-1] for i in range(1, len(success_timestamps))]
    print(f'Average time between successful requests: {sum(time_gaps) / len(time_gaps):.2f} seconds')
else:
    print('At least two successful requests are needed to calculate the time between requests.')

```




<a id='4-2'></a>
### 4.2 - Optional - Spotipy SDK

In several cases, the API developers also provide a Software Development Kit (SDK) to connect and perform requests to the different endpoints of the API without the necessity of creating the code from scratch. 

For Spotify Web API they developed the [Spotipy SDK](https://spotipy.readthedocs.io/en/2.22.1/) to do it. 

This is an example of how it will work to replicate the extraction of data from the new album releases endpoint in a paginated way.


``` python

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# 1. Credentials
credentials = SpotifyClientCredentials(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET
    )

spotify = spotipy.Spotify(client_credentials_manager=credentials)

credentials.get_access_token()

# 2. Get data from New album releases
limit = 20
response = spotify.new_releases(limit=limit)


``` 

1. The `credentials` object handles the authentication process and contains the token to be used in later requests.

        *Note*: Please ignore the `DeprecationWarning` message if you see an access token in the output.

2. Get data from new album releases

NOTE: You can also paginate through these responses. If you check the documentation of the [`new_releases` method](https://spotipy.readthedocs.io/en/2.22.1/#spotipy.client.Spotify.new_releases), you can see that you can specify the parameter `offset`, as you previously did. 



<a id='4-2-a'></a>
#### Paginated Request with SDK

``` python

def paginated_new_releases_sdk(limit: int=20) -> list:

    album_data = []

    album_data.extend(response['albums']['items'])
    total_albums_elements = response['albums']['total']
    offset_idx = list(range(limit, total_albums_elements, limit))

    for idx in offset_idx: 
        
        response_page = spotify.new_releases(limit=limit, offset=idx)
        album_data.extend(response_page['albums']['items'])

    return album_data
    
album_data_sdk = paginated_new_releases_sdk()
album_data_sdk[0]

```




