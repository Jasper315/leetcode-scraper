import requests
import json
import time
from datetime import datetime

class LeetcodeScraper:
    def __init__(self):
        self.base_url = "https://leetcode.com"
        self.graphql_url = f"{self.base_url}/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        }
    
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
        response = requests.post(self.graphql_url, headers=self.headers, json=payload)
        
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
            topicTags {
              name
              slug
            }
            codeSnippets {
              lang
              langSlug
              code
            }
            sampleTestCase
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
        response = requests.post(self.graphql_url, headers=self.headers, json=payload)
        
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

def main():
    scraper = LeetcodeScraper()
    
    print("Starting to fetch latest LeetCode problems...")
    
    try:
        # Get the latest 50 problems
        latest_problems = scraper.get_latest_problems(50)
        
        # Save to JSON file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"leetcode_latest_problems_{timestamp}.json"
        scraper.save_to_json(latest_problems, filename)
        
        print(f"Scraping completed, results saved to {filename}")
    except Exception as e:
        print(f"Error during scraping process: {e}")

if __name__ == "__main__":
    main() 