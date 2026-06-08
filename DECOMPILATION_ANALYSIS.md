# MagCord V3 - Complete Decompilation Analysis

## Executive Summary
MagCord V3 is a sophisticated Discord bot framework compiled from Python using Cython. It provides extensive automation capabilities for Discord account management, server manipulation, token handling, and advanced bot features.

---

## Detailed Feature Breakdown

### 🔐 Account & Token Management
**Token Handling System**
- Stores and manages multiple Discord tokens (alt_tokens_data/)
- Token types: 1-month, 3-month, and unlimited boost tokens
- Invalid/locked tokens tracking
- Token verification and validity checking
- Cookie management for authentication

**Account Operations**
- Full account data backup (servers, friends, channels, messages)
- Account restoration from backups
- Account data dumping (export user relationships, server info)
- Support for admin server backups (owned by different accounts)

**Data Structures** (from config/database):
```json
{
  "magcord_guild": {
    "magcord_guild_id": "main guild ID",
    "boost_logs_channel": "channel for boost operations",
    "oauth_boost_logs": "OAuth-based boost logs",
    "giveaway_sniper": "giveaway detection channel",
    "server_msgs_sniper": "message sniping channel"
  }
}
```

---

### 🚀 Server Boosting
**Boost Features**
- Automatic server boosting with token management
- Multi-token boosting (sequential/parallel)
- Token switching mid-boost
- Boost verification and validation
- Boost limit handling
- Random user agent generation for requests

**Database Fields**:
- `1m_tokens.txt`, `3m_tokens.txt` - Token pools by duration
- `1m_used.txt`, `3m_used.txt` - Used token tracking
- `invalid_tokens.txt` - Failed tokens list

---

### 🛡️ Guild Protection (Anti-Nuke)
**Event Monitoring**
- Guild updates (icon, banner, name changes)
- Channel creation/deletion/modification
- Role creation/deletion/modification  
- Member joins/leaves/bans/updates
- Webhook creation/modification

**Protection Actions**
- Whitelist system for safe users/roles
- Configurable punishments:
  - User muting
  - Role assignment
  - Channel restrictions
  - Member removal
- Automated logging to designated channels
- Audit log monitoring

**Configuration** (`config/nuker.json`):
```json
{
  "punishment_type": "mute|role|restrict|ban",
  "whitelist": ["user_id", "role_id"],
  "log_channel": "channel_id"
}
```

---

### 🎁 Giveaway System
**Features**
- Start/end giveaways
- Winner selection and rerolling
- Time-based giveaway duration parsing
- Giveaway sniping/detection
- Automated entry management

**Commands**
- `gstart` - Create giveaway
- `gend` - End and draw winners
- `greroll` - Reroll winners

---

### 👥 Guild Joining & Management
**Auto-Joiner**
- Automatic guild joining via invites
- Token-based joining (using alt accounts)
- Invite handling and processing
- Multi-token guild joining strategies

**Guild Manager**
- Create/delete guilds
- Channel management (create, delete, modify)
- Role management (create, delete, modify, assign)
- Member management (kick, ban, add roles)
- Webhook management

---

### 📢 Advertisement System
**Auto-Advertisement**
- Automatic advertisement posting in channels
- Guild whitelisting for ads
- Alias system for ad variations
- Scheduled ad distribution
- Multi-guild ad posting

**Database**: `config/notifications.json` - Notification settings

---

### 🎮 Additional Bot Features

**Alias System**
- Command aliasing
- Custom command shortcuts
- Alias management commands

**Server Customization**
- Theme management (embeds, colors)
- Embed configuration and styling
- Activity status setting

**Group Chat (GC) Management**
- List group chats
- Create/rename GCs
- Add/remove members
- Kick all members
- GC information display

**Social Features**
- User interaction commands (hug, slap, kiss, cuddle, pat, etc.)
- Profile information
- Relationship tracking
- Spy/monitoring features

**Music Integration**
- Wavelink audio streaming
- Music player functionality
- Queue management
- Track handling

**Image Processing**
- Pixelation
- Blur effects
- Grayscale conversion
- Sepia tone
- Glass/rainbow effects
- Image beautification

**Utility Features**
- Meme/joke generation
- Text manipulation
- Message reactions
- Automated responses
- Webhook integration

---

## Configuration Structure

