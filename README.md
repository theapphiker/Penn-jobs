# penn_jobs
Collection of scripts that scrape Pennsylvania-based jobs of interest based on keywords and then emails the results.

<h2>Requirements</h2>

<b>Modules</b>
<ul>
<li>bs4</li>
<li>selenium</li>
<li>python-dotenv</li>
<li>html5lib</li>
</ul>

If you have PIP installed, type: `pip install -r requirements.txt` from the command line and your system should install all required modules.

<b>Sending Emails using Python</b>

GeeksforGeeks has <a href='https://www.geeksforgeeks.org/send-mail-gmail-account-using-python/'>instructions</a> for sending emails using SMTP (Simple Mail Transfer Protocol). I store the sender, receiver, and sender password in a .env file on my system that the script accesses. This is by no means secure or best practice, but works for this purpose on my local system.

<b>Firefox</b>

These scripts require having the <a href='https://www.mozilla.org/en-US/firefox/new/'>Firefox web browser</a> installed on your system. The scripts could be modified to work with other web browsers.

<h2>Schedule Python Scripts to Run Daily</h2>

I have scheduled these scripts to run daily on my system. Please see <a href='https://www.geeksforgeeks.org/schedule-python-script-using-windows-scheduler/'>GeeksforGeeks instructions</a> for one way to do this.

<h2>Example Output</h2>

The user should receive an email with results similar to the below picture.
<img src="https://github.com/theapphiker/Penn-jobs/blob/2d90b94f47375b2a6164b2aac210c71d9704a8d0/example_output.png" alt="example output">

