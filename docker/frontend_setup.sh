#!/bin/sh
cd frontend/
npm install
# yarn install
# yarn serve --host 0.0.0.0
cd src/
yarn build --watch --mode=production