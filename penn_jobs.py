"""penn_jobs.py, this program extracts Pennylvania government jobs of interest and sends an email to my Gmail account with the results."""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from time import sleep
import os
from dotenv import load_dotenv
import smtplib
from datetime import date
import threading

def main():
    """
    Scrapes jobs of interest from Pennylvania government job search website and then emails the jobs to my Gmail account.
    
    """
    # add more searches to this list as needed
    job_links = [
    "https://www.governmentjobs.com/careers/pabureau?keywords=intelligence",
    "https://www.governmentjobs.com/careers/pabureau?keywords=investigator",
    "https://www.governmentjobs.com/careers/pabureau?keywords=python",
    "https://www.governmentjobs.com/careers/pabureau?keywords=sql",
    "https://www.governmentjobs.com/careers/pabureau?keywords=analyst"
]
    results_dict = {}
    lock = threading.Lock()

    print("Getting jobs...")
    threads = []
    for job_search in job_links:
         thread = threading.Thread(target = write_to_dict, args = (results_dict, job_search, lock))
         threads.append(thread)
         thread.start()

    for thread in threads:
         thread.join()  # Wait for all threads to complete

    # adding text for email
    print("Writing email with jobs...")
    results_text = write_jobs_text(results_dict)

    # adding job search information and current date
    today = date.today()
    formatted_date = today.strftime("%m/%d/%Y")
    results_text = "Penn Government Jobs for " + formatted_date + "\n\n" + results_text

    # change email in .env file as needed
    load_dotenv()
    sender_email = os.getenv('SENDER_EMAIL_ADDRESS')
    receiver_email = os.getenv('RECEIVER_EMAIL_ADDRESS')
    pw = os.getenv('APP_PASSWORD')
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender_email, pw)
    s.sendmail(sender_email, receiver_email, str(results_text).encode('utf-8'))
    s.quit()
    print("Email sent!")

def write_to_dict(the_dict, search, lock):
    """
    Writes the HTML content retrieved for a given search query to a global dictionary.

    This function fetches the HTML content associated with a search query using `get_html()`,
    processes the query to create a key, and stores the HTML content in the the_dict dictionary.
    The function uses a lock to ensure thread-safe access to the shared dictionary.

    Args:
    search: The search query string.  This string is expected to be a URL or URL-encoded string
    from which a key will be extracted.

    Returns:
    None.  This function modifies the_dict in place.
    """
    results = get_html(search)
    with lock:
        the_dict[search.replace("%20","_").split("=")[1]] = results


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
     browser.quit()
     jobs = parse_html(inner_html)
     return jobs

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
    if soup.find('div', class_="search-results-grid-container") is None:
        results.append([])
    else:
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
        if results_dict[k] == [[]]:
            results_text += "No jobs found."
            results_text += "\n"
            results_text += "\n"
        else:
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