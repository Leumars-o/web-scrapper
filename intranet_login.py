""" This module is responsible for extracting relevant data from the user's intranet

    Returns:
        _type_: dict
                The relevant data from the intranet module
"""
import requests
import os
from datetime import datetime
from dotenv import load_dotenv
import json
from bs4 import BeautifulSoup


# set base url
url = "https://intranet.alxswe.com/auth/sign_in"

# Load environment variables
load_dotenv()
email = os.getenv('USER_EMAIL')
password = os.getenv('USER_PASSWORD')


def fetch_projects():
    """ This function is responsible for extracting relevant data from the user's intranet

    Returns:
        _type_: dict
                The relevant data from the intranet module
    """

    # Create session with cookies and user-agent
    with requests.Session() as session:
        # Get initial page to potentially capture CSRF token and cookies
        page = session.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Extract CSRF token
        csrf_token = soup.find('input', {'name': 'authenticity_token'})['value']
        if not csrf_token:
            print("Couldn't find CSRF token element.")
            exit()

        cookie = session.cookies.get_dict()['_holberton_intranet_session']
        if not cookie:
            print("No session cookies found.")
            exit()

        # Prepare headers with cookies and user-agent
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-US,en;q=0.9",
            "Cache-Control": "max-age=0",
            "Content-Type": "application/x-www-form-urlencoded",
            "Cookie": f"_holberton_intranet_session={cookie}; timezone=1",
            "Dnt": "1",
            "Origin": "https://intranet.alxswe.com",
            "Priority": "u=0, i",
            "Referer": "https://intranet.alxswe.com/auth/sign_in",
            "Sec-Ch-Ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": "\"Android\"",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Mobile Safari/537.36"
        }
            
        # Prepare login payload with extracted data
        payload = {
            "authenticity_token": f"{csrf_token}",
            "user[email]": f"{email}",
            "user[password]": f"{password}",
            "user[remember_me]": 0,
            "commit": "Log+in"
        }

        # Create dictionary of projects
        projects = {}

        # Send login request with payload and headers
        response = session.post(url, headers=headers, data=payload)
        current_url = response.url
        
        # Check if login was successful
        if current_url == "https://intranet.alxswe.com/dashboard":
            print("Login successful.")
        elif current_url == "https://intranet.alxswe.com/auth/sign_in":
            print("Login failed.")
            exit()
        else:
            tokens = current_url.split('/')
            if "evaluation_quizzes" in tokens:
                projects['evaluation_quiz'] = tokens[-1]
        
        # Handle the response here
        soup = BeautifulSoup(response.text, 'html.parser')


        # Get All Months Average
        monthly_average = soup.find('tbody')
        if monthly_average:
            # Get Average for Current Month
            month_average = monthly_average.find_all('td', class_='text-right')
            month_average = month_average[-1].text.strip()
            projects['Month Average'] = month_average
        else:
            projects['Month Average'] = 0

        # Get Active projects
        list_group = soup.find('ul', class_='list-group')

        if list_group:

            all_projects = list_group.find_all('li', class_='list-group-item')

            #Loop through projects and sort out the relevant information
            for active_project in all_projects:

                #Extract progress percentage
                progress_percent = active_project.find('div', class_='project_progress_percentage')
                progress = progress_percent.text.strip() if progress_percent else None
                # print (f"Progress: {progress}")
            
                #Extract project name
                anchor_tag = active_project.find('a')
                project_name = anchor_tag.text.strip() if anchor_tag else None
                project_link = anchor_tag.get('href') if anchor_tag else None

                #Extract start date
                start_date_element = active_project.find('div', class_="d-inline-block", attrs= {'data-react-class': 'common/DateTime'})

                if start_date_element:
                    start_date_json = start_date_element.get('data-react-props') if start_date_element else None
                        
                    start_date = None
                    start_time = None
                
                    if start_date_json:
                        try:
                            #Parse JSON string to extract start date if JSON is valid
                            start_date_data = json.loads(start_date_json)
                            date_string = start_date_data.get('value')
                            date_string, start_time = date_string.split('T')
                            start_date = datetime.strptime(date_string, '%Y-%m-%d').strftime('%A %B %d, %Y')
                            start_time = start_time[:5]

                        except json.JSONDecodeError:
                            print(f"Error parsing JSON for the start date  in project: {project_name}")
                    
                # Extract Project Deadline
                deadline_element = active_project.find_all('div', class_="d-inline-block", attrs= {'data-react-class': 'common/DateTime'})

                if len(deadline_element) > 1:
                    deadline = deadline_element[1]
                    deadline_json = deadline.get('data-react-props') if deadline else None
                    try:
                        #Parse JSON string if JSON is valid
                        deadline_data = json.loads(deadline_json)
                        deadline_string = deadline_data.get('value')
                        deadline_string, deadline_time = deadline_string.split('T')
                        deadline_date = datetime.strptime(deadline_string, '%Y-%m-%d').strftime('%A %B %d, %Y')
                        deadline_time = deadline_time[:5]

                    except json.JSONDecodeError:
                        print(f"Error parsing JSON for the deadline in project: {project_name}")
                else:
                    deadline_date = "Not Available"
                    deadline_time = None
                        
                # Create project dictionary entry with extracted information
                task_name = f"task-{len(projects)}"

                
                # Add project to dictionary
                projects[task_name] = {
                'progress': progress,
                'name': project_name,
                'link': f"https://intranet.alxswe.com{project_link}",
                'start_date': start_date,
                'start_time': start_time,
                'deadline_date': deadline_date,
                'deadline_time': deadline_time
                }
            projects['Active Projects'] = len(all_projects)
        
        else:
            projects['Active Projects'] = 0

        # Return dictionary of projects data
        return projects


def main():
    projects = fetch_projects()
    return projects


if __name__ == "__main__":
    main()
