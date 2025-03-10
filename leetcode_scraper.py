import requests
import json
import time
from datetime import datetime

class LeetcodeScraper:
    def __init__(self, username=None, password=None, session_id=None):
        self.base_url = "https://leetcode.com"
        self.graphql_url = f"{self.base_url}/graphql"
        self.login_url = f"{self.base_url}/accounts/login/"
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        }
        self.session = requests.Session()
        
        # Apply existing session cookie if provided
        if session_id:
            self.headers["Cookie"] = f"LEETCODE_SESSION={session_id}"
            self.session.cookies.set("LEETCODE_SESSION", session_id, domain="leetcode.com", path="/")
            print("Using provided session ID for authentication")
            self.is_premium = self.check_premium_status()
        # Log in if credentials are provided
        elif username and password:
            self.login(username, password)
            self.is_premium = self.check_premium_status()
        else:
            print("No authentication credentials provided. Running in anonymous mode.")
            self.is_premium = False
    
    def login(self, username, password):
        """Log in to LeetCode with the provided credentials"""
        print(f"Attempting to log in as {username}...")
        
        # First, get the CSRF token
        response = self.session.get(self.login_url)
        if response.status_code != 200:
            print(f"Failed to get login page: {response.status_code}")
            return False
        
        # Extract CSRF token
        csrf_token = None
        for line in response.text.split('\n'):
            if 'csrfToken' in line:
                try:
                    # Try to extract token from JavaScript
                    csrf_token = line.split('"')[1]
                    break
                except:
                    pass
        
        if not csrf_token:
            print("Could not find CSRF token, login will likely fail")
        
        # Prepare login data
        login_data = {
            'login': username,
            'password': password,
            'csrfmiddlewaretoken': csrf_token,
            'next': '/'
        }
        
        # Add CSRF token to headers
        headers = {
            'Referer': self.login_url,
            'User-Agent': self.headers['User-Agent']
        }
        
        # Attempt login
        response = self.session.post(self.login_url, data=login_data, headers=headers)
        
        # Check if login was successful
        if response.url != self.login_url and 'login' not in response.url:
            print("Login successful!")
            
            # Update headers with new cookies
            self.headers["Cookie"] = "; ".join([f"{c.name}={c.value}" for c in self.session.cookies])
            
            # Print session ID for future use
            if 'LEETCODE_SESSION' in self.session.cookies:
                session_id = self.session.cookies.get('LEETCODE_SESSION')
                print(f"Your LEETCODE_SESSION ID: {session_id}")
                print("You can use this session ID for future runs without login")
            
            return True
        else:
            print("Login failed!")
            return False
            
    def check_premium_status(self):
        """Check if the current user has LeetCode Premium"""
        query = """
        query {
          userStatus {
            isPremium
            username
          }
        }
        """
        
        payload = {
            "query": query
        }
        
        try:
            response = self.session.post(self.graphql_url, headers=self.headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                if "data" in data and "userStatus" in data["data"]:
                    is_premium = data["data"]["userStatus"].get("isPremium", False)
                    username = data["data"]["userStatus"].get("username", "Anonymous")
                    if is_premium:
                        print(f"Logged in as {username} with Premium subscription")
                    else:
                        print(f"Logged in as {username} without Premium subscription")
                    return is_premium
        except Exception as e:
            print(f"Error checking premium status: {e}")
        
        print("Could not verify premium status, assuming non-premium")
        return False
    
    def get_all_problems(self):
        """Get basic information for all problems"""
        # Use allQuestions query, which is currently available in the API
        query = """
        query {
          allQuestions {
            questionId
            questionFrontendId
            title
            titleSlug
            difficulty
            isPaidOnly
          }
        }
        """
        
        payload = {
            "query": query
        }
        
        print(f"Fetching problem list...")
        response = self.session.post(self.graphql_url, headers=self.headers, json=payload)
        
        print(f"Problem list response status code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Response data structure: {list(data.keys())}")
                
                # Check if the response contains the data
                if "data" in data and data["data"] is not None and "allQuestions" in data["data"]:
                    questions = data["data"]["allQuestions"]
                    print(f"Retrieved {len(questions)} problems")
                    return questions
                else:
                    print(f"Problem list data not found in response")
                    print(f"Response content: {json.dumps(data, indent=2)[:500]}...")
                    return []
            except Exception as e:
                print(f"Error parsing response data: {e}")
                print(f"Raw response content: {response.text[:500]}...")
                return []
        else:
            print(f"Failed to fetch problem list: {response.status_code}")
            print(f"Response content: {response.text[:500]}...")
            return []
    
    def get_problem_detail(self, title_slug):
        """Get detailed information for a single problem"""
        query = """
        query questionData($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            questionId
            questionFrontendId
            title
            titleSlug
            content
            difficulty
            stats
            companyTagStats
            topicTags {
              name
              slug
            }
            similarQuestions
            codeSnippets {
              lang
              langSlug
              code
            }
            sampleTestCase
            likes
            dislikes
            discussionCount
          }
        }
        """
        
        variables = {
            "titleSlug": title_slug
        }
        
        payload = {
            "query": query,
            "variables": variables
        }
        
        print(f"Fetching problem details: {title_slug}")
        response = self.session.post(self.graphql_url, headers=self.headers, json=payload)
        
        print(f"Problem detail response status code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if "data" in data and data["data"] is not None and "question" in data["data"]:
                    return data["data"]["question"]
                else:
                    print(f"Problem details not found in response")
                    print(f"Response content: {json.dumps(data, indent=2)[:500]}...")
                    return None
            except Exception as e:
                print(f"Error parsing problem detail response: {e}")
                print(f"Raw response content: {response.text[:500]}...")
                return None
        else:
            print(f"Failed to fetch problem detail: {response.status_code}")
            print(f"Response content: {response.text[:500]}...")
            return None
    
    def save_to_json(self, data, filename):
        """Save data to a JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Data saved to {filename}")
    
    def get_latest_problems(self, count=50):
        """Get information for the latest problems"""
        all_problems = self.get_all_problems()
        
        if not all_problems:
            print("No problem list retrieved, cannot get latest problems")
            return []
        
        # Sort problems by ID to get the latest ones
        try:
            # Use questionId field for sorting
            sorted_problems = sorted(all_problems, key=lambda x: int(x.get("questionId", "0")), reverse=True)
            latest_problems = sorted_problems[:count]
            print(f"Retrieved latest {len(latest_problems)} problems")
        except Exception as e:
            print(f"Error sorting problems: {e}")
            print(f"Problem example: {json.dumps(all_problems[0], indent=2)}")
            return []
        
        # Get detailed information
        detailed_problems = []
        for problem in latest_problems:
            title = problem.get("title", "Unknown Problem")
            title_slug = problem.get("titleSlug", "")
            print(f"Fetching details for problem: {title}")
            
            if not title_slug:
                print(f"Problem {title} has no titleSlug, skipping")
                continue
                
            detail = self.get_problem_detail(title_slug)
            if detail:
                detailed_problems.append(detail)
                print(f"Successfully fetched details for: {title}")
            else:
                print(f"Failed to fetch details for: {title}")
            time.sleep(1)  # Avoid too frequent requests
        
        print(f"Total detailed problems retrieved: {len(detailed_problems)}")
        return detailed_problems
    
    def get_problems_by_id_range(self, start_id=2200, end_id=2800):
        """Get problems with frontend IDs in a specific range"""
        all_problems = self.get_all_problems()
        
        if not all_problems:
            print("No problem list retrieved, cannot get problems by ID range")
            return []
        
        # Filter problems by frontend ID in the specified range
        try:
            filtered_problems = []
            for problem in all_problems:
                try:
                    frontend_id = int(problem.get("questionFrontendId", "0"))
                    if start_id <= frontend_id <= end_id:
                        filtered_problems.append(problem)
                except ValueError:
                    # Skip if frontend ID is not a number
                    continue
                    
            print(f"Found {len(filtered_problems)} problems with IDs between {start_id} and {end_id}")
        except Exception as e:
            print(f"Error filtering problems by ID range: {e}")
            return []
        
        # Get detailed information
        detailed_problems = []
        for problem in filtered_problems:
            title = problem.get("title", "Unknown Problem")
            title_slug = problem.get("titleSlug", "")
            frontend_id = problem.get("questionFrontendId", "Unknown ID")
            print(f"Fetching details for problem {frontend_id}: {title}")
            
            if not title_slug:
                print(f"Problem {title} has no titleSlug, skipping")
                continue
                
            detail = self.get_problem_detail(title_slug)
            if detail:
                detailed_problems.append(detail)
                print(f"Successfully fetched details for: {title}")
            else:
                print(f"Failed to fetch details for: {title}")
            time.sleep(1)  # Avoid too frequent requests
        
        print(f"Total detailed problems retrieved: {len(detailed_problems)}")
        return detailed_problems

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='LeetCode Problem Scraper with Authentication Support')
    parser.add_argument('--username', type=str, help='LeetCode username')
    parser.add_argument('--password', type=str, help='LeetCode password')
    parser.add_argument('--session', type=str, help='LeetCode session ID (alternative to username/password)')
    parser.add_argument('--start-id', type=int, default=2200, help='Start of problem ID range')
    parser.add_argument('--end-id', type=int, default=2210, help='End of problem ID range')
    parser.add_argument('--latest', type=int, help='Number of latest problems to fetch (alternative to ID range)')
    
    args = parser.parse_args()
    
    # Initialize scraper with authentication if provided
    scraper = LeetcodeScraper(
        username=args.username,
        password=args.password,
        session_id=args.session
    )
    
    print("Starting LeetCode Problem Scraper...")
    
    try:
        # Determine which problems to fetch
        if args.latest:
            print(f"Fetching the latest {args.latest} problems...")
            problems = scraper.get_latest_problems(args.latest)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"leetcode_latest_problems_{args.latest}_{timestamp}.json"
        else:
            # Default to ID range
            start_id = args.start_id
            end_id = args.end_id
            print(f"Fetching problems with IDs between {start_id} and {end_id}...")
            problems = scraper.get_problems_by_id_range(start_id, end_id)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"leetcode_problems_{start_id}_to_{end_id}_{timestamp}.json"
        
        # Save to JSON file
        scraper.save_to_json(problems, filename)
        
        print(f"Scraping completed, results saved to {filename}")
        
        # Create a marker file to indicate this is the latest scrape
        with open("latest_scrape_file.txt", "w") as f:
            f.write(filename)
            
        # Log premium status for reference
        premium_status = "premium account" if scraper.is_premium else "free account"
        print(f"Data was fetched using a {premium_status}")
        if not scraper.is_premium:
            print("Note: Company tags data requires a premium account.")
            
    except Exception as e:
        print(f"Error during scraping process: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 