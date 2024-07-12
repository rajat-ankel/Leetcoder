import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urlparse

base_url = "https://walkccc.me/LeetCode/problems/"
start_problem = 1
end_problem = 4000
folder_name = "solutions"
os.makedirs(folder_name, exist_ok=True)

for problem_num in range(start_problem, end_problem + 1):
    url = base_url + str(problem_num)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find LeetCode URL
    leetcode_url = None
    h1_tag = soup.find('h1')
    if h1_tag:
        a_tag = h1_tag.find('a', href=True)
        if a_tag:
            leetcode_url = a_tag['href']
        else:
            print(f"LeetCode URL not found for problem {problem_num}. Skipping.")
            continue
    else:
        print(f"Header tag not found for problem {problem_num}. Skipping.")
        continue

    # Extract problem name from the LeetCode URL
    parsed_url = urlparse(leetcode_url)
    path_segments = parsed_url.path.strip('/').split('/')
    problem_name = path_segments[-1]

    # Find solution content
    solution_content = "Solution not found."
    code_tags = soup.find_all("code")
    for code_tag in code_tags:
        # Remove all <span class="c1"> elements
        for span_tag in code_tag.find_all("span", class_="c1"):
            span_tag.decompose()

        # Get text from the cleaned code tag
        code_text_parts = []
        for element in code_tag.descendants:
            if isinstance(element, str):
                code_text_parts.append(element.strip())
        code_text = ' '.join(code_text_parts)

        if len(code_text) > 30:  # Adjust threshold if necessary
            solution_content = code_text
            break  # Found the main solution code, stop searching

    # Prepare data to write to JSON
    data = {
        "problemName": problem_name,
        "language": "cpp",
        "code": solution_content
    }

    # Construct JSON filename with problem number prefix
    json_filename = os.path.join(folder_name, f"{problem_num}_{problem_name}.json")

    # Write data to JSON file
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"Saved solution for {problem_num}_{problem_name}.json.")

print("All solutions scraped and saved.")