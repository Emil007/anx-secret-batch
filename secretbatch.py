import csv
import requests
import sys

INPUT_FILE = "input.csv"
OUTPUT_FILE = "output.csv"
API_URL = "https://secret.anexia.com/api/secret"

try:
    # Open the input CSV file with semicolon delimiter
    with open(INPUT_FILE, mode="r", newline='', encoding="utf-8") as infile, \
         open(OUTPUT_FILE, mode="w", newline='', encoding="utf-8") as outfile:
        reader = csv.DictReader(infile, delimiter=';')
        # Prepare fieldnames for output: original fields + 'SecretLink'
        fieldnames = reader.fieldnames if reader.fieldnames is not None else []
        fieldnames = list(fieldnames)  # make a mutable copy
        fieldnames.append("SecretLink")
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()

        # Process each row from input
        for row in reader:
            # Construct the secret content as "Key: Value" lines
            lines = []
            for col in reader.fieldnames:  # use original column order
                value = row.get(col, "")
                lines.append(f"{col}: {value}")
            secret_text = "\n".join(lines)

            secret_link = ""
            try:
                # Create the secret via Anexia Secret API
                response = requests.post(API_URL, json={"secret": secret_text})
                # Raise an HTTPError if the response was not successful (status != 200)
                response.raise_for_status()
            except Exception as api_err:
                # Log the error with row identification (e.g., Name or index)
                identifier = row.get("Name") or "Row {}".format(reader.line_num)
                print(f"Error: Failed to create secret for {identifier} - {api_err}", file=sys.stderr)
                secret_link = ""
            else:
                # Parse the API JSON response to get the secret URL
                try:
                    data = response.json()
                except ValueError:
                    print(f"Error: Invalid JSON response for row {row.get('Name', reader.line_num)}", file=sys.stderr)
                    data = {}
                # The API is expected to return an identifier or URL for the secret
                if "fullUrl" in data:
                    # If API gave a full URL (assuming key name 'fullUrl')
                    secret_link = data["fullUrl"]
                elif "url" in data:
                    # If API gave a slug or partial URL, construct the full link
                    slug = data["url"]
                    if slug:
                        # Some responses might already include the domain in 'url'
                        if not slug.startswith("http"):
                            secret_link = f"https://secret.anexia.com/secret/{slug}"
                        else:
                            secret_link = slug
                else:
                    # If no expected key, log an error
                    print(f"Warning: No URL returned for {row.get('Name', reader.line_num)}", file=sys.stderr)
                    secret_link = ""

            # Write the output row (including the SecretLink, even if blank on failure)
            output_row = {**row, "SecretLink": secret_link}
            writer.writerow(output_row)
except FileNotFoundError:
    print(f"Error: Input file '{INPUT_FILE}' not found.", file=sys.stderr)
except Exception as e:
    # Catch-all for any other errors
    print(f"Unexpected error: {e}", file=sys.stderr)
