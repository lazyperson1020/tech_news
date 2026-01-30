#!/bin/bash

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Setting up The Silicon Post Backend...${NC}\n"

# Navigate to backend
cd "$(dirname "$0")/backend"

# Create venv
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv venv

# Activate venv and install
echo -e "${YELLOW}Installing dependencies...${NC}"
. venv/bin/activate
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt

# Create .env
if [ ! -f ".env" ]; then
  echo -e "${YELLOW}Creating .env file...${NC}"
  cp .env.example .env
fi

# Migrations
echo -e "${YELLOW}Running migrations...${NC}"
python manage.py migrate

# Create superuser
echo -e "${GREEN}Backend setup complete!${NC}"
echo -e "${YELLOW}To create a superuser, run:${NC}"
echo -e "  cd backend && source venv/bin/activate && python manage.py createsuperuser"
echo -e "\n${YELLOW}To start the backend server:${NC}"
echo -e "  cd backend && source venv/bin/activate && python manage.py runserver"
