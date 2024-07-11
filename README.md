# penn_jobs
Collection of scripts that scrape Pennsylvania-based jobs of interest based on keywords and then emails the results.

<h2>Requirements</h2>

<b>Modules</b>
<ul>
<li>bs4</li>
<li>selenium</li>
<li>time</li>
<li>ezgmail</li>
</ul>

If you have PIP installed, type: `pip install -r requirements.txt` from the command line and your system should install all required modules.

<b>EZGmail</b>

Please read Al Sweigart's <a href='https://github.com/asweigart/ezgmail'>documentation and instructions</a> for setting up EZGmail to allow your Python script to access a Gmail account.
The user must save their email address in a .env file with the variable name "EMAIL_ADDRESS".

<b>Firefox</b>

These scripts require having the <a href='https://www.mozilla.org/en-US/firefox/new/'>Firefox web browser</a> installed on your system. The scripts could be modified to work with other web browsers.

<h2>Schedule Python Scripts to Run Daily</h2>

I have scheduled these scripts to run daily on my system. Please see <a href='https://www.geeksforgeeks.org/schedule-python-script-using-windows-scheduler/'>GeeksforGeeks instructions</a> for one way to do this.

<h2>Example Output</h2>

The user should receive an email with results similar to the below picture.
![example_output](https://github.com/theapphiker/penn_jobs/assets/84999858/eb4013c0-80aa-4cb2-93c2-82cdb8436380)

