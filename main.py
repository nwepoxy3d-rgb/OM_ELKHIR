name: Build_APK
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build_Android
        uses: ArtemSerebrenninkov/buildozer-action@v1
        with:
          command: buildozer android debug
          repository_root: .
