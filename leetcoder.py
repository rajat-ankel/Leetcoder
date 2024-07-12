import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

# Folder containing solution JSON files
solutions_folder = 'solutions'
# File to store solved problem names
solved_file = 'solved.json'
# File to store not solved problem names
notsolved_file = 'notsolved.json'

# Function to extract numeric prefix from filename
def extract_numeric_prefix(filename):
    numeric_prefix = ''
    for char in filename:
        if char.isdigit():
            numeric_prefix += char
        else:
            break
    return int(numeric_prefix) if numeric_prefix else float('inf')

# Load all JSON files in sequence based on numerical filename sorting
def load_solutions(folder):
    solutions = []
    filenames = sorted(os.listdir(folder), key=lambda x: extract_numeric_prefix(x))
    for filename in filenames:
        if filename.endswith('.json'):
            filepath = os.path.join(folder, filename)
            with open(filepath, 'r') as file:
                solutions.append(json.load(file))
    return solutions

# Load solved problem names
def load_solved_problems(solved_file):
    if os.path.exists(solved_file):
        with open(solved_file, 'r') as file:
            return json.load(file)
    return []

# Load not solved problem names
def load_notsolved_problems(notsolved_file):
    if os.path.exists(notsolved_file):
        with open(notsolved_file, 'r') as file:
            return json.load(file)
    return []

# Save solved problem names
def save_solved_problems(solved_file, solved_problems):
    with open(solved_file, 'w') as file:
        json.dump(solved_problems, file, indent=4)

# Save not solved problem names
def save_notsolved_problems(notsolved_file, notsolved_problems):
    with open(notsolved_file, 'w') as file:
        json.dump(notsolved_problems, file, indent=4)

# Wait for user to log in manually
def wait_for_manual_login(driver):
    driver.get('https://leetcode.com/accounts/login/')
    print("Please log in to LeetCode manually...")
    while True:
        if driver.current_url == 'https://leetcode.com/':
            print("Login successful!")
            break
        time.sleep(2)

# Submit solution
def submit_solution(driver, problem_name, code):
    # Replace \" with ""
    code = code.replace('\"\"', '""')

    url = f'https://leetcode.com/problems/{problem_name}/'
    driver.get(url)
    time.sleep(3)  # wait for the page to load

    try:
        # Find the textarea and clear it
        code_editor = driver.find_element(By.XPATH, '//textarea[@role="textbox"]')
        code_editor.click()
        code_editor.send_keys(Keys.CONTROL + 'a')
        code_editor.send_keys(Keys.DELETE)

        # Send the new solution code to the textarea
        code_editor.send_keys(code)
        
        # Format the code using Alt + Shift + F
        code_editor.send_keys(Keys.ALT, Keys.SHIFT, 'f')
        
        time.sleep(1)  # wait for the formatting to complete

        # Click the submit button
        submit_button = driver.find_element(By.XPATH, '//button[@data-e2e-locator="console-submit-button"]')
        submit_button.click()

        # Wait for submission result "Accepted"
        wait_time = 0
        while wait_time < 30:  # maximum wait time of 30 seconds
            try:
                result = driver.find_element(By.XPATH, '//span[@data-e2e-locator="submission-result"]').text
                if result == 'Accepted':
                    print(f"Solution for {problem_name} was accepted.")
                    return True
            except:
                pass
            time.sleep(1)
            wait_time += 1

        print(f"Solution for {problem_name} was not accepted or timed out waiting for result.")
        return False

    except Exception as e:
        print(f"Failed to submit solution for {problem_name}: {e}")
        return False

# Main function
def main():
    solutions = load_solutions(solutions_folder)
    solved_problems = load_solved_problems(solved_file)
    notsolved_problems = load_notsolved_problems(notsolved_file)

    # Combine both lists to avoid repeating problems
    all_attempted_problems = set(solved_problems + notsolved_problems)

    # Setup Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        wait_for_manual_login(driver)

        for solution in solutions:
            problem_name = solution['problemName']
            if problem_name in all_attempted_problems:
                print(f"Skipping already attempted problem: {problem_name}")
                continue

            code = solution['code']
            if submit_solution(driver, problem_name, code):
                solved_problems.append(problem_name)
                save_solved_problems(solved_file, solved_problems)
            else:
                notsolved_problems.append(problem_name)
                save_notsolved_problems(notsolved_file, notsolved_problems)

            # Update the set of all attempted problems
            all_attempted_problems.add(problem_name)
                
            time.sleep(2)  # wait before moving to the next problem

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
