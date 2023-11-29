# AutoAmex

AutoAmex is a Python-based automation tool for interacting with the American Express website to add all available offers across all cards to your account.

## Requirements

The required Python packages are listed in `requirements.txt`. You can install them using pip:
```
bash
pip install -r requirements.txt
```

## Main Functionality

The main script is `autoamex.py`. It uses the following functions:

- `main(argv)`: This function is the entry point of the script. It accepts command line arguments to specify the browser to use (default is "Chrome").

- `amex_login_and_collect_offers(credentials, browser)`: This function logs into the American Express website using the provided credentials and browser. It logs various information, such as available offers and time taken for each operation.

## Configuration File

The configuration file should be a CSV file located in the `conf/` directory. It should contain your username and password for the American Express website, separated by a comma. Here's an example of what the file might look like:

```
username,password
```
Replace `username` and `password` with your actual username and password.

## Helper Functions

The `helper.py` script contains several helper functions:

- `load_config(filename)`: Reads a CSV file and returns a list of lists.

- `get_driver(browser)`: Returns a WebDriver instance for the specified browser.

- `amex_log_in(driver, usr, pwd, email_field_id='lilo_userName', pass_field_id='lilo_password')`: Logs into the American Express website.

- `amex_log_out(driver)`: Logs out of the American Express website.

- `click_on_offers(driver)`: Clicks on available offers on the American Express website.

- `collect_offer_names(driver)`: Collects the names of available offers.

## Running the Script

You can run the script from the command line as follows:
```
bash
python src/autoamex.py [browser]
```

Replace `[browser]` with the name of the browser you want to use (e.g., "Chrome", "Firefox"). If no browser is specified, "Chrome" is used by default.

## .gitignore

The `.gitignore` file is set to ignore certain file types, including `.pyc`, `.swp`, `.csv`, `.log`, `.json`, `.xlsx`, and `chromedriver*`

