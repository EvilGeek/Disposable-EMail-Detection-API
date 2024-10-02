# DispoEMailAPI

DispoEMailAPI is a Flask-based API designed to check if an email or domain belongs to a disposable email provider. It also includes functionality for suggesting correct email domains, checking MX (Mail Exchange) records, and distinguishing between public and disposable domains.

## Features

- **Check Disposable Domains**: Verify if a domain or email is from a disposable email provider.
- **Public Domain Detection**: Identify whether a domain is a known public domain (e.g., Gmail, Yahoo).
- **MX Record Lookup**: Look up the best MX records for a domain.
- **Email Domain Suggestion**: Suggest alternative, valid email domains if a typo is detected.

## Requirements

- Python 3.7+
- Flask
- SQLite (built-in with Python)
