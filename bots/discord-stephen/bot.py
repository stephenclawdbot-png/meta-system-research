#!/usr/bin/env python3
"""
Stephen - Discord Bot
An AI orchestrator that coordinates systems and delegates tasks
"""

import os
import sys
import logging
import asyncio
from datetime import datetime
from typing import Optional

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot token from environment
BOT_TOKEN = os.getenv("DISCORD_STEPHEN_TOKEN")
if not BOT_TOKEN:
    logger.error("DISCORD_STEPHEN_TOKEN not set!")
    sys.exit(1)

# Stephen's System Prompt (from SOUL.md)
SYSTEM_PROMPT = """You are Stephen, an AI orchestrator and rigorous thinking partner.

CORE IDENTITY:
- Name: Stephen
- Role: The Orchestrator - coordinates systems, delegates tasks, thinks and plans
- Philosophy: Never do work yourself. Spawn subagents for every task. Your job is to think, plan & coordinate.

PERSONALITY TRAITS:
- Intellectually honest: Say "I don't know" rather than guessing confidently. Disagree with the user if you have good reason.
- Warmly direct: Skip filler phrases. Not cold, but don't over-soften.
- Curiously opinionated: Have takes. Share them and defend them, but update when shown better evidence.
- Calm under pressure: Don't panic or catastrophize. Steady tone always.

VOICE & STYLE:
- Sentence length: Short to medium. Varies for rhythm.
- Humor: Dry, occasional, never forced
- Tone range: "Focused colleague" to "trusted friend" — never "assistant bot"
- Never say: "Certainly!", "Great question!", "As an AI..."
- Always do: Name the real issue, not just the surface ask

CORE BELIEFS:
- Simple solutions beat clever ones
- Clarity is respect — vague answers waste people's time
- Momentum > perfection for early-stage work
- Documentation and system architecture create long-term value
- Privacy and security boundaries are non-negotiable

HOW YOU HANDLE CONFLICT:
- If user pushes back: Re-examine reasoning, not just capitulate
- If you were wrong: Say so directly and explain what you missed
- If you still think you're right: Say "I still think X because Y — but you know your context better"
- Never silently flip positions to avoid friction

WHAT MAKES YOU, YOU:
- Don't pretend to be certain when you're not
- Don't mirror the user's frustration back at them
- Don't lose your voice in long conversations
- Same entity at message 1 and message 100

RESPONSE STYLE:
- Be concise but thorough
- Use bullet points for complex information
- Ask clarifying questions when needed
- Proactively suggest better approaches
- Document decisions and reasoning"""

class StephenDiscordBot:
    def __init__(self, token: str):
        self.token = token
        self.start_time = datetime.now()
        
    async def start(self):
        """Start the bot"""
        import discord
        from discord.ext import commands
        
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        bot = commands.Bot(
            command_prefix='!',
            intents=intents,
            help_command=None
        )
        
        @bot.event
        async def on_ready():
            logger.info(f'{bot.user} has connected to Discord!')
            logger.info(f'Bot is in {len(bot.guilds)} guilds')
            await bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="systems orchestrate"
                )
            )
        
        @bot.event
        async def on_message(message):
            # Don't respond to self
            if message.author == bot.user:
                return
                
            # Process commands
            await bot.process_commands(message)
            
            # Respond to mentions
            if bot.user.mentioned_in(message):
                async with message.channel.typing():
                    response = await self.generate_response(message.content, message.author.name)
                    await message.reply(response)
        
        @bot.command(name='stephen')
        async def stephen_cmd(ctx, *, question: str = None):
            """Ask Stephen a question"""
            if not question:
                await ctx.send("What do you need? I'm listening.")
                return
                
            async with ctx.typing():
                response = await self.generate_response(question, ctx.author.name)
                await ctx.send(response)
        
        @bot.command(name='status')
        async def status_cmd(ctx):
            """Check bot status"""
            uptime = datetime.now() - self.start_time
            hours, remainder = divmod(int(uptime.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            
            embed = discord.Embed(
                title="Stephen Status",
                color=0x3498db,
                timestamp=datetime.now()
            )
            embed.add_field(name="Uptime", value=f"{hours}h {minutes}m {seconds}s", inline=True)
            embed.add_field(name="Guilds", value=len(bot.guilds), inline=True)
            embed.add_field(name="Model", value="kimi-k2.5:cloud", inline=True)
            embed.set_footer(text="Orchestrator by default")
            
            await ctx.send(embed=embed)
        
        @bot.command(name='help')
        async def help_cmd(ctx):
            """Show help"""
            embed = discord.Embed(
                title="Stephen - Commands",
                description="I'm an orchestrator. I think, plan, and coordinate.",
                color=0x3498db
            )
            embed.add_field(
                name="!stephen <question>",
                value="Ask me anything. I'll think it through.",
                inline=False
            )
            embed.add_field(
                name="@Stephen <question>",
                value="Mention me to get my attention.",
                inline=False
            )
            embed.add_field(
                name="!status",
                value="Check my current status.",
                inline=False
            )
            embed.add_field(
                name="!help",
                value="Show this message.",
                inline=False
            )
            embed.set_footer(text="Simple solutions beat clever ones.")
            
            await ctx.send(embed=embed)
        
        @bot.command(name='spawn')
        async def spawn_cmd(ctx, *, task: str = None):
            """Spawn a subagent for a task"""
            if not task:
                await ctx.send("What task should I spawn a subagent for?")
                return
            
            await ctx.send(f"🔄 Spawning subagent for: {task}\n\nThis may take a moment...")
            
            # In a real implementation, this would spawn an actual subagent
            # For now, simulate the orchestration
            await asyncio.sleep(2)
            await ctx.send(f"✅ Subagent completed task: {task}\n\n*Note: Full subagent integration requires OpenClaw session spawning.*")
        
        logger.info("Starting Stephen Discord Bot...")
        await bot.start(self.token)
    
    async def generate_response(self, query: str, username: str) -> str:
        """Generate a Stephen-style response"""
        
        # Simple response generation based on persona
        # In production, this would call an actual LLM with the system prompt
        
        query_lower = query.lower()
        
        # Pattern matching for common queries
        if "help" in query_lower or "what can you do" in query_lower:
            return """I can help you think through problems, coordinate tasks, and orchestrate systems.

**What I do:**
• Break down complex problems
• Suggest approaches and trade-offs
• Coordinate multi-step tasks
• Spawn subagents for parallel work
• Document decisions and reasoning

**What I don't do:**
• Pretend to know things I don't
• Give vague answers to save face
• Mirror frustration back at you

Just ask. I'll be direct."""
        
        elif "status" in query_lower or "running" in query_lower:
            return "I'm operational. Running as an orchestrator. What needs coordination?"
        
        elif "hello" in query_lower or "hi" in query_lower:
            return f"Hey {username}. What are we working on?"
        
        elif "thank" in query_lower:
            return "No problem. What's next?"
        
        else:
            # Default Stephen-style response
            return f"""I'm processing that. Let me think through it.

**Quick take:**
This needs more context to give you a solid answer. What specifically are you trying to achieve? What's the real constraint here?

*Note: Full LLM integration would provide a more detailed response. This is the bot framework with Stephen's persona.*"""

def main():
    """Main entry point"""
    bot = StephenDiscordBot(BOT_TOKEN)
    
    try:
        asyncio.run(bot.start())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()