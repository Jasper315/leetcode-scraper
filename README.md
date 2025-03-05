# LeetCode Problem Scraper

This Python script helps you fetch the latest problems from LeetCode platform. It's designed to retrieve problem details programmatically using LeetCode's GraphQL API.

## Features

- Fetches the latest 50 LeetCode problems (configurable)
- Retrieves detailed information for each problem including description, difficulty, tags and code templates
- Saves the data in JSON format for easy processing
- Handles API errors gracefully with informative output

## Prerequisites

- Python 3.6 or newer
- Internet connection to access LeetCode API

## Installation

1. Clone this repository or download the source code
2. Create a virtual environment (recommended)
3. Install required dependencies:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

Simply run the script to fetch the latest 50 problems:

```bash
python leetcode_scraper.py
```

The script will:
1. Connect to LeetCode's GraphQL API
2. Fetch the list of all problems
3. Sort them by ID to get the latest problems
4. Retrieve detailed information for each of the 50 most recent problems
5. Save the results to a JSON file named `leetcode_latest_problems_YYYYMMDD_HHMMSS.json`

## Configuration

If you want to change the number of problems to fetch, modify the parameter in the `main()` function:

```python
# In main(), change 50 to your desired number
latest_problems = scraper.get_latest_problems(50)
```

## Output Format

The script generates a JSON file containing an array of problem objects. Each problem object includes:

- `questionId`: Internal LeetCode ID
- `questionFrontendId`: Problem number displayed on LeetCode
- `title`: Problem title
- `titleSlug`: URL-friendly identifier for the problem
- `content`: Detailed problem description (HTML format)
- `difficulty`: Problem difficulty (Easy, Medium, Hard)
- `topicTags`: Related topics/tags for the problem
- `codeSnippets`: Code templates in various programming languages
- `sampleTestCase`: Example test cases for the problem

## Important Notes

1. **Rate Limiting**: The script adds a 1-second delay between requests to avoid overwhelming LeetCode's servers. Do not modify this unless you want to risk being rate-limited or blocked.

2. **API Changes**: LeetCode may change their API structure at any time. If the script stops working, check for API changes and update the GraphQL queries accordingly.

3. **Premium Content**: Some problems may be marked as `isPaidOnly: true`. These are only accessible with a LeetCode Premium subscription.

4. **Problem Availability**: The newest problems may be from contests and might not be immediately visible on the public problem list on the website.

5. **Error Handling**: The script includes robust error handling, but if any issues occur, check the console output for detailed error messages.

## Using the Data

After running the script, you can use the JSON data for:
- Analyzing problem patterns and difficulty distribution
- Creating custom problem lists
- Building tools that interact with LeetCode problems
- Implementing offline problem viewers

## Troubleshooting

If you encounter issues:

1. Check your internet connection
2. Verify that LeetCode's website is accessible
3. Look for error messages in the console output
4. Ensure your Python environment is properly set up
5. Check if LeetCode has changed their API structure

## Contributing

If you find bugs or have suggestions for improvements, please feel free to contribute by submitting issues or pull requests.

## License
- Do not run this script too frequently to avoid straining the LeetCode server
- The script will have a 1 second delay when requesting question details to avoid too frequent requests
- LeetCode may change its API structure, and you may need to update your GraphQL query if the script does not work properly
- This project is for educational purposes. Use responsibly and respect LeetCode's terms of service. 