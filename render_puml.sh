#!/bin/bash
# Рендер всех PlantUML-схем курса в PNG (200 DPI)
cd "$(dirname "$0")"
java -jar plantuml.jar -tpng -Sdpi=200 -o "$PWD/course/images" course/puml/*.puml
