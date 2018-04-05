## JIRA Status
### Python module for collecting information on a JIRA project.

## Table of Contents

* [Configuration](#configuration)
* [Usage](#usage)
* [Options](#options)
* [License](#license)

## Configuration

Rename the `sample.configuration.json` to `configuration.json` and enter the configuration values.

## Usage

```bash
python .\jira-status\ --verbose
```

You can find the output of the script in the `logs` directory of the project.

## Options

Option | Description | Usage
---    | ---         | ---
Verbose | Outputs the status and information about the script's progress to the CLI. | `--verbose`
Email | Sends an email based on the `configuration.json` file. | `--email`

## License

MIT