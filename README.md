# Pilot-AI Marketing Agent

An AI-powered marketing automation solution using CrewAI and Google's Gemini model.

## Features

- Market Research Automation
- Content Calendar Generation
- Blog Post Creation
- SEO Optimization
- Social Media Strategy

## Tech Stack

- Backend: Python, FastAPI, CrewAI
- Frontend: Streamlit
- AI: Google Gemini Pro
- Deployment: Docker & Docker Compose

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/pilot-ai-marketing-agent.git
cd pilot-ai-marketing-agent
```

2. Create environment file:
```bash
cp .env.example .env
# Add your API keys to .env
```

3. Run with Docker:
```bash
docker-compose up
```

Access the application:
- Frontend: http://localhost:8501
- Backend API: http://localhost:8007

## Environment Variables

Required environment variables in `.env`:
- `GEMINI_API_KEY`: Your Google Gemini API key

## Docker Images

- Backend: `YOUR_DOCKER_USERNAME/pilot-ai-backend`
- Frontend: `YOUR_DOCKER_USERNAME/pilot-ai-frontend`

## License

MIT

## Contributing

Pull requests are welcome. For major changes, please open an issue first.