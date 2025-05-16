import zipfile
import os
import re


def extract_zip(zip_path):
    filename = os.path.basename(zip_path)

    filename = filename.lower().replace(" ", "").replace(".zip", "")

    output_dir = f"./data/{filename}"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(output_dir)

    return output_dir


def find_txt(path):
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".txt"):
                return os.path.join(root, file)
    return None


def parse_txt(arquivo_txt):
    pattern = re.compile(r"(\d{1,2}/\d{1,2}/\d{2}), (\d{2}:\d{2}) - (.*?): (.*)")

    parsed_data = []
    users_unique = set()

    with open(arquivo_txt, "r") as file:
        content = file.read()
        for line in content.splitlines():
            match = pattern.match(line)
            if match:
                date, time, user, message = match.groups()
                parsed_data.append(
                    {"date": date, "time": time, "user": user, "message": message}
                )
                users_unique.add(user)

    return parsed_data, list(users_unique)


def parse_whataspp(path):
    zip_output = extract_zip(path)

    ws_txt = find_txt(zip_output)

    ws_data, ws_users = parse_txt(ws_txt)

    return ws_data, ws_users
