"""penn_jobs.py, this program extracts Pennylvania government jobs of interest and sends an email to my Gmail account with the results."""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from time import sleep
import ezgmail
import os
from dotenv import load_dotenv

# add more searches to this list as needed
JOB_LINKS = [
    "https://www.governmentjobs.com/careers/pabureau?keywords=intelligence",
    "https://www.governmentjobs.com/careers/pabureau?keywords=investigator",
    "https://www.governmentjobs.com/careers/pabureau?keywords=python"
]

def main():
    """
    Scrapes jobs of interest from Pennylvania government job search website and then emails the jobs to my Gmail account.
    
    """
    results_dict = {}

    for job_search in JOB_LINKS:
        html = get_html(job_search)
        jobs = parse_html(html)
        results_dict[job_search.replace("%20","_").split("=")[1]] = jobs

    results_text = write_jobs_text(results_dict)

    # change email below as needed
    load_dotenv()
    email = os.getenv('EMAIL_ADDRESS')
    ezgmail.send(email, "PSU Jobs", results_text)

def get_html(job_search):
    """
    Fetches the HTML content of a provided Pennylvania government job search URL using a headless Firefox browser.

    Args:
    job_search (str): The URL of the Pennylvania government job search.

    Returns:
    str: The inner HTML content of the retrieved webpage.
    """
    options = Options()
    options.add_argument(
        "--headless"
    )  # prevents Firefox browser from obviously opening
    browser = webdriver.Firefox(options=options)
    browser.get(job_search)
    sleep(5) # sleep for 5 seconds to allow time for the JavaScript to load
    inner_html = browser.execute_script("return document.body.innerHTML")
    return inner_html


def parse_html(html):
    """
    Parses the HTML content of a Pennylvania government job search page and extracts relevant job details.

    Args:
    html (str): The HTML content of the job search page.

    Returns:
    list: A list of lists, where each inner list contains details for a single job posting
    (job title, job URL, date of job posting).
    """
    results = []
    soup = BeautifulSoup(html, "html5lib")
    for e in soup.find('div', class_="search-results-grid-container").select('tr'):
        temp_results = []
        if "data-job-id" in str(e):
            temp_results.append((e.select("a")[0].getText()))
            temp_results.append(
                "https://www.governmentjobs.com" + e.find("a").get("href")
            )
        if "job-table-posted" in str(e):
            if e.find("td",class_="job-table-posted hidden-sm hidden-xs"):
                temp_results.append("Posted: " + e.find("td",class_="job-table-posted hidden-sm hidden-xs").get_text())
            if e.find("td",class_="job-table-closing"):
                temp_results.append("Closing: " + e.find("td",class_="job-table-closing").get_text())
        results.append(temp_results)
    return results


def write_jobs_text(results_dict):
    """
    Formats a dictionary containing extracted job details into a text string suitable for email notification.

    Args:
    results_dict (dict): A dictionary containing job search terms as keys and lists of job details as values.

    Returns:
    str: A formatted text string containing job titles, URLs, and dates of job posting for relevant jobs.
    """
    results_text = """"""
    for k in results_dict.keys():
        results_text += k.upper() + " JOBS"
        results_text += "\n"
        for v in results_dict[k]:
            if v != []:
                for value in v:
                    results_text += value
                    results_text += "\n"
                results_text += "\n"
    results_text += "\n"
    return results_text

if __name__ == "__main__":
    main()