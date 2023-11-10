#!/bin/bash

# check if nvm is installed
if [ -z "$(command -v nvm)" ]; then
    echo "NVM is not installed. Installing NVM..."
    # install nvm
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    # Load NVM into the current shell session
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
fi

# check if node is installed
if [ -z "$(command -v node)" ]; then
    echo "Node.js is not installed. Installing Node.js using NVM..."
    # Install the latest lts version of node
    nvm install --lts
fi

# check if npm is installed
if [ -z "$(command -v npm)" ]; then
    echo "npm is not installed. Please install npm manually."
    exit 1
fi

# update npm to the latest version
npm install -g npm@latest

# navigate to your project directory
project_directory="../frontend/"  # adjust the path accordingly

cd "$project_directory" || exit

# install project dependencies
npm install

# run the build
npm run build