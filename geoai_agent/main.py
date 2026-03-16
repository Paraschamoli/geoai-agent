"""GEO AI Agent - AI Content Optimization Agent (Original Workflow)."""

# geoai_agent/main.py
import argparse
import asyncio
import json
import os
import sys
import traceback
from pathlib import Path
from textwrap import dedent
from typing import Any

from agno.agent import Agent
from agno.models.openrouter import OpenRouter
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.newspaper4k import Newspaper4kTools
from bindu.penguin.bindufy import bindufy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global agent instance
agent: Agent | None = None
_initialized = False
_init_lock = asyncio.Lock()


def load_config() -> dict:
    """Load agent configuration from project root."""
    # Try multiple possible locations for agent_config.json
    possible_paths = [
        Path(__file__).parent.parent / "agent_config.json",  # Project root
        Path(__file__).parent / "agent_config.json",  # Same directory as main.py
        Path.cwd() / "agent_config.json",  # Current working directory
    ]

    for config_path in possible_paths:
        if config_path.exists():
            try:
                with open(config_path) as f:
                    return json.load(f)
            except (PermissionError, json.JSONDecodeError) as e:
                print(f"⚠️  Error reading {config_path}: {type(e).__name__}")
                continue
            except Exception as e:
                print(f"⚠️  Unexpected error reading {config_path}: {type(e).__name__}")
                continue

    # If no config found or readable, create a minimal default
    print("⚠️  No agent_config.json found, using default configuration")
    return {
        "name": "geoai-agent",
        "description": "AI content optimization agent for web analysis",
        "version": "1.0.0",
        "deployment": {
            "url": "http://127.0.0.1:3773",
            "expose": True,
            "protocol_version": "1.0.0",
            "proxy_urls": ["127.0.0.1"],
            "cors_origins": ["*"],
        },
        "environment_variables": [
            {"key": "OPENROUTER_API_KEY", "description": "OpenRouter API key for LLM calls", "required": True},
            {"key": "SERP_API_KEY", "description": "SERP API key for web searches", "required": True},
        ],
    }


