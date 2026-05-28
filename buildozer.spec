[app]

# (str) Title of your application
title = Calorie Tracker

# (str) Package name
package.name = calorietracker

# (str) Package domain
package.domain = org.shifaodessa

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 1.0

# (list) Application requirements
# Фиксируем версии для стабильной сборки в облаке
requirements = python3==3.11.9,hostpython3==3.11.9,kivy==2.3.0

# (str) Supported orientations
orientation = portrait

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

# Отключаем локальные рецепты, чтобы buildozer не пытался компилировать 
# конфликтующие графические библиотеки (ThorVG и др.)
p4a.local_recipes = 

# =============================================================================
# Buildozer configurations
# =============================================================================

[buildozer]

# Уровень логирования 2 дает нам максимум информации в логах
log_level = 2
warn_on_root = 0
