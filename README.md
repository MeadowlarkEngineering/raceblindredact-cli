# Redact CLI

A Command Line Tool for redacting documents using [RaceBlindRedact.com]

This tool is a self-contained executable written in python.  There are no external dependencies and no installation is required besides copying the executable to a permanent location.

Contact support@meadowlarkengineering.com for questions.

## Installation

**Step 1:** Download the [latest release zip file](https://github.com/MeadowlarkEngineering/raceblindredact-cli/releases) for either Linux or Windows.

**Step 2:** Unzip the tool and copy the executable named `redact` to the preferred location.   If you are just evaluating the tool, then you can copy it to your home directory.  If you are installing it permanently, then place it in a location where it can be found by the operating system such as `/usr/local/bin` for linux or `C:\Program Files` for windows.

## Running

The `redact` command line tool (CLI) can be run in a windows command shell, a windows powershell, or a linux shell.  

A valid RaceBlindRedact API Token is required in order to redact documents using the tool.  To receive a token contact support@meadowlarkengineering.com

The token is specified in one of three ways in the following order.

1. By providing the token on the command line using the `--token` option
2. By setting the REDACT_API_TOKEN environment variable.
3. By saving the token to the file $HOME/.redact_api_token

If the token is not specified on the command line, and the environment variable is not set, and the `$HOME/.redact_api_token` file does not exist, then the user is prompted to create the file `$HOME/.redact_api_token` and the token is saved to that file.

### Basic Usage

The `redact` command takes two mandatory arguments, an **input** file which must be a PDF, PNG, JPG, or TIFF document, and an **output** file, which will be where the output pdf document is saved. 

For example. If the executable was saved in the users home directory, they can run the following command to redact the document `input.pdf`
```
$HOME/redact d:\CaseMaterials\CaseNumber\input.pdf d:\CaseMaterials\CaseNumber\input-redacted.pdf
```

### Additional Options

The following command line options are available.

- **--version** Display the version of the redact CLI tool
- **--token <token>** Set the API token to use
- **--mode {image,text}** Set the redaction mode. There are two modes. 
  - **text** In text mode, text is extracted and then redacted. The output document does not have the formatting of the input document. 
  - **image** In image mode, the original layout of the input is preserved in the output.  This is the *default* mode if not otherwise specified.
- **-api-url <url>** The URL of the redaction service.  This defaults to https://api.raceblindredact.com and should not be changed unless specifically instructed by support staff for troubleshooting purposes.


### Errors

There are two errors that may be encountered when using the redaction service

1. **401 Unauthorized**.  If the provided token is invalid or expired, then the command will fail an error message stating the request was unauthorized.

2. **429 Rate Limit Exceeded**.  If the command is run consecutively at a rate that is faster than allowed, then the command will fail with an error message stating the Rate Limit was exceeded.  In this situation waiting 15-30 seconds and retrying the command will fix the issue.


## License
This code is freely available under the [MIT License](LICENSE)

Copyright 2024 Meadowlark Engineering LLC
