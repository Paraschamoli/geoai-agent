# 🌐 GEO AI Agent

<p align="center">
  <img src="https://raw.githubusercontent.com/getbindu/create-bindu-agent/refs/heads/main/assets/light.svg" alt="bindu Logo" width="200">
</p>

<h1 align="center">GEO AI Agent</h1>

<p align="center">
  <strong>AI-powered content optimization and SEO analysis agent</strong>
</p>

<p align="center">
  <a href="https://github.com/Paraschamoli/geoai-agent/actions/workflows/main.yml?query=branch%3Amain">
    <img src="https://img.shields.io/github/actions/workflow/status/Paraschamoli/geoai-agent/main.yml?branch=main" alt="Build status">
  </a>
  <a href="https://img.shields.io/github/license/Paraschamoli/geoai-agent">
    <img src="https://img.shields.io/github/license/Paraschamoli/geoai-agent" alt="License">
  </a>
</p>

---

## 📖 Overview

GEO AI Agent is a comprehensive content optimization and SEO analysis tool built on the [Bindu Agent Framework](https://github.com/getbindu/bindu). It performs a sophisticated 6-agent workflow to analyze web content and provide actionable optimization recommendations.

**Key Capabilities:**
- � **Title Extraction** - Automatically extracts main titles from web pages
- 🔍 **Query Fan-Out Research** - Performs comprehensive web searches and discovers related queries
- 🎯 **Main Query Extraction** - Identifies core search queries for SEO optimization
- 🤖 **AI Overview Retrieval** - Fetches Google AI overviews and generates fallback content
- � **Query Summarization** - Creates structured summaries of search findings
- ⚡ **Content Optimization** - Generates comparison reports with actionable recommendations

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager
- API keys for OpenRouter and SERP

### Installation

```bash
# Clone the repository
git clone https://github.com/Paraschamoli/geoai-agent.git
cd geoai-agent

# Create virtual environment
uv venv --python 3.12.9
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync

# Configure environment
cp .env.example .env
```

### Configuration

Edit `.env` and add your API keys:

| Key | Get It From | Required |
|-----|-------------|----------|
| `OPENROUTER_API_KEY` | [OpenRouter](https://openrouter.ai/keys) | ✅ Yes |
| `SERP_API_KEY` | [SERP.dev](https://serper.dev/) | ✅ Yes |

### Run the Agent

```bash
# Start the agent
uv run python -m geoai_agent

# Agent will be available at http://localhost:3773
```

---

## 💡 Usage

### Example Queries

```bash
# Analyze a website for SEO optimization
"Analyze and optimize the webpage content for the following URL:

https://www.nike.com

Focus on:
- Extracting the page title
- Generating related Google search queries
- Fetching AI Overviews
- Comparing the page content with search results
- Providing actionable SEO and content optimization suggestions"
```

### Input Formats

**Plain Text:**
```
Analyze and optimize the webpage content for the following URL:

https://example.com

Focus on:
- Extracting the page title
- Generating related Google search queries
- Fetching AI Overviews
- Comparing the page content with search results
- Providing actionable SEO and content optimization suggestions
```

### Output Structure

The agent returns a comprehensive optimization report with:
- **Executive Summary**: Brief overview of current content status
- **Title Analysis**: Extracted title and SEO assessment
- **Query Fan-Out Research**: Comprehensive search findings
- **Main Query Extraction**: Core search query for optimization
- **AI Overview Analysis**: Google AI overview content
- **Query Fan-Out Summary**: Structured summary of findings
- **Content Optimization Comparison**: Detailed comparison table with action items

---

## 🔌 API Usage

The agent exposes a RESTful API when running. Default endpoint: `http://localhost:3773`

### Quick Start

For complete API documentation, request/response formats, and examples, visit:

📚 **[Bindu API Reference - Send Message to Agent](https://docs.getbindu.com/api-reference/all-the-tasks/send-message-to-agent)**

### Additional Resources

- 📖 [Full API Documentation](https://docs.getbindu.com/api-reference/all-the-tasks/send-message-to-agent)
- 📦 [Postman Collections](https://github.com/GetBindu/Bindu/tree/main/postman/collections)
- 🔧 [API Reference](https://docs.getbindu.com)

---

## 🎯 Skills

### GEO AI Content Optimizer (v1.0.0)

**Primary Capability:**
- Comprehensive web content analysis and SEO optimization
- 6-agent workflow for detailed content optimization
- AI-powered comparison reports with actionable recommendations

**Features:**
- Automatic title extraction from web pages
- Comprehensive query fan-out research
- Google AI overview retrieval and analysis
- Structured content summarization
- Detailed comparison tables
- Prioritized action items for SEO improvement

**Best Used For:**
- Website SEO optimization
- Content gap analysis
- Competitive research
- AI overview targeting
- Search visibility improvement

**Not Suitable For:**
- Real-time monitoring (analysis is static)
- Technical SEO audits (focuses on content)
- Link building strategies

**Performance:**
- Average processing time: ~30-60 seconds
- Max concurrent requests: 10
- Memory per request: ~500MB

---

## 🛠️ Development

### Project Structure

```
geoai-agent/
├── geoai_agent/
│   ├── skills/
│   │   └── geo-ai/
│   │       ├── skill.yaml          # Skill configuration
│   │       └── __init__.py
│   ├── __init__.py
│   ├── main.py                     # Agent entry point
│   └── agent_config.json           # Agent configuration
├── tests/
│   └── test_main.py
├── .env.example
├── docker-compose.yml
├── Dockerfile.agent
└── pyproject.toml
```

### Running Tests

```bash
make test              # Run all tests
make test-cov          # With coverage report
```

### Code Quality

```bash
make format            # Format code with ruff
make lint              # Run linters
make check             # Format + lint + test
```

### Pre-commit Hooks

```bash
# Install pre-commit hooks
uv run pre-commit install

# Run manually
uv run pre-commit run -a
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Powered by Bindu

Built with the [Bindu Agent Framework](https://github.com/getbindu/bindu)

**Why Bindu?**
- 🌐 **Internet of Agents**: A2A, AP2, X402 protocols for agent collaboration
- ⚡ **Zero-config setup**: From idea to production in minutes
- 🛠️ **Production-ready**: Built-in deployment, monitoring, and scaling

**Build Your Own Agent:**
```bash
uvx cookiecutter https://github.com/getbindu/create-bindu-agent.git
```

---

## 📚 Resources

- 📖 [Full Documentation](https://Paraschamoli.github.io/geoai-agent/)
- 💻 [GitHub Repository](https://github.com/Paraschamoli/geoai-agent/)
- 🐛 [Report Issues](https://github.com/Paraschamoli/geoai-agent/issues)
- 💬 [Join Discord](https://discord.gg/3w5zuYUuwt)
- 🌐 [Agent Directory](https://bindus.directory)
- 📚 [Bindu Documentation](https://docs.getbindu.com)

---

<p align="center">
  <strong>Built with 💛 by the team from Amsterdam 🌷</strong>
</p>

<p align="center">
  <a href="https://github.com/Paraschamoli/geoai-agent">⭐ Star this repo</a> •
  <a href="https://discord.gg/3w5zuYUuwt">💬 Join Discord</a> •
  <a href="https://bindus.directory">🌐 Agent Directory</a>
</p>
