# Đặt script này ở folder gốc smart-locker

# 1️⃣ Định nghĩa folder
$backend = "backend"
$app = Join-Path $backend "app"

# 2️⃣ Tạo folder app nếu chưa có
if (!(Test-Path $app)) {
    New-Item -ItemType Directory -Path $app
    Write-Host "Tạo folder: $app"
}

# 3️⃣ Tạo __init__.py nếu chưa có
foreach ($folder in @($backend, $app)) {
    $init = Join-Path $folder "__init__.py"
    if (!(Test-Path $init)) {
        New-Item -ItemType File -Path $init
        Write-Host "Tạo file __init__.py tại $folder"
    }
}

# 4️⃣ Di chuyển file main.py và auth.py vào backend/
$files_backend = @("main.py","auth.py")
foreach ($f in $files_backend) {
    $src = Get-ChildItem -Path . -Recurse -Filter $f | Where-Object {$_.FullName -notlike "*\venv\*"} | Select-Object -First 1
    if ($src) {
        Move-Item -Path $src.FullName -Destination $backend -Force
        Write-Host "Di chuyển $f vào $backend"
    }
}

# 5️⃣ Di chuyển monggo.py vào backend/app/
$src_monggo = Get-ChildItem -Path . -Recurse -Filter "monggo.py" | Where-Object {$_.FullName -notlike "*\venv\*"} | Select-Object -First 1
if ($src_monggo) {
    Move-Item -Path $src_monggo.FullName -Destination $app -Force
    Write-Host "Di chuyển monggo.py vào $app"
}

Write-Host "✅ Hoàn tất sắp xếp file!"
