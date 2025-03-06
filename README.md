# LeetCode Problem Dataset Extractor

This repository contains a comprehensive dataset extraction tool for LeetCode problems, designed for educational and research purposes. The toolset allows researchers and educators to collect structured data about LeetCode coding problems for academic analysis, algorithm research, and educational content creation.

## Academic Purpose

This dataset is intended solely for academic and educational purposes, including but not limited to:

- **Algorithm Analysis**: Studying problem patterns, difficulty distributions, and algorithmic approaches
- **Computer Science Education**: Creating instructional materials with real-world problem examples
- **Technical Interview Research**: Analyzing trends in technical interview questions
- **Visualization and Data Mining**: Exploring relationships between different programming concepts

## Disclaimer

This project is not affiliated with, endorsed by, or sponsored by LeetCode. All data is collected through public APIs for academic research purposes only. Please ensure you comply with LeetCode's Terms of Service when using this tool.

## Features

- Extract problem metadata (ID, title, difficulty, tags, etc.)
- Collect problem statistics (acceptance rate, submission count, etc.)
- Gather user engagement metrics (likes, dislikes, discussion count)
- Identify related problems through similar questions mapping
- Support for authentication to access premium data (requires LeetCode Premium)
- Transform raw data into research-friendly CSV and JSON formats

## Requirements

- Python 3.6+
- Required packages listed in `requirements.txt`

## Installation

1. Clone this repository
2. Create a virtual environment (recommended)
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

To scrape problems within a specific ID range:

```bash
python leetcode_scraper.py --start-id 2200 --end-id 2300
```

### Authentication (Optional)

For accessing premium features (like company tags), you can authenticate with:

```bash
python leetcode_scraper.py --username "your_username" --password "your_password" --start-id 2200 --end-id 2300
```

Or use a session ID (more secure):

```bash
python leetcode_scraper.py --session "your_leetcode_session_id" --start-id 2200 --end-id 2300
```

### Data Transformation

After scraping, transform the data into research-friendly formats:

```bash
python transform_data.py
```

This will:
1. Find the most recent scraped data file
2. Transform it into a structured format
3. Generate both JSON and CSV outputs
4. Clean up older transformed files

## Output Data Format

The transformed data includes:

| Field | Description |
|-------|-------------|
| Id | Problem frontend ID |
| name | Problem title |
| difficulty | Easy/Medium/Hard |
| acceptance_rate | Percentage of successful submissions |
| total_submissions | Total number of submissions |
| total_accepted | Number of accepted submissions |
| tags | Algorithm/data structure categories |
| companies | Companies where this problem appeared (Premium) |
| discussion_count | Number of discussion posts |
| likes | Number of upvotes |
| dislikes | Number of downvotes |
| similar_questions | Related problems with links |
| url | URL to the problem |

## Best Practices

- Add a 1-second delay between requests (already implemented)
- Avoid frequent login/scraping to prevent rate-limiting
- Store session IDs securely if using authentication
- Consider scraping during off-peak hours

## Ethics and Responsible Use

When using this dataset for research:

1. Cite LeetCode as the source of the problems
2. Do not use the data for commercial purposes
3. Respect intellectual property rights
4. Follow responsible data mining practices

## Citation

If you use this dataset in your research, please cite it as:

```
@misc{leetcode-dataset,
  author = {Your Name},
  title = {LeetCode Problem Dataset Extractor},
  year = {2023},
  publisher = {GitHub},
  url = {https://github.com/yourusername/leetcode-dataset}
}
```

## License

This project is available for academic and educational use only. See LICENSE file for details.

## Contributing

Contributions to improve the dataset extraction tools are welcome. Please feel free to submit pull requests or open issues to discuss potential improvements. 