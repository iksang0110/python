from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def fetch_jobs_weworkremotely(search_term):
    url = f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={search_term}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    jobs = []

    for job_section in soup.find_all('section', class_='jobs'):
        for job in job_section.find_all('li', class_='feature'):
            title = job.find('span', class_='title').text.strip()
            company = job.find('span', class_='company').text.strip()
            link = "https://weworkremotely.com" + job.find('a')['href']

            jobs.append({
                'Company': company,
                'Title': title,
                'Link': link
            })

    return jobs


def fetch_jobs_web3career(search_term):
    url = f"https://web3.career/{search_term}-jobs"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    jobs = []

    for job in soup.find_all('div', class_='job-listing'):
        title = job.find('h4').text.strip()
        company = job.find('div', class_='company').text.strip()
        link = job.find('a', class_='apply-button')['href']

        jobs.append({
            'Company': company,
            'Title': title,
            'Link': link
        })

    return jobs


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        search_term = request.form.get("search_term", "")
        wework_jobs = fetch_jobs_weworkremotely(search_term)
        web3_jobs = fetch_jobs_web3career(search_term)
        all_jobs = wework_jobs + web3_jobs
        return render_template_string("""
            <h1>Job Listings for '{{ search_term }}'</h1>
            <ul>
                {% for job in all_jobs %}
                    <li><strong>{{ job['Title'] }}</strong> at {{ job['Company'] }} - <a href="{{ job['Link'] }}">Link</a></li>
                {% endfor %}
            </ul>
            <a href="/">Back</a>
        """, search_term=search_term, all_jobs=all_jobs)
    return '''
        <form method="post">
            <input type="text" name="search_term" placeholder="Enter a skill (e.g., Python)">
            <input type="submit" value="Search">
        </form>
    '''


if __name__ == "__main__":
    app.run(debug=True)
