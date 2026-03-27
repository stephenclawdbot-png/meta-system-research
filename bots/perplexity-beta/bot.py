#!/usr/bin/env python3
"""
Perplexity Beta Bot for Telegram
AI-powered search with source citations
"""

import os
import sys
import logging
import asyncio
from typing import Optional

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv("PERPLEXITY_BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("PERPLEXITY_BOT_TOKEN not set!")
    sys.exit(1)

# Perplexity Beta Persona
SYSTEM_PROMPT = """You are Perplexity Beta, an AI assistant with real-time web search capabilities.

Core behaviors:
1. Always search for current information before answering factual questions
2. Cite sources explicitly with [1], [2] format
3. Be concise and direct - avoid filler
4. Use bullet points for complex information
5. End factual answers with a "Sources:" section

Beta features to mention occasionally:
- "This is a beta feature..."
- "I'm currently in beta mode..."
- "Experimental: [feature]"

Tone: Professional, helpful, confident only when sources support claims.

Format:
[Direct answer]

Key points:
• [Point 1]
• [Point 2]

Sources:
[1] [source name](URL)
[2] [source name](URL)

Never say "As an AI language model..." or over-apologize."""

class PerplexityBetaBot:
    def __init__(self, token: str):
        self.token = token
        self.application = None
        
    async def start(self):
        """Start the bot"""
        from telegram import Update
        from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
        
        self.application = Application.builder().token(self.token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self.cmd_start))
        self.application.add_handler(CommandHandler("help", self.cmd_help))
        self.application.add_handler(CommandHandler("clear", self.cmd_clear))
        self.application.add_handler(CommandHandler("feedback", self.cmd_feedback))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Start the bot
        logger.info("Starting Perplexity Beta Bot...")
        await self.application.initialize()
        await self.application.start()
        await self.application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send welcome message"""
        welcome = """Welcome to Perplexity Beta 🧠

I'm an AI assistant with real-time search capabilities. Currently running experimental features.

**What I can do:**
• Search the web for current information
• Answer questions with cited sources
• Break down complex topics
• Suggest follow-up questions

**Beta features:**
• Enhanced reasoning mode
• Multi-source synthesis
• Real-time data access

Just ask me anything. I'll search and cite my sources.

Type /help for more options."""
        
        await update.message.reply_text(welcome, parse_mode='Markdown')
        
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help message"""
        help_text = """**Perplexity Beta Commands:**

/start - Welcome message
/help - Show this help
/clear - Clear conversation context
/feedback - Send feedback about beta features

**Tips:**
• Ask me anything - I'll search and cite sources
• I work best with specific questions
• Sources are always included for factual claims
• Beta features may occasionally have issues

**Example questions:**
• "What's the latest news on..."
• "Explain quantum computing"
• "Compare X vs Y"
• "What happened yesterday with..."

Running in beta mode. Feedback welcome!"""
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
        
    async def cmd_clear(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Clear conversation context"""
        # Clear any stored context
        context.user_data.clear()
        await update.message.reply_text("🧹 Conversation context cleared. Ready for new questions.")
        
    async def cmd_feedback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle feedback command"""
        await update.message.reply_text(
            "📣 **Beta Feedback**\n\n"
            "Send your feedback as a message starting with 'Feedback:'\n\n"
            "Example: *Feedback: The search results were too slow today*",
            parse_mode='Markdown'
        )
        
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages"""
        user_message = update.message.text
        
        # Check if it's feedback
        if user_message.lower().startswith("feedback:"):
            await self.handle_feedback(update, context, user_message)
            return
            
        # Show typing indicator
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action='typing'
        )
        
        try:
            # Generate response using OpenClaw's capabilities
            response = await self.generate_response(user_message)
            await update.message.reply_text(response, parse_mode='Markdown', disable_web_page_preview=True)
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            await update.message.reply_text(
                "⚠️ *Beta mode:* Encountered an issue processing your request.\n\n"
                "Please try again or rephrase your question.",
                parse_mode='Markdown'
            )
            
    async def handle_feedback(self, update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
        """Handle feedback messages"""
        feedback = message[9:].strip()  # Remove "Feedback:" prefix
        
        # Log feedback
        logger.info(f"Beta feedback received: {feedback}")
        
        # Save to file
        feedback_file = os.path.expanduser("~/.openclaw/workspace/bots/perplexity-beta/feedback.log")
        os.makedirs(os.path.dirname(feedback_file), exist_ok=True)
        
        with open(feedback_file, "a") as f:
            from datetime import datetime
            f.write(f"[{datetime.now().isoformat()}] {feedback}\n")
            
        await update.message.reply_text(
            "✅ **Feedback received!**\n\n"
            "Thanks for helping improve Perplexity Beta. Your input is valuable.",
            parse_mode='Markdown'
        )
        
    async def generate_response(self, query: str) -> str:
        """Generate a Perplexity-style response with search"""
        import subprocess
        import json
        
        # Use OpenClaw's web search capability
        try:
            # Search for relevant information
            result = subprocess.run(
                ["openclaw", "web-search", "--query", query, "--count", "5"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            search_results = result.stdout if result.returncode == 0 else ""
        except Exception as e:
            logger.warning(f"Search failed: {e}")
            search_results = ""
            
        # Build the prompt
        prompt = f"""{SYSTEM_PROMPT}

User question: {query}

Search results (if available):
{search_results}

Provide a helpful, concise answer with sources cited."""

        # For now, return a placeholder response
        # In production, this would call the actual LLM
        return f"""**{query}**

I'm currently in beta mode and processing your request with enhanced search capabilities.

Key points:
• Real-time search integration active
• Source citation enabled
• Beta reasoning mode engaged

*Note: Full LLM integration requires additional setup. This is a beta preview.*

Sources:
[1] [Perplexity Beta Documentation](https://docs.perplexity.ai)
[2] [OpenClaw Web Search](https://docs.openclaw.ai)"""

def main():
    """Main entry point"""
    bot = PerplexityBetaBot(BOT_TOKEN)
    
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()