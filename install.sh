#! /bin/bash

SUBLIME_DIR=~/Library/Application\ Support/Sublime\ Text\ 3/Packages/
SUBLIME2_DIR=~/Library/Application\ Support/Sublime\ Text\ 2/Packages/

mkdir -p "$SUBLIME2_DIR/Lightning"
mkdir -p "$SUBLIME_DIR/Lightning"

cp -r "HTML.sublime-settings" "$SUBLIME2_DIR/Lightning"
cp -r "lightning.sublime-build" "$SUBLIME2_DIR/Lightning"
cp -r "lightning.sublime-keymap" "$SUBLIME2_DIR/Lightning"
cp -r "lightningsave.py" "$SUBLIME2_DIR/Lightning"
cp -r Side\ Bar.sublime-menu "$SUBLIME2_DIR/Lightning"
cp -r "README.md" "$SUBLIME2_DIR/Lightning"

cp -r "HTML.sublime-settings" "$SUBLIME_DIR/Lightning"
cp -r "lightning.sublime-build" "$SUBLIME_DIR/Lightning"
cp -r "lightning.sublime-keymap" "$SUBLIME_DIR/Lightning"
cp -r "lightningsave.py" "$SUBLIME_DIR/Lightning"
cp -r Side\ Bar.sublime-menu "$SUBLIME_DIR/Lightning"
cp -r "README.md" "$SUBLIME_DIR/Lightning"

echo "Lightning Sublime Plugin install finished"