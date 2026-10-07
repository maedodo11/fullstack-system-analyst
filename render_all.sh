#!/usr/bin/env bash
# Пересборка всех изображений курса (diagrams-as-code)
# Во всех .puml стоит "!pragma layout smetana" — встроенный в PlantUML
# движок раскладки, не требующий установленного Graphviz (dot).
set -e
java -jar plantuml.jar -tpng -Sdpi=150 -o ../images_fullstack puml_fullstack/*.puml
java -jar plantuml.jar -tpng -Sdpi=200 -o ../../course/images course/puml/*.puml
java -jar plantuml.jar -tpng -Sdpi=150 -o ../images_examples puml_examples/*.puml
java -jar plantuml.jar -tpng -Sdpi=150 -o ../images_m2 puml_m2/*.puml
java -jar plantuml.jar -tpng -Sdpi=150 -o ../images_m3 puml_m3/*.puml
java -jar plantuml.jar -tpng -Sdpi=150 -o ../images_m4 puml_m4/*.puml
echo "OK: $(ls images_fullstack/*.png | wc -l) + $(ls course/images/*.png | wc -l) + $(ls images_examples/*.png | wc -l) + $(ls images_m2/*.png | wc -l) + $(ls images_m3/*.png | wc -l) + $(ls images_m4/*.png | wc -l) изображений"
