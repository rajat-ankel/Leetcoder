# LeetCode Automation Bot

This project automates the process of submitting solutions to LeetCode problems. It uses Selenium WebDriver to interact with LeetCode's website and submit solutions from JSON files.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [License](#license)
- [Contact](#contact)

## Introduction

The LeetCode Automation Bot helps in automating the submission of solutions to LeetCode problems. It supports the following:
- Loading solutions from JSON files.
- Automatically submitting solutions and checking for successful submissions.
- Storing lists of solved and not solved problems.

## Features

- **Manual Login**: Allows users to manually log in to LeetCode.
- **Automated Submission**: Automatically submits solutions and checks for "Accepted" results.
- **Track Solved/Not Solved Problems**: Maintains records of solved and not solved problems in separate JSON files.
- **Scheduled Updates**: (Optional) Can be integrated with scheduling libraries to run at specific intervals.

## Installation

### Prerequisites

Ensure you have the following installed:

- [Python 3.6+](https://www.python.org/downloads/)
- [Google Chrome](https://www.google.com/chrome/)

### Steps

1. **Clone the repository:**

    ```sh
    git clone https://github.com/rajat-ankel/leetcode-automation-bot.git
    cd leetcode-automation-bot
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Submitting Solutions

To start the solution submission process, run:

```sh
python leetcoder.py


### Scrap Solutions

For Scraping New Solutions, run:

```sh
python leetscraper.py