async def initialize_agent() -> None:
    """Initialize the GEO AI agent with proper model and tools."""
    global agent

    # Get API keys from environment
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    serp_api_key = os.getenv("SERP_API_KEY")
    model_name = os.getenv("MODEL", "meta-llama/llama-3.1-8b-instruct")

    # Model selection logic (supports OpenRouter)
    if not openrouter_api_key:
        # Define error message separately to avoid TRY003
        error_msg = (
            "OPENROUTER_API_KEY required. Set OPENROUTER_API_KEY environment variable.\n"
            "For OpenRouter: https://openrouter.ai/keys"
        )
        raise ValueError(error_msg)

    if not serp_api_key:
        error_msg = (
            "SERP_API_KEY required. Set SERP_API_KEY environment variable.\n"
            "Get your API key from: https://serper.dev/"
        )
        raise ValueError(error_msg)

    # Fix the model ID if it has the invalid prefix or invalid free tier
    if model_name:
        # Remove invalid prefix
        if model_name.startswith("openrouter/"):
            model_name = model_name.replace("openrouter/", "")
        
        # Replace invalid free model with a valid one
        if model_name == "meta-llama/llama-3.1-8b-instruct:free":
            model_name = "meta-llama/llama-3.1-8b-instruct"
            print(f"🔧 Fixed model ID to: {model_name}")
        elif model_name == "meta-llama/llama-3.1-8b-instruct":
            print(f"✅ Using valid model: {model_name}")
        else:
            print(f"🔧 Using model: {model_name}")
    else:
        model_name = "meta-llama/llama-3.1-8b-instruct"
        print(f"🔧 Using default model: {model_name}")

    # Initialize OpenRouter model
    model = OpenRouter(
        id=model_name,
        api_key=openrouter_api_key,
        cache_response=True,
        supports_native_structured_outputs=True,
    )
    print(f"✅ Using OpenRouter model: {model_name}")

    # Initialize tools
    search_tools = DuckDuckGoTools()
    newspaper_tools = Newspaper4kTools()

    # Create the GEO AI agent (single agent pattern like research-agent)
    agent = Agent(
        name="GEO AI Content Optimizer",
        model=model,
        tools=[search_tools, newspaper_tools],
        description=dedent("""\
            You are an expert AI content optimization specialist with deep expertise in:
            
            - Web content analysis and SEO optimization
            - Google Search algorithm understanding
            - AI Overview analysis and content gap identification
            - SERP (Search Engine Results Page) analysis
            - Content strategy and optimization recommendations
            - Competitive analysis and keyword research
            - User intent analysis and content matching
            
            You run a comprehensive 6-agent workflow for content optimization:
            1. **Title Scraper** - Extracts main title from URLs
            2. **Query Fan-Out Researcher** - Performs comprehensive web searches
            3. **Main Query Extractor** - Identifies core search queries
            4. **AI Overview Retriever** - Gets Google AI overviews
            5. **Query Fan-Out Summarizer** - Creates structured summaries
            6. **AI Content Optimizer** - Generates comparison reports and recommendations\
        """),
        instructions=dedent("""\
            You are an expert AI content optimization specialist that runs a comprehensive 6-agent workflow. 
            When given a URL, automatically execute the complete analysis process:

            **WORKFLOW EXECUTION:**

            **Phase 1: Title Scraping** 📝
            - Visit the URL and extract the main H1 heading or title
            - If no H1 tag exists, infer a title from the page content
            - Use newspaper tools to scrape and analyze the webpage
            - Output: Plain string title

            **Phase 2: Query Fan-Out Research** 🔍
            - Use the extracted title as search query
            - Perform comprehensive web searches using search tools
            - Gather multiple related queries, topics, and patterns
            - Output: Markdown search results

            **Phase 3: Main Query Extraction** 🎯
            - Analyze the query fan-out from previous phase
            - Extract the main, concise search query suitable for Google
            - Transform into Google-style keyphrase users would type
            - Output: Short, clear search query

            **Phase 4: AI Overview Retrieval** 🤖
            - Use the main query to perform SERP searches
            - Look for Google AI-generated overviews in search results
            - If no AI Overview found, generate one based on search results
            - Output: Markdown AI Overview

            **Phase 5: Query Fan-Out Summarization** 📊
            - Analyze the query fan-out content from Phase 2
            - Identify key themes, topics, and patterns
            - Generate comprehensive, well-structured summary
            - Output: Markdown summary

            **Phase 6: Content Optimization Comparison** ⚡
            - Compare the query fan-out summary with the Google AI Overview
            - Identify patterns, similarities, and differences between sources
            - Generate action items for topics appearing in both sources
            - Create comparison table with columns: Aspect, Query Fan-Out Summary, Google AI Overview, Similarities/Patterns, Differences
            - Output: Comprehensive optimization report in Markdown

            **EXECUTION REQUIREMENTS:**
            - Always follow the exact 6-phase sequence
            - Use the same output formats as specified in each phase
            - Include the summary table at the beginning of the comparison report
            - Focus on actionable SEO and content optimization recommendations
            - Structure all outputs professionally with clear sections

            **ERROR HANDLING:**
            - If any phase fails, continue with available information
            - Always provide fallback options when primary methods fail
            - Include clear error messages if specific tasks cannot be completed

            **QUALITY STANDARDS:**
            - Provide specific, actionable recommendations
            - Include examples and implementation guidance
            - Consider both technical SEO and content quality
            - Focus on aligning with Google's AI overview standards
            - Ensure all outputs are professional and well-structured\
        """),
        expected_output=dedent("""\
            # 🌐 Content Optimization Report for {url}

            ## 📊 Executive Summary
            {Brief overview of current content status and optimization potential}

            ## 📝 Title Analysis
            **Extracted Title:** {Main title from the URL}
            **Title Assessment:** {Analysis of title quality and SEO implications}

            ## 🔍 Query Fan-Out Research
            **Search Results:** {Comprehensive search findings and related queries}
            **Key Themes Identified:** {Main topics and patterns discovered}

            ## 🎯 Main Query Extraction
            **Core Search Query:** {Primary Google-style query extracted}
            **Query Refinement:** {Optimized search term for maximum relevance}

            ## 🤖 AI Overview Analysis
            **Google AI Overview:** {Retrieved or generated AI overview content}
            **Overview Assessment:** {Analysis of AI overview structure and key points}

            ## 📊 Query Fan-Out Summary
            **Structured Summary:** {Comprehensive summary of search findings}
            **Key Insights:** {Main takeaways from the query fan-out analysis}

            ## ⚡ Content Optimization Comparison

            ### Summary Table
            | Aspect | Query Fan-Out Summary | Google AI Overview | Similarities/Patterns | Differences |
            |--------|----------------------|-------------------|---------------------|-------------|
            | {Analysis rows comparing both sources} |

            ### Action Items
            **High Priority (Immediate Impact):**
            {Most critical improvements with highest ROI}

            **Medium Priority (Significant Improvement):**
            {Important enhancements for better performance}

            **Low Priority (Fine-tuning):**
            {Minor optimizations for incremental gains}

            ## 📈 Implementation Strategy
            **Phase 1 (Week 1-2):** {Immediate actions}
            **Phase 2 (Week 3-4):** {Secondary improvements}
            **Phase 3 (Month 2):** {Long-term optimizations}

            ## 🎯 Expected Outcomes
            **Search Visibility:** {Predicted improvements in rankings}
            **AI Overview Inclusion:** {Likelihood of appearing in AI overviews}
            **User Engagement:** {Expected impact on user metrics}

            ---
            *Analysis conducted by GEO AI Content Optimizer*
            *Generated: {current_date}*
            *Model: {model_name}*
        """),
        add_datetime_to_context=True,
        markdown=True,
    )
    print("✅ GEO AI Agent initialized")


