import requests
from authentication import get_auth_header

def get_new_releases(url: str, access_token: str, offset: int=0, limit: int=20, next: str="") -> Dict[Any, Any]:
    """Perform get() request to new releases endpoint

    Args:
        url (str): Base url for the request
        access_token (str): Access token
        offset (int, optional): Page offset for pagination. Defaults to 0.
        limit (int, optional): Number of elements per page. Defaults to 20.
        next (str, optional): Next URL to perform next request. Defaults to "".

    Returns:
        Dict[Any, Any]: Request response

    Run:
        URL_NEW_RELEASES = "https://api.spotify.com/v1/browse/new-releases"
        releases_response = get_new_releases(url=URL_NEW_RELEASES, access_token=token.get('access_token'))

    # Note: the `access_token` value from the dictionary `token` can be
    retrieved either using `get()` method or dictionary syntax `token['access_token']`

    """

    if next == "":
        request_url = f"{url}?offset={offset}&limit={limit}"
    else:
        request_url = f"{next}"

    ### START CODE HERE ### (~ 4 lines of code)
    # Call get_auth_header() function and pass the access token.
    headers = get_auth_header(access_token=access_token)

    try:
        # Perform a get() request using the request_url and headers.
        response = requests.get(url=request_url, headers=headers)
        # Use json() method over the response to return it as Python dictionary.
        return response.json()
    ### END CODE HERE ###

    except Exception as err:
        print(f"Error requesting data: {err}")
        return {'error': err}




# NOTE!!!
# THIS FUNCTION IS NOT TESTED. IT IS MADE JUST TO GIVE AN IDEA OF THE LOGIC

def get_paginated_with_offset_new_releases(
    base_url: str, offset: int=0, limit: int=20, access_token: str, get_token: Callable, **kwargs
) -> list:
    """Performs paginated calls to the new releases endpoint. Manages token refresh when required.

    Args:
        base_url (str): Base URL for API requests (without offset and limit)
        access_token (str): Access token
        get_token (Callable): Function that requests access token

    Returns:
        list: Request responses stored as a list
    """

    # Get header containing access token
    headers = get_auth_header(access_token=access_token)

    # Add offset and limit to the base_url
    request_url = request_url = f"{url}?offset={offset}&limit={limit}"

    # Initialize list to store the retrieved data
    new_releases_data = []


    try:
        # Request first page
        print(f"Requesting to: {request_url}")
        response = requests.get(url=request_url, headers=headers)

        # check that the response has been retrieved
        # if condition over the status code of the response
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

        # extract the first page response content as a dictionary
        # add the response to the list new_releases_data
        response_dict = response.json()
        new_releases_data.extend(response_dict["albums"]["items"])

        # Get the total number of the elements in albums
        total_elements = response_dict["albums"]["total"]


        # Request following pages
        while offset < total_elements - limit:

            # Update the offset value
            # and update the url to make the next request with the new offset
            offset = response_dict["albums"]["offset"] + limit
            request_url = request_url = f"{url}?offset={offset}&limit={limit}"

            # Request page starting at offset
            response = requests.get(url=request_url, headers=headers)
            new_releases_data.extend(response_dict["albums"]["items"])

            print(f"Finished iteration for page with offset: {offset}, and number of items in response {len(responses)}")


        return new_releases_data

    except Exception as err:
        print(f"Error occurred during request: {err}")
        return []

































