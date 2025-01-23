"""psu_jobs.py, this program extracts Penn State jobs of interest and sends an email to my Gmail account with the results."""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from time import sleep
import os
from dotenv import load_dotenv
import smtplib
from datetime import date

# add more searches to this list as needed
JOB_LINKS = [
    "https://psu.wd1.myworkdayjobs.com/PSU_Staff?q=secret",
    "https://psu.wd1.myworkdayjobs.com/PSU_Staff?q=risk",
    "https://psu.wd1.myworkdayjobs.com/PSU_Staff?q=data%20analyst",
    "https://psu.wd1.myworkdayjobs.com/PSU_Staff?q=python",
    "https://psu.wd1.myworkdayjobs.com/en-US/PSU_Staff?q=ARL"
]

def main():
    """
    Scrapes jobs of interest from Penn State Workday job search website and then emails the jobs to my Gmail account.
    
    """
    results_dict = {}

    print("Getting jobs...")
    for job_search in JOB_LINKS:
        html = get_html(job_search)
        jobs = parse_html(html)
        results_dict[job_search.replace("%20","_").split("=")[1]] = jobs


    print("Writing email with jobs...")
    results_text = write_jobs_text(results_dict)

   # adding job search information and current date
    today = date.today()
    formatted_date = today.strftime("%m/%d/%Y")
    results_text = "PSU Jobs for " + formatted_date + "\n\n" + results_text

    # change email in .env as needed
    load_dotenv()
    sender_email = os.getenv('SENDER_EMAIL_ADDRESS')
    receiver_email = os.getenv('RECEIVER_EMAIL_ADDRESS')
    pw = os.getenv('APP_PASSWORD')
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender_email, pw)
    s.sendmail(sender_email, receiver_email, results_text)
    s.quit()
    print("Email sent!")

def get_html(job_search):
    """
    Fetches the HTML content of a provided Penn State Workday job search URL using a headless Firefox browser.

    Args:
    job_search (str): The URL of the Penn State Workday job search.

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
    Parses the HTML content of a Penn State Workday job search page and extracts relevant job details.

    Args:
    html (str): The HTML content of the job search page.

    Returns:
    list: A list of lists, where each inner list contains details for a single job posting
    (job title, job URL, date of job posting).
    """
    results = []
    soup = BeautifulSoup(html, "html5lib")
    for e in soup.select("li"):
        temp_results = []
        if "jobTitle" in str(e):
            temp_results.append((e.select("a")[0].getText()))
            temp_results.append(
                "https://psu.wd1.myworkdayjobs.com" + e.find("a").get("href")
            )
            try:
                temp_results.append(e.select("dd")[1].getText())
            except:
                pass
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
            if v != [] and "Posted 30+ Days Ago" not in " ".join(v):
                for value in v:
                    results_text += value
                    results_text += "\n"
                results_text += "\n"
    results_text += "\n"
    return results_text

if __name__ == "__main__":
    main()