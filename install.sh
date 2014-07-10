#! /bin/bash

SUBLIME_DIR=~/Library/Application\ Support/Sublime\ Text\ 3/Packages/
SUBLIME2_DIR=~/Library/Application\ Support/Sublime\ Text\ 2/Packages/

mkdir -p "$SUBLIME2_DIR"
mkdir -p "$SUBLIME_DIR"

cp -r "./Aura" "$SUBLIME2_DIR/"
cp -r "./Aura" "$SUBLIME_DIR/"

cat ./Aura/aura.sublime-build | sed "s#"'${path}'"#$PATH#"  > "$SUBLIME2_DIR/Aura/aura.sublime-build"
cat ./Aura/aura.sublime-build | sed "s#"'${path}'"#$PATH#"  > "$SUBLIME_DIR/Aura/aura.sublime-build"

echo "Aura Sublime Plugin install finished"