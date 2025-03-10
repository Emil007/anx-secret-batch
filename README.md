# Create Secrets from CSV Using Anexia Secret API

This script reads an `input.csv` file, publishes each row as a one-time viewable secret on the [Anexia Secret API](https://secret.anexia.com/docs), then writes an `output.csv` containing the original data plus the published secret links.

## Features

- **CSV input with semicolon delimiter** (e.g., `Name;User;Passwort;Server`)
- **No password** for secrets: anyone with the link can view it **once**
- **Single-use** secrets expire after first retrieval (by default)

## Requirements

- Python 3.7+ (it should work on Python 3.x generally)
- [Requests](https://pypi.org/project/requests/) library

## Usage

1. **Clone** this repository or copy the script into your local project folder.
2. **Install dependencies**:
   ```bash
   pip install requests
3. **Prepare your CSV**:
   - Name the file `input.csv`.
   - Use `;` as a delimiter (for example, `Name;User;Passwort;Server`).

4. **Run the script**:
   ```bash
   python3 secretbatch.py
The script will:
- Read your `input.csv`.
- Publish each row as a one-time secret on Anexia Secret.
- Write an `output.csv` with all original columns plus a new `SecretLink` column.

5. **Check your `output.csv**:
   - It contains the same data from `input.csv` plus the `SecretLink` column with the generated one-time URLs.

## Example

Given an `input.csv` such as:

  ```csv
  Name;User;Passwort;Server
  Herbert Krcal;hkcral;passwort1234;server1.example.com
  Baum Mann;bmann;passwortbm1234;server2.example.com
  ```

Each secret is published with the contents:

  ```yaml
  Name: Herbert Krcal
  User: hkcral
  Passwort: passwort1234
  Server: server1.example.com
  ```
The output.csv looks like:

  ```csv
  Name;User;Passwort;Server;SecretLink
  Herbert Krcal;hkcral;passwort1234;server1.example.com,https://secret.anexia.com/secret/<unique-id>
  ```

## Customizing

- **Change the expiry**: Adjust the JSON payload if you want a custom expiration (e.g., `+1 hour`).
- **Add a password**: Provide `"password": "somepassword"` in the JSON payload if you want password protection.
- **Delimiter**: Modify both `csv.DictReader(delimiter=';')` and `csv.DictWriter(delimiter=';')` if you use a different CSV format.
