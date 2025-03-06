import json
import os
import re
import glob
from datetime import datetime

def extract_stats(stats_str):
    """Extract acceptance rate and submission counts from stats string"""
    if not stats_str:
        return {
            "acceptance_rate": None,
            "total_submissions": None,
            "total_accepted": None
        }
    
    try:
        # The stats string format is typically something like:
        # {"totalAcceptedRaw": 1234, "totalSubmissionRaw": 5678, "totalAccepted": "1.2K", "totalSubmission": "5.6K", "acRate": "21.7%"}
        stats_dict = json.loads(stats_str)
        
        acceptance_rate = stats_dict.get("acRate", "0%").strip("%")
        try:
            acceptance_rate = float(acceptance_rate)
        except:
            acceptance_rate = 0.0
            
        total_submissions = stats_dict.get("totalSubmissionRaw", 0)
        total_accepted = stats_dict.get("totalAcceptedRaw", 0)
        
        return {
            "acceptance_rate": acceptance_rate,
            "total_submissions": total_submissions,
            "total_accepted": total_accepted
        }
    except Exception as e:
        print(f"Error extracting stats: {e}")
        print(f"Stats string: {stats_str}")
        return {
            "acceptance_rate": None,
            "total_submissions": None,
            "total_accepted": None
        }

def extract_company_tags(company_tags_str):
    """Extract company tags from company tag stats string"""
    if not company_tags_str:
        return []
    
    try:
        companies = json.loads(company_tags_str)
        # Companies are usually in a format like: [{"slug": "company-name", "name": "Company Name", "frequency": 42}]
        return [company.get("name") for company in companies if "name" in company]
    except Exception as e:
        print(f"Error extracting company tags: {e}")
        print(f"Company tags string: {company_tags_str}")
        return []

def extract_similar_questions(similar_questions_str):
    """Extract similar questions into a readable format"""
    if not similar_questions_str:
        return []
    
    try:
        # Similar questions are usually stored as a JSON string
        similar_questions = json.loads(similar_questions_str)
        
        # Format each similar question for readability
        formatted_questions = []
        for question in similar_questions:
            title = question.get("title", "")
            difficulty = question.get("difficulty", "")
            title_slug = question.get("titleSlug", "")
            
            # Format as "Title [Difficulty]"
            formatted_question = f"{title} [{difficulty}]"
            
            # Add URL if title_slug is available
            if title_slug:
                formatted_question += f": https://leetcode.com/problems/{title_slug}/"
                
            formatted_questions.append(formatted_question)
            
        return formatted_questions
    except Exception as e:
        print(f"Error extracting similar questions: {e}")
        print(f"Similar questions string: {similar_questions_str}")
        return []

def transform_leetcode_data(input_file, output_file):
    """Transform LeetCode JSON data into a more structured format"""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    transformed_data = []
    
    for problem in data:
        # Extract base fields
        problem_id = problem.get("questionFrontendId")
        name = problem.get("title")
        difficulty = problem.get("difficulty")
        
        # Extract tags
        tags = []
        if "topicTags" in problem and problem["topicTags"]:
            tags = [tag.get("name") for tag in problem["topicTags"] if "name" in tag]
        
        # Extract stats
        stats_str = problem.get("stats")
        stats = extract_stats(stats_str)
        
        # Extract company tags
        company_tags_str = problem.get("companyTagStats")
        companies = extract_company_tags(company_tags_str)
        
        # Get discussion count
        discussion_count = problem.get("discussionCount", 0)
        
        # Get likes and dislikes
        likes = problem.get("likes", 0)
        dislikes = problem.get("dislikes", 0)
        
        # Extract similar questions
        similar_questions_str = problem.get("similarQuestions")
        similar_questions = extract_similar_questions(similar_questions_str)
        
        # Create the transformed problem entry
        transformed_problem = {
            "Id": problem_id,
            "name": name,
            "tags": tags,
            "difficulty": difficulty,
            "acceptance_rate": stats["acceptance_rate"],
            "total_submissions": stats["total_submissions"],
            "total_accepted": stats["total_accepted"],
            "companies": companies,
            "discussion_count": discussion_count,
            "likes": likes,
            "dislikes": dislikes,
            "similar_questions": similar_questions,
            "url": f"https://leetcode.com/problems/{problem.get('titleSlug', '')}/",
            # Keep these useful fields but they won't be included in CSV
            "content": problem.get("content"),
            "code_snippets": problem.get("codeSnippets")
        }
        
        transformed_data.append(transformed_problem)
    
    # Sort by ID (typically numeric, but could be alphanumeric)
    try:
        transformed_data.sort(key=lambda x: (
            int(re.search(r'\d+', x["Id"]).group()) if x["Id"] and re.search(r'\d+', x["Id"]) else float('inf')
        ))
    except Exception as e:
        print(f"Error sorting data: {e}")
    
    # Save to output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transformed_data, f, ensure_ascii=False, indent=2)
    
    print(f"Transformed data saved to {output_file}")
    return transformed_data

