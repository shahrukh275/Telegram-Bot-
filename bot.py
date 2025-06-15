#!/usr/bin/env python3
"""
Telegram Admin Bot
A comprehensive bot for managing Telegram groups with advanced moderation features.
"""

import logging
import asyncio
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ChatMemberHandler,
    filters, ContextTypes
)

# Import configuration and database
from config import Config
from database import db

# Import all handlers
from handlers.admin_commands import (
    fileid_command, activate_command, silence_command, unsilence_command,
    underattack_command, ua_command, reload_command, debug_command,
    pin_command, unpin_command, purge_command
)

from handlers.user_management import (
    promote_command, title_command, demote_command,
    ban_command, sban_command, gban_command, sgban_command,
    unban_command, gunban_command, banlist_command,
    kick_command, skick_command, gkick_command,
    mute_command, unmute_command, smute_command
)

from handlers.warning_system import (
    warn_command, gwarn_command, swarn_command,
    unwarn_command, resetwarns_command, warnings_command
)

from handlers.whitelist_system import (
    whitelist_command, gwhitelist_command, unwhitelist_command,
    gunwhitelist_command, whitelisted_command, checkwhitelist_command
)

from handlers.user_info import (
    resetuser_command, resetrep_command, user_command,
    lastactive_command, id_command, chatinfo_command
)

from handlers.verification import (
    verify_command, handle_forwarded_message
)

from handlers.help_commands import (
    help_command, start_command, about_command, commands_command
)

from handlers.events import (
    handle_new_member, handle_left_member, handle_message,
    handle_chat_member_update, handle_bot_added_to_chat, error_handler
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, Config.LOG_LEVEL.upper())
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the bot"""
    try:
        # Validate configuration
        Config.validate()
        logger.info("Configuration validated successfully")
        
        # Create application
        application = Application.builder().token(Config.BOT_TOKEN).build()
        
        # Add command handlers
        
        # Admin utility commands
        application.add_handler(CommandHandler("fileid", fileid_command))
        
        # Chat management commands
        application.add_handler(CommandHandler("activate", activate_command))
        application.add_handler(CommandHandler("silence", silence_command))
        application.add_handler(CommandHandler("unsilence", unsilence_command))
        application.add_handler(CommandHandler("underattack", underattack_command))
        application.add_handler(CommandHandler("ua", ua_command))
        application.add_handler(CommandHandler("reload", reload_command))
        application.add_handler(CommandHandler("debug", debug_command))
        application.add_handler(CommandHandler("pin", pin_command))
        application.add_handler(CommandHandler("unpin", unpin_command))
        application.add_handler(CommandHandler("purge", purge_command))
        
        # User management commands
        application.add_handler(CommandHandler("promote", promote_command))
        application.add_handler(CommandHandler("title", title_command))
        application.add_handler(CommandHandler("demote", demote_command))
        
        application.add_handler(CommandHandler("ban", ban_command))
        application.add_handler(CommandHandler("sban", sban_command))
        application.add_handler(CommandHandler("gban", gban_command))
        application.add_handler(CommandHandler("sgban", sgban_command))
        
        application.add_handler(CommandHandler("unban", unban_command))
        application.add_handler(CommandHandler("gunban", gunban_command))
        application.add_handler(CommandHandler("banlist", banlist_command))
        
        application.add_handler(CommandHandler("kick", kick_command))
        application.add_handler(CommandHandler("skick", skick_command))
        application.add_handler(CommandHandler("gkick", gkick_command))
        
        application.add_handler(CommandHandler("mute", mute_command))
        application.add_handler(CommandHandler("unmute", unmute_command))
        application.add_handler(CommandHandler("smute", smute_command))
        
        # Warning system commands
        application.add_handler(CommandHandler("warn", warn_command))
        application.add_handler(CommandHandler("gwarn", gwarn_command))
        application.add_handler(CommandHandler("swarn", swarn_command))
        application.add_handler(CommandHandler("unwarn", unwarn_command))
        application.add_handler(CommandHandler("resetwarns", resetwarns_command))
        application.add_handler(CommandHandler("warnings", warnings_command))
        
        # Whitelist system commands
        application.add_handler(CommandHandler("whitelist", whitelist_command))
        application.add_handler(CommandHandler("gwhitelist", gwhitelist_command))
        application.add_handler(CommandHandler("unwhitelist", unwhitelist_command))
        application.add_handler(CommandHandler("gunwhitelist", gunwhitelist_command))
        application.add_handler(CommandHandler("whitelisted", whitelisted_command))
        application.add_handler(CommandHandler("checkwhitelist", checkwhitelist_command))
        
        # User info commands
        application.add_handler(CommandHandler("resetuser", resetuser_command))
        application.add_handler(CommandHandler("resetrep", resetrep_command))
        application.add_handler(CommandHandler("user", user_command))
        application.add_handler(CommandHandler("lastactive", lastactive_command))
        application.add_handler(CommandHandler("id", id_command))
        application.add_handler(CommandHandler("chatinfo", chatinfo_command))
        
        # Verification commands
        application.add_handler(CommandHandler("verify", verify_command))
        
        # Help commands
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("about", about_command))
        application.add_handler(CommandHandler("commands", commands_command))
        
        # Event handlers
        application.add_handler(MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS, 
            handle_new_member
        ))
        
        application.add_handler(MessageHandler(
            filters.StatusUpdate.LEFT_CHAT_MEMBER, 
            handle_left_member
        ))
        
        # Handle bot being added to chat
        application.add_handler(MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS & filters.User(user_id=None),  # Will be set to bot's ID
            handle_bot_added_to_chat
        ))
        
        # Handle forwarded messages for verification (private chats only)
        application.add_handler(MessageHandler(
            filters.FORWARDED & filters.ChatType.PRIVATE,
            handle_forwarded_message
        ))
        
        # Chat member updates (promotions, bans, etc.)
        application.add_handler(ChatMemberHandler(
            handle_chat_member_update,
            ChatMemberHandler.CHAT_MEMBER
        ))
        
        # General message handler (should be last)
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        ))
        
        # Error handler
        application.add_error_handler(error_handler)
        
        logger.info("Bot handlers registered successfully")
        
        # Start the bot
        logger.info("Starting bot...")
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == '__main__':
    main()