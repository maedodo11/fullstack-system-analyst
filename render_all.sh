#!/usr/bin/env bash
# Пересборка всех изображений курса
set -e
java -jar plantuml.jar -tpng -Sdpi=150 -o images_fullstack puml_fullstack/*.puml
java -jar plantuml.jar -tpng -Sdpi=200 -o course/images course/puml/*.puml
echo "OK: $(ls images_fullstack/*.png | wc -l) + $(ls course/images/*.png | wc -l) изображений"
