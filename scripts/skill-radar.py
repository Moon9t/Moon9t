import requests, os, re

USERNAME = "Moon9t"
TOKEN = os.getenv("GITHUB_TOKEN", None)
headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

# categories mapping
categories = {
    "AI/ML": ["python", "pytorch", "tensorflow", "opencv"],
    "Backend": ["node", "express", "django", "go"],
    "Security": ["pentest", "kali", "security", "crypto"],
    "Frontend": ["react", "reactnative", "flutter"],
    "Databases": ["postgres", "mysql", "mongodb", "sqlite"],
    "DevOps": ["docker", "aws", "linux", "bash"]
}

scores = {k: 0 for k in categories}

# fetch repos
repos = requests.get(f"https://api.github.com/users/{USERNAME}/repos", headers=headers).json()

for repo in repos:
    lang_url = repo.get("languages_url")
    if not lang_url: continue
    langs = requests.get(lang_url, headers=headers).json()
    for lang in langs.keys():
        for cat, keys in categories.items():
            if any(re.search(k, lang.lower()) for k in keys):
                scores[cat] += langs[lang]

# normalize to 0–100
max_val = max(scores.values()) or 1
for k in scores:
    scores[k] = int(scores[k] / max_val * 100)

# generate quickchart URL
labels = list(scores.keys())
data = list(scores.values())
chart_url = f"https://quickchart.io/chart?c={{type:'radar',data:{{labels:{labels},datasets:[{{label:'Skill Radar',data:{data},backgroundColor:'rgba(56,189,165,0.2)',borderColor:'#38BDA5',pointBackgroundColor:'#38BDA5'}}]}},options:{{scales:{{r:{{angleLines:{{color:'#333'}},grid:{{color:'#444'}},pointLabels:{{color:'#38BDA5'}}}}}},plugins:{{legend:{{labels:{{color:'#38BDA5'}}}}}}}}}}"

# update README
with open("README.md", "r") as f:
    content = f.read()

new_line = f'<p align="center"><img src="{chart_url}" width="500"/></p>'
updated = re.sub(r'(<p align="center"><img src="https://quickchart.io/chart\?c=.*?</p>)', new_line, content, flags=re.DOTALL)

with open("README.md", "w") as f:
    f.write(updated)

