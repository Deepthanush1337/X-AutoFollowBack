# MagCord V3 Bot - .SO File Decompilation Summary

## Overview
MagCord V3 is a comprehensive Discord bot framework compiled as Cython modules (.so files). The bot is designed for advanced guild management, token handling, boosting, and automated Discord operations.

## Decompiled Modules

### 1. main.so (14.4 MB) - Core Bot Logic
Compiled from `main.py`. Contains all major bot classes and Discord.py bot functionality.

#### Major Classes & Features:

**Account Management**
- `Account` - Account backup and restoration
  - `backupaccount()` - Backup user account data
  - `backupservers()` - Backup guild/server information
  - `backupownerservers()` - Backup owned servers
  - `backupadminservers()` - Backup admin servers
  - `backupfriends()` - Backup friend list
  - `restoreservers()` - Restore server data
  - `restorefriends()` - Restore friend list
  - `dumpservers()` - Dump server info
  - `dumpfriends()` - Dump friend data
  - `dumpgcs()` - Dump group chats

**Token & Alt Account Management**
- `Alts` - Alternative account handling
  - `join_with_token()` - Join guilds with alt tokens
  - `check_token()` - Verify token validity
  - `check_token_line()` - Check token from line
  - `get_user_from_token()` - Extract user info from token
  - `send_message_with_token()` - Send messages via token
  - `switchtoken()` - Switch between tokens
  - `random_csrf_token()` - Generate CSRF tokens

**Boost Features**
- `Boost` - Server boosting operations
  - `boost()` - Boost server
  - `boost_with_token()` - Boost using specific token
  - `addtokens()` - Add tokens to boost pool
  - `checktokens()` - Verify token validity
  - `cleartokens()` - Clear token storage
  - `get_cookies()` - Extract/manage cookies
  - `ran_str()` - Generate random strings
  - `check_token_in_guild()` - Validate token in guild

**Server Management**
- `GuildManager` - Guild operations
  - Guild creation/deletion
  - Channel management
  - Role management
  - Member management

**Anti-Nuke Protection**
- `AntiNuke` - Guild protection features
  - `on_guild_update()` - Monitor guild changes
  - `on_guild_channel_create/delete/update()` - Monitor channels
  - `on_guild_role_create/delete/update()` - Monitor roles
  - `on_member_ban/join/remove/update()` - Monitor members
  - `on_webhooks_update()` - Monitor webhooks
  - `whitelist()` - Whitelist users/roles
  - `punish()` - Enforce punishments
  - `setpunishment()` - Configure punishment type

**Giveaway System**
- `Giveaway` - Giveaway management
  - `gstart()` - Start giveaway
  - `gend()` - End giveaway
  - `greroll()` - Reroll winners
  - `parse_time()` - Parse duration strings

**Server Joining**
- `Joiner` - Automatic guild joining
  - Auto-join guilds with various methods
  - Invite handling

**Auto-Advertise**
- `AutoAdvertise` - Automatic advertisement posting
  - `autoad()` - Automatic ad posting
  - `adguildadd/rem()` - Manage ad guilds
  - `adaliasadd/rem()` - Manage ad aliases

**Alias System**
- `AliasCog` - Command aliases
  - `addalias()` - Add command alias
  - `removealias()` - Remove alias
  - `apply_aliases()` - Apply aliases to commands

**Social Features**
- `SpyCog` - Monitoring/spying features
- `ReactionRoleCog` - Reaction-based role assignment
- `Greet` - Greeting/welcome messages
- `Wallet` - Currency/wallet management
- `ServerCog` - Server-specific features
- `TasksCog` - Scheduled tasks

**Other Features**
- Image manipulation (blur, pixelate, grayscale, sepia, rainbow, etc.)
- Meme/joke commands
- Group chat management
- Notification system
- Reaction loops
- NSFW content handling
- Music features (wavelink integration)

---

### 2. utils.so (1.2 MB) - Utility Functions
Compiled from `utils.py`. Contains helper functions for configuration, messaging, and bot operations.

#### Key Functions:
- **Config Management**: `load_config()`, `save_config()`, `get_config_value()`
- **Token Management**: `load_tokens()`, `get_active_token()`, `switch_token()`
- **Messaging**: `send()`, `send_webhook()`, `send_to_discord()`, `senderror()`
- **Text Processing**: `center_text()`, `color_text()`, `chunk_text()`, `split_description()`
- **Bot Auth**: `check_bot_authorization()`, `auto_authorize_bot()`
- **Embed Management**: `safe_add_field()`, `save_embed_data()`, `load_embed_config()`
- **Utilities**: `denitro()`, `resolve_placeholders()`, `get_notification_status()`

---

### 3. extra.so, extra2.so, extra3.so, extra4.so, extra5.so
Additional compiled modules with specialized functionality. (Detailed contents require deeper analysis)

---

## Security Implications

The bot includes features for:
- ✓ **Account Control**: Full account backup/restore
- ✓ **Token Management**: Handling multiple Discord tokens
- ✓ **Automated Actions**: Token-based guild joining and boosting
- ✓ **Account Data Dumping**: Extracting account information
- ✓ **Server Manipulation**: Channel/role/member management
- ✓ **Protection Systems**: Anti-nuke and anti-raid features

---

## Technical Details

**Compilation**: Cython (Python → C → Compiled Binary)
- **Debug Info**: Present (not stripped)
- **Symbols**: Visible for analysis
- **Size**: main.so = 14.4 MB (large due to debug symbols)

**Dependencies**:
- discord.py (Discord API)
- wavelink (Audio/Music)
- Various utility libraries

---

## Decompilation Methods Used

1. **String Extraction**: `strings` command to extract readable strings and function names
2. **Symbol Analysis**: `nm` and `objdump` for symbol table inspection
3. **Binary Inspection**: `file` and `readelf` for ELF format analysis
4. **Radare2**: Binary decompilation framework
5. **Cython Symbol Reconstruction**: Parsing `__pyx_` prefixed symbols for structure

---

## Generated Files

- `decompiled_main.py` - Reconstructed class/method skeleton from main.so (2,357 lines)
- `decompiled_utils.py` - Reconstructed utility functions from utils.so
- `DECOMPILATION_SUMMARY.md` - This summary document

All files preserve the original architecture and function signatures extracted from the compiled binaries.
