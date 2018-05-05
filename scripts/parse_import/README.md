# Parse Import

This script is used to export the list of users from the legacy Parse platform to our new API.


## Usage Instructions

### Prerequisites

Before running the script, you must have admin access to both the old Parse platform as well as the new API. Specifically, you need the application ID and master key for Parse, as well as the email address and password of a staff account on the new API.

### Dependencies

The import script has a few dependencies. These can be installed with:

```bash
$ pip install -r requirements.txt
```

### Running It

The script can be run by simply calling

```bash
$ ./import.py
```

The credentials mentioned above can be passed to the program either through command line options or environment variables. The help text for the script contains specifics.

```bash
$ ./import.py --help
```

### Starting Over

If you would like to wipe the results of a previous import and start over, you can pass the `--delete` flag to the script. This will wipe all previously uploaded legacy users from the new API.

**Warning: This action is irreversible**

```bash
$ ./import.py --delete
$ ./import.py
```