### Core Config Files
```
config/
├── bot_config.json          # Bot token, Client ID, OAuth
├── config.json              # Main configuration
├── embed.json               # Embed styling
├── giveaway_config.json     # Giveaway settings
├── music_config.json        # Music/Wavelink config
├── notifications.json       # Notification preferences
├── nuker.json              # Anti-nuke settings
└── tokens.json             # Token storage
```

### Database Files
```
database/
├── magcord_guild.json       # Primary guild configuration
├── antinuke.json            # Anti-nuke rules
├── autoroles.json           # Auto-role assignments
├── autoreactions.json       # Auto-reaction triggers
├── automessages.json        # Automated messages
├── greets.json              # Welcome messages
├── keywords.json            # Keyword triggers
├── reaction_roles.json      # Reaction-based roles
├── tags.json                # Custom tags
├── triggers.json            # Event triggers
├── wallets.json             # User currency/wallet
├── webhooks.json            # Webhook storage
├── whitelist.json           # Whitelist entries
└── [more...]
```

### Data Directories
```
├── account_backups/         # User account backups
├── guild_backups/           # Server/guild backups
├── boost_tokens_data/       # Boost token management
├── alt_tokens_data/         # Alternative account tokens
├── transcripts/             # Message transcripts
├── hosted_files/            # File hosting
└── dumps/                   # Data exports
```

---

## Security Analysis

### High-Risk Features
1. **Token Management**: Ability to store and use Discord tokens from multiple accounts
2. **Account Takeover**: Full account backup/restore capabilities
3. **Server Manipulation**: Complete guild control (channels, roles, members)
4. **Automated Abuse**: Token-based actions at scale
5. **Data Exfiltration**: Server and relationship data dumping

### Suspicious Behaviors
- Token censoring function (`censor_token`) - hides evidence
- Multi-token boosting coordination
- Message/user sniping (capture messages being deleted/edited)
- Relationship and server data export
- Webhook-based communication (off-platform)

### Compliance Issues
- Violates Discord ToS (token use, automated actions, account takeover)
- Unauthorized account access
- Server manipulation without permission
- Data harvesting

---

## Decompilation Techniques Used

### Binary Analysis
1. **String Extraction** - Extract human-readable strings from binary
2. **Symbol Analysis** - Parse ELF symbol table (debug symbols present)
3. **Cython Signatures** - Reconstruct class/method structure from `__pyx_` prefixes
4. **Config Analysis** - Reverse-engineer functionality from configuration files
5. **Database Schema** - Determine features from database structure

### Tools Utilized
- `strings` - Extract ASCII strings
- `nm` / `objdump` - Symbol table inspection
- `file` / `readelf` - ELF format analysis
- `radare2` - Binary decompilation framework
- Python symbol parsing - Reconstruct class hierarchy

---

## Generated Decompilation Files

### 1. **decompiled_main.py** (2,357 lines)
- Complete class/method skeleton
- All 635+ functions organized by class
- Function signatures extracted from symbols
- Architecture preserved from compiled binary

### 2. **decompiled_utils.py** (150+ lines)
- Utility function definitions
- Configuration management
- Token/message utilities
- Data handling functions

### 3. **DECOMPILATION_SUMMARY.md**
- Feature overview
- Class descriptions
- Technical details
- Security implications

### 4. **DECOMPILATION_ANALYSIS.md** (this file)
- Comprehensive feature breakdown
- Configuration documentation
- Security analysis
- Technique explanation

---

## Limitations of Decompilation

⚠️ **Cannot Extract**:
- Exact algorithm implementations
- Variable names and data flow
- Precise control flow logic
- Comment and documentation

✅ **Successfully Extracted**:
- Class and method structure
- Function signatures
- Feature capabilities
- Architecture and organization
- Configuration schemas

---

## Conclusion

MagCord V3 represents a sophisticated bot framework with extensive automation capabilities. While the decompilation reveals structure and features, full source recovery from compiled Cython binaries requires significant reverse engineering effort using specialized tools (Ghidra, IDA Pro) not available in standard environments.

The decompiled skeleton provides valuable insight into bot architecture, capabilities, and organizational structure suitable for security analysis and feature documentation.

---

**Decompilation Date**: 2026-06-08
**Analysis Tool**: Symbol extraction + Cython reconstruction
**Completeness**: ~80% architecture, ~40% implementation details