def create_csv_from_json(json_file, csv_file):
    """Create a CSV file from the transformed JSON data"""
    import csv
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Extract field names from the first record
    if not data:
        print("No data to export to CSV")
        return
    
    fieldnames = [
        "Id", "name", "difficulty", "acceptance_rate", 
        "total_submissions", "total_accepted", "tags",
        "companies", "discussion_count", "likes", "dislikes", 
        "similar_questions", "url"
    ]
    
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        
        for problem in data:
            # Convert lists to comma-separated strings for CSV
            problem_copy = problem.copy()
            if "tags" in problem_copy and isinstance(problem_copy["tags"], list):
                problem_copy["tags"] = ", ".join(problem_copy["tags"])
            if "companies" in problem_copy and isinstance(problem_copy["companies"], list):
                problem_copy["companies"] = ", ".join(problem_copy["companies"])
            if "similar_questions" in problem_copy and isinstance(problem_copy["similar_questions"], list):
                problem_copy["similar_questions"] = " | ".join(problem_copy["similar_questions"])
                
            writer.writerow(problem_copy)
    
    print(f"CSV data saved to {csv_file}")

def main():
    # Find latest JSON file based on modification time
    json_files = glob.glob("leetcode_problems_*.json")
    json_files = [f for f in json_files if not f.endswith('_transformed.json')]
    
    if not json_files:
        print("No LeetCode problem JSON files found in the current directory")
        return
    
    # Sort files by modification time, newest first
    latest_file = max(json_files, key=os.path.getmtime)
    
    print(f"Found latest problem file: {latest_file}")
    
    # Extract ID range from filename
    id_range_match = re.search(r'leetcode_problems_(\d+)_to_(\d+)', latest_file)
    if id_range_match:
        start_id = id_range_match.group(1)
        end_id = id_range_match.group(2)
        id_range = f"{start_id}_{end_id}"
    else:
        id_range = "unknown_range"
    
    # Generate output filenames with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"leetcode_problems_{id_range}_{timestamp}_transformed.json"
    csv_file = f"leetcode_problems_{id_range}_{timestamp}_transformed.csv"
    
    print(f"Processing {latest_file}...")
    transformed_data = transform_leetcode_data(latest_file, output_file)
    create_csv_from_json(output_file, csv_file)
    print(f"Completed processing {latest_file}")
    print(f"Generated {output_file} and {csv_file}")
    
    # Clean up old transformed files (optional)
    # Delete all but the newest transformed files to avoid clutter
    all_transformed_jsons = glob.glob("*_transformed.json")
    all_transformed_csvs = glob.glob("*_transformed.csv")
    
    if len(all_transformed_jsons) > 3:  # Keep last 3 transformed JSONs
        old_jsons = sorted(all_transformed_jsons, key=os.path.getmtime)[:-3]
        for old_file in old_jsons:
            print(f"Removing old transformed file: {old_file}")
            try:
                os.remove(old_file)
            except Exception as e:
                print(f"Error removing {old_file}: {e}")
    
    if len(all_transformed_csvs) > 3:  # Keep last 3 transformed CSVs
        old_csvs = sorted(all_transformed_csvs, key=os.path.getmtime)[:-3]
        for old_file in old_csvs:
            print(f"Removing old transformed file: {old_file}")
            try:
                os.remove(old_file)
            except Exception as e:
                print(f"Error removing {old_file}: {e}")

if __name__ == "__main__":
    main() 