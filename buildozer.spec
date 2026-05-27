[app]

# (str) Title of your application
title = Calorie Tracker

# (str) Package name
package.name = calorietracker

# (str) Package domain (needed for android packaging)
package.domain = org.alexshevchenko

# (str) Source code directory
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,openssl,requests,urllib3

# (str) Supported orientations (valid options are: landscape, portrait, all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# =============================================================================
# Android specific configuration
# =============================================================================

# (list) Permissions required by the app
# Включаем интернет (для ИИ) и доступ к хранилищу (для сохранения профиля)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk automatically
android.skip_update = False

# (bool) If True, then automatically accept SDK license agreements
android.accept_sdk_license = True

# (list) The Android architectures to build for
# Сборка под большинство современных телефонов
android.archs = arm64-v8a, armeabi-v7a

# (bool) Allow data backup
android.allow_backup = True

# (str) Format used to package the app for release mode (aab or apk)
android.release_artifact = apk

# (str) Format used to package the app for debug mode (apk or aar)
android.debug_artifact = apk


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1