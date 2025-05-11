import requests
from bs4 import BeautifulSoup as bs

github_user = input("Enter your GitHub username: ")
url = 'https://github.com/'+github_user
r = requests.get(url)

if r.status_code == 200:  # Check if the request was successful
    soup = bs(r.content, 'html.parser')
    profile_image_tag = soup.find('img', {'class': 'avatar'})
    
    if profile_image_tag:  # Check if the image tag was found
        profile_image = profile_image_tag['src']
        print("Profile Image URL: ", profile_image)
    else:
        print("Profile image not found for the given username.")
else:
    print(f"Failed to fetch the page. Status code: {r.status_code}")