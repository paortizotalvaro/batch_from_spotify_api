from typing import Callable

import requests
from authentication import get_auth_header        

def get_paginated_new_releases(
    base_url: str, access_token: str, get_token: Callable, **kwargs
) -> list:
    """Performs paginated calls to the new releases endpoint. Manages token refresh when required.

    Args:
        base_url (str): Base URL for API requests
        access_token (str): Access token
        get_token (Callable): Function that requests access token

    Returns:
        list: Request responses stored as a list
    """
    headers = get_auth_header(access_token=access_token)
    request_url = base_url
    new_releases_data = []

    try:
        while request_url:
            print(f"Requesting to: {request_url}")
            response = requests.get(url=request_url, headers=headers)

            # check that the response has been retrieved
            # if the status code is 401, retrieve the token again
            # exit if no access token is retrieved
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
            

            # extract the response content as a dictionary
            response_json = response.json()

            # add the response to the list new_releases_data
            new_releases_data.extend(response_json["albums"]["items"])

            # update the url to make the next request
            request_url = response_json["albums"]["next"]

        return new_releases_data

    except Exception as err:
        print(f"Error occurred during request: {err}")
        return []


def get_paginated_album_tracks(
    base_url: str,
    access_token: str,
    album_id: str,
    get_token: Callable,
    **kwargs,
) -> list:
    """Performs paginated requests to the album/{album_id}/tracks endpoint

    Args:
        base_url (str): Base URL for endpoint requests
        access_token (str): Access token
        album_id (str): Id of the album to be queried
        get_token (Callable): Function that requests access token

    Returns:
        list: Request responses stored as a list
    """
    ### Exercise 5:
    ### START CODE HERE ### (~ 23 lines of code)
    # Call the get_auth_header() function with the access token.
    headers = get_auth_header(access_token=access_token)
    #  Create the requests_url by using the base_url and album_id parameters. 
    request_url = f"{base_url}/{album_id}/tracks"
    album_data = []

    try:
        while request_url:

            # Perform a GET request for the first page.
            print(f"Requesting to: {request_url}")
            response = requests.get(url=request_url, headers=headers)
            print(f"response {response}")

            # check that the response has been retrieved
            # if the status code is 401, retrieve the token again
            # exit if no access token is retrieved
            if response.status_code == 401:  # Unauthorized
                
                # Handle token expiration and update.
                token_response = get_token(**kwargs)
                if "access_token" in token_response:
                    # Call get_auth_header() function with the "access_token" from the token_response.
                    headers = authentication.get_auth_header(
                        access_token=token_response["access_token"]
                    )
                    print("Token has been refreshed")
                    continue  # Retry the request with the updated token
                else:
                    print("Failed to refresh token.")
                    return []

            # Convert the response to json using the json() method.
            response_json = response.json()

            # Extend the album_data list with the value from "items" in response_json.
            album_data.extend(response_json["items"])

            # Update request_url with the "next" value from response_json.
            request_url = response_json["next"]


    except Exception as err:
        print(f"Error occurred during request: {err}")
        return []
