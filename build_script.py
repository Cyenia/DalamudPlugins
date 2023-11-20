import os, sys, math, filecmp, shutil, json

if len(sys.argv) != 3:
    print(f"{os.path.basename(__file__)} (repository) (branch)\nExample: {os.path.basename(__file__)} 'goatcorp/DalamudPlugins' 'master'")
    exit(1)

repo = sys.argv[1]
branch = sys.argv[2]

new_json = []
updated = False
folder = "plugins"
new_file = 'new.json'
repo_file = 'pluginmaster.json'
raw = f"https://raw.githubusercontent.com/{repo}"

for name in os.listdir(folder):
    path = os.path.join(folder, name)
    if not os.path.isdir(path): continue

    file = os.path.join(path, name + ".json" )
    if not os.path.isfile(file): continue

    json_file = open(file, "r")
    file_data = json_file.read()
    json_file.close()
    if len(file_data) == 0: continue

    try:
        json_data = json.loads(file_data)
    except json.decoder.JSONDecodeError:
        continue

    json_data["LastUpdate"] = math.floor(os.path.getmtime(file))
    download_link = f"{raw}/{branch}/{folder}/{name}/latest.zip"
    json_data["DownloadLinkInstall"] = download_link
    json_data["DownloadLinkTesting"] = download_link
    json_data["DownloadLinkUpdate"] = download_link
    new_json.append(json_data)

with open(new_file, 'w', encoding='utf-8') as f:
    json.dump(new_json, f, ensure_ascii=False, indent=4)

if not os.path.isfile(repo_file):
    with open(repo_file, 'w'): pass

if not filecmp.cmp(repo_file, new_file):
    updated = True
    shutil.copy(new_file, repo_file)

os.remove(new_file)

print(f"new-files={updated}")