async def run_agent(messages: list[dict[str, str]]) -> Any:
    """Run the agent with the given messages."""
    global agent
    if not agent:
        # Define error message separately to avoid TRY003
        error_msg = "Agent not initialized"
        raise RuntimeError(error_msg)

    # Run the agent and get response
    return await agent.arun(messages)  # type: ignore[invalid-await]


async def handler(messages: list[dict[str, str]]) -> Any:
    """Handle incoming agent messages with lazy initialization."""
    global _initialized

    # Lazy initialization on first call
    async with _init_lock:
        if not _initialized:
            print("🔧 Initializing Research Agent...")
            await initialize_agent()
            _initialized = True

    # Run the async agent
    result = await run_agent(messages)
    return result


async def cleanup() -> None:
    """Clean up any resources."""
    print("🧹 Cleaning up GEO AI Agent resources...")


def main():
    """Run the main entry point for the GEO AI Agent."""
    parser = argparse.ArgumentParser(description="Bindu GEO AI Agent")
    parser.add_argument(
        "--openrouter-api-key",
        type=str,
        default=os.getenv("OPENROUTER_API_KEY"),
        help="OpenRouter API key (env: OPENROUTER_API_KEY)",
    )
    parser.add_argument(
        "--serp-api-key",
        type=str,
        default=os.getenv("SERP_API_KEY"),
        help="SERP API key (env: SERP_API_KEY)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=os.getenv("MODEL", "meta-llama/llama-3.1-8b-instruct"),
        help="OpenRouter model ID (env: MODEL)",
    )
    parser.add_argument(
        "--config",
        type=str,
        help="Path to agent_config.json (optional)",
    )
    args = parser.parse_args()

    # Set environment variables if provided via CLI
    if args.openrouter_api_key:
        os.environ["OPENROUTER_API_KEY"] = args.openrouter_api_key
    if args.serp_api_key:
        os.environ["SERP_API_KEY"] = args.serp_api_key
    if args.model:
        os.environ["MODEL"] = args.model

    print("🤖 GEO AI Agent - AI Content Optimization (6-Agent Workflow)")
    print("🔍 Capabilities: Web scraping, Google search, AI overview analysis, content optimization")

    # Load configuration
    config = load_config()

    try:
        # Bindufy and start the agent server
        print("🚀 Starting Bindu GEO AI Agent server...")
        print(f"🌐 Server will run on: {config.get('deployment', {}).get('url', 'http://127.0.0.1:3773')}")
        bindufy(config, handler)
    except KeyboardInterrupt:
        print("\n🛑 GEO AI Agent stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Cleanup on exit
        asyncio.run(cleanup())


if __name__ == "__main__":
    main()
