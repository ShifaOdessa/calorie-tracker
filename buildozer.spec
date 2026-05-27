[app]

# (str) Title of your application
title = Calorie Tracker

# (str) Package name
package.name = calorietracker

# (str) Package domain (needed for android packaging)
package.domain = org.shifaodessa

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
# Жестко фиксируем стабильную версию Kivy для корректной сборки с NDK 25b
requirements = python3==3.11.9,kivy==2.3.0

# (str) Supported orientations (valid options are: landscape, portrait, all)
orientation = portrait

# =============================================================================
# Android specific configurations
# =============================================================================

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) If True, then skip trying to update the Android sdk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) The Android architecturalis to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a, armeabi-v7a

# (bool) Use allow backup
android.allow_backup = True

# =============================================================================
# Buildozer configurations
# =============================================================================

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0
