# Contributing to ResearchMind AI

Thank you for your interest in contributing to **ResearchMind AI**! We welcome contributions from developers, researchers, designers, and documentation writers.

## Getting Started

1. **Fork the Repository** on GitHub: [ng945217-byte/Research-Mind](https://github.com/ng945217-byte/Research-Mind)
2. **Clone your fork**:
   ```bash
   git clone https://github.com/<your-username>/Research-Mind.git
   cd Research-Mind
   ```
3. **Create a new branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Environment Setup

### Backend Setup (Python 3.10+)
```bash
cd backend
python -m venv venv

# Windows
.\venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Edit .env and supply your API keys

# Start backend server
uvicorn main:app --port 8001 --reload
```

### Frontend Setup (Node.js 18+)
```bash
cd frontend
npm install
npm run dev
```

## Guidelines

- Follow existing code conventions and formatting.
- Ensure your changes do not break existing backend endpoints or frontend components.
- Keep commits clear, descriptive, and atomic.
- Submit a Pull Request detailing the changes made, motivation, and tests performed.

## Reporting Issues

If you discover a bug or have a suggestion, please open an issue using the relevant GitHub issue template.
