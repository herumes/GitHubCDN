import requests
import base64
import random
from urllib.parse import quote

class GithubCDN:
    def __init__(self, owner: str, repo: str, token: str):
        self.owner = owner
        self.repo = repo
        self.token = token
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}"
        self.raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/main"

    def upload_file(self, file_path: str, file_name: str, commit_message: str = "Uploaded via GitHubCDN", directory: str = "") -> int:
        with open(file_path, "rb") as file:
            file_data = base64.b64encode(file.read()).decode()
        
        upload_url = f"{self.base_url}/contents/{directory}/{file_name}" if directory else f"{self.base_url}/contents/{file_name}"
        headers = {
            'X-GitHub-Api-Version': '2022-11-28',
            'Authorization': f"Bearer {self.token}",
            'Accept': 'application/vnd.github+json'
        }
        payload = {
            'committer': {'name': "ShuttleAI", 'email': "noreply@shuttleai.app"},
            'message': commit_message,
            'content': file_data
        }
        response = requests.put(upload_url, json=payload, headers=headers)
        uploaded_file = f"{self.raw_url}/{directory}/{file_name}" if directory else f"{self.raw_url}/{file_name}"
        return uploaded_file if response.status_code == 201 else response.json()

    def download_file(self, file_name: str, directory: str = "", output_file: str = None) -> str:
        download_url = f"{self.raw_url}/{directory}/{file_name}" if directory else f"{self.raw_url}/{file_name}"
        response = requests.get(download_url, stream=True)
        
        if output_file is None:
            output_file = file_name.replace(".", f"_{random.randint(0, 1000)}.")
        
        with open(output_file, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        return output_file

if __name__ == "__main__":
    GITHUB_REPO_OWNER = "YOUR_GITHUB_USERNAME"
    GITHUB_REPO_NAME = "YOUR_GITHUB_REPO_NAME"
    TOKEN = "YOUR_GITHUB_TOKEN"

    # Example Usage
    github_cdn = GithubCDN(GITHUB_REPO_OWNER, GITHUB_REPO_NAME, TOKEN)

    upload_file = github_cdn.upload_file('image.png', quote('A spider thing3.png'), "Uploaded via API", "images")
    print(f"File Upload Response: {upload_file}")

    downloaded_file = github_cdn.download_file('spiderman.png', output_file="spiderman_downloaded.png")
    print(f"File downloaded as {downloaded_file}")
