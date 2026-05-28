[app]

# (str) Title of your application
title = Calorie Tracker

# (str) Package name
package.name = calorietracker

# (str) Package domain (needed for android packaging)
package.domain = org.shifaodessa

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 1.0

# (list) Application requirements
# Оставляем только самое необходимое
requirements = python3==3.11.9,hostpython3==3.11.9,kivy==2.3.0

# (str) Supported orientations
orientation = portrait

# =============================================================================
# Python-for-android specific configurations
# =============================================================================

# Используем ветку develop, чтобы обойти баги с новыми версиями pip
p4a.branch = develop

# =============================================================================
# Android specific configurations
# =============================================================================

fullscreen = 1
android.permissions = INTERNET
android.api = 34
android.minapi = 21
android.ndk = 26b
android.skip_update = False
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

# Исключаем проблемные графические библиотеки, которые вызывают ошибки сборки
p4a.local_recipes = 

# =============================================================================
# Buildozer configurations
# =============================================================================

[buildozer]

# Устанавливаем уровень 2, чтобы видеть все детали сборки
log_level = 2
warn_on_root = 0
