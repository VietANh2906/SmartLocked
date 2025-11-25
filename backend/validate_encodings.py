import json

# Đường dẫn tới file users.json
USERS_FILE = "users.json"

# Đọc file
with open(USERS_FILE, "r", encoding="utf-8") as f:
    users = json.load(f)

valid_users = []
removed_users = []

for user in users:
    encoding = user.get("encoding")
    if encoding and len(encoding) == 128:
        valid_users.append(user)
    else:
        removed_users.append(user["name"])

# Ghi lại file users.json chỉ với các encoding chuẩn
with open(USERS_FILE, "w", encoding="utf-8") as f:
    json.dump(valid_users, f, indent=4, ensure_ascii=False)

if removed_users:
    print("Đã loại bỏ các user có encoding không chuẩn (không 128 chiều):")
    for name in removed_users:
        print("-", name)
else:
    print("Tất cả user đều có encoding chuẩn 128 chiều. Không có gì bị loại bỏ.")
