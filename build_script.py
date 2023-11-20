import os, sys, math, filecmp, shutil, json

if len(sys.argv) != 3:
    print(f"{os.path.basename(__file__)} (repository) (branch)\nExample: {os.path.basename(__file__)} 'goatcorp/DalamudPlugins' 'master'")
    exit(1)

repo = sys.argv[1]
branch = sys.argv[2]

new_json = []
updated = False
old_file = None
folder = "plugins"
new_file = 'new.json'
repo_file = 'pluginmaster.json'
raw = f"https://raw.githubusercontent.com/{repo}"

def get_file_data(_file: str):
    _json_file = open(_file, "r")
    _file_data = _json_file.read()
    _json_file.close()
    return _file_data

if os.path.isfile(repo_file):
    file_data = get_file_data(repo_file)

    try:
        old_file = json.loads(file_data)
    except json.decoder.JSONDecodeError:
        pass

for name in os.listdir(folder):
    path = os.path.join(folder, name)
    if not os.path.isdir(path): continue

    file = os.path.join(path, name + ".json" )
    if not os.path.isfile(file): continue

    file_data = get_file_data(file)
    if len(file_data) == 0: continue

    try:
        json_data = json.loads(file_data)
    except json.decoder.JSONDecodeError:
        continue

    json_data["LastUpdate"] = math.floor(os.path.getmtime(file))

    for plugin in old_file:
        if plugin["Name"] == json_data["Name"]:
            if plugin["AssemblyVersion"] == json_data["AssemblyVersion"]:
                json_data["LastUpdate"] = plugin["LastUpdate"]
            break

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

print(f"new-files={'true' if updated else 'false'}")
