# GlobalProtect Disable with Ticket

This Python script is used to retrieve a ticket from a remote server using a specific API key.

## Setup

The script uses the following environment variables:

- `PANORAMA_API_KEY`: The API key for accessing the server.
- `GP_REQUEST`: The raw request number.
- `DURATION_IN_MINUTES`: The requested duration for the ticket.
- `portal_name`: The name of the portal to access.
- `template_name`: The template name for the request.
- `BASE_URL`: The base URL for the API server.

These variables need to be set in your environment before running the script.

## Dependencies

This script uses the following Python libraries:

- `os`
- `re`
- `json`
- `httpx`
- `xmltodict`

Make sure these are installed in your environment. If they're not, you can install them using pip:

```sh
pip install httpx xmltodict
```

## Usage

Once you have set up your environment and installed the dependencies, you can run the script using Python 3:

```sh
python3 ticket_retrieval.py
```

The script will attempt to retrieve the ticket from the server. It will print the server's response to the console. It will also return a tuple containing the retrieved ticket (or an error message) and a boolean indicating whether the request failed.

**Note:** The script currently disables SSL/TLS verification when making the HTTP request. This may expose your application to risks. For a more secure application, consider providing a path to a certificate file for the `verify` parameter in the httpx.get() method.

This README provides basic information about what the script does, how to set it up, the dependencies, and how to use it. You can always add more details if needed, such as examples, more thorough setup instructions, known issues, etc.
