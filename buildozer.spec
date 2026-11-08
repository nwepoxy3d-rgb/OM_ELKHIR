[app]

title = OM EL KHIR
package.name = omelkhir
package.domain = org.omelkhir

source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,webp,atlas
source.exclude_dirs = .git,.github,.buildozer,bin,__pycache__

version = 0.1.0

requirements = python3,kivy,plyer

orientation = portrait
fullscreen = 0

android.permissions = CAMERA
android.api = 35
android.minapi = 23
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
