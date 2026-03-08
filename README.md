# Mobileye_task--Chen_Siton
Mobileye Solution for Validation Engineer

## Mobileye Log Parser

This project contains a Python solution (`solution.py`) for analyzing a communication session log (`data.txt`) against a protocol metadata specification (`protocol.json`).

## Requirements
- Python 3.x

## Files
- `solution.py`: Contains the `Solution` class with logic to answer 6 specific questions about the log data.
- `data.txt`: The log data file containing comma-separated rows of messages.
- `protocol.json`: Contains expected protocol specifications, frames per second (FPS), dynamic size traits, and mapping of protocols to versions.

## Usage
Run the script from your terminal:

```bash
python solution.py
```

## Questions Implemented

1. **Version Detection**: Extracts and decodes the version name from the first log message sequence in `data.txt`.
2. **Frequency Checks**: Identifies protocols that appear at the wrong frequency compared to their expected frequency based on their expected FPS.
3. **Missing Protocols**: Identifies protocols listed as relevant for the detected version in `protocol.json` but are completely missing from the `data.txt` log.
4. **Unexpected Protocols**: Identifies protocols that actually appear in the `data.txt` log but are not listed as relevant for the detected version in `protocol.json`.
5. **Payload Size Verification**: Identifies protocols where the expected size integer specified in a log line does not match the actual byte length of the trailing hexadecimal message content.
6. **Inconsistent Static Sizes**: Identifies protocols marked as `dynamic_size: false` in `protocol.json` that erroneously declare inconsistent expected message sizes throughout the log file.

## Helper Methods & Error Handling
To keep the code clean and strictly validated, we implemented the following:
- **`_get_relevant_pids()`**: A helper method that fetches all relevant Protocol IDs for the current version.
- **`_get_observed_pids_counts()`**: A helper method that counts the frequencies of all Protocol IDs that actually appear in the log file, avoiding duplicated parsing logic.
- **Strict Version Checking (KeyError)**: If the version detected in `data.txt` (e.g., `Version1`) is not defined in `protocol.json`, the script will forcefully raise a `KeyError: "Version 'Version1' not found in protocol.json"` instead of silently failing and returning empty lists.
