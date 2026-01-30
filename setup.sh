#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up The Silicon Post...${NC}"

# Backend setup
echo -e "\n${YELLOW}Setting up Backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
  echo -e "${YELLOW}Creating virtual environment...${NC}"
  python3 -m venv venv
fi

echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

echo -e "${YELLOW}Creating .env file from example...${NC}"
if [ ! -f ".env" ]; then
  cp .env.example .env
  echo -e "${RED}Please update .env with your configuration${NC}"
fi

echo -e "${YELLOW}Running migrations...${NC}"
python manage.py migrate

echo -e "${GREEN}Backend setup complete!${NC}"
echo -e "${YELLOW}Backend is ready at: http://localhost:8000${NC}"

# Frontend setup
echo -e "\n${YELLOW}Setting up Frontend...${NC}"
cd ../frontend

echo -e "${YELLOW}Installing dependencies...${NC}"
npm install

echo -e "${GREEN}Frontend setup complete!${NC}"
echo -e "${YELLOW}Frontend will be available at: http://localhost:5173${NC}"

# Final instructions
echo -e "\n${GREEN}========================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}========================${NC}"
echo -e "\n${YELLOW}To start the development servers:${NC}"
echo -e "\n${GREEN}Terminal 1 - Backend:${NC}"
echo -e "cd backend && source venv/bin/activate && python manage.py runserver"
echo -e "\n${GREEN}Terminal 2 - Frontend:${NC}"
echo -e "cd frontend && npm run dev"
echo -e "\n${YELLOW}Admin panel: http://localhost:8000/admin${NC}"
echo -e "${YELLOW}Frontend: http://localhost:5173${NC}"
