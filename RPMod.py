# meta developer: chatgpt
# meta name: RPMod

from .. import loader, utils


@loader.tds
class RPMod(loader.Module):
    """Inline RP module with custom commands"""

    strings = {"name": "RPMod"}

    async def client_ready(self):
        self.rp = await self.get("rp_commands", {})
        self.disabled = await self.get("rp_disabled", [])
        self.dm = await self.get("rp_dm", True)

    # =========================
    # CORE RP LOGIC
    # =========================

    async def watcher(self, message):
        if not getattr(message, "text", None):
            return

        if message.sender_id != (await message.client.get_me()).id:
            return

        chat_id = str(message.chat_id)

        # blocked chats
        if chat_id in self.disabled:
            return

        # DM toggle
        if message.is_private and not self.dm:
            return

        text = message.text.lower().strip()

        if text not in self.rp:
            return

        reply = await message.get_reply_message()
        if not reply:
            return

        try:
            await message.delete()
        except:
            pass

        me = await message.client.get_me()

        user1 = f"<b>{me.first_name}</b>"
        user2 = f"<b>{reply.sender.first_name}</b>"

        action = self.rp[text]

        await utils.answer(
            message,
            f"💕 {user1} {action} {user2}"
        )

    # =========================
    # ADMIN COMMANDS (ENGLISH)
    # =========================

    async def rpaddcmd(self, message):
        """Add RP command"""
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "Usage: .rpadd <command> <emoji/action>")
            return

        parts = args.split(" ", 1)
        if len(parts) < 2:
            await utils.answer(message, "Usage: .rpadd <command> <emoji/action>")
            return

        cmd, action = parts
        self.rp[cmd.lower()] = action

        await self.set("rp_commands", self.rp)
        await utils.answer(message, f"✅ Added RP command: {cmd}")

    async def rpdellcmd(self, message):
        """Delete RP command"""
        args = utils.get_args_raw(message).lower()
        if not args:
            await utils.answer(message, "Usage: .rpdel <command>")
            return

        if args in self.rp:
            del self.rp[args]
            await self.set("rp_commands", self.rp)
            await utils.answer(message, f"🗑 Deleted RP command: {args}")
        else:
            await utils.answer(message, "❌ Command not found")

    async def rplistcmd(self, message):
        """List RP commands"""
        if not self.rp:
            await utils.answer(message, "No RP commands")
            return

        out = "\n".join([f"• {k} → {v}" for k, v in self.rp.items()])
        await utils.answer(message, f"📜 RP commands:\n\n{out}")

    async def rpclearcmd(self, message):
        """Clear all RP commands"""
        self.rp = {}
        await self.set("rp_commands", self.rp)
        await utils.answer(message, "🧹 All RP commands cleared")

    async def rponcmd(self, message):
        """Enable RP in chat"""
        cid = str(message.chat_id)
        if cid in self.disabled:
            self.disabled.remove(cid)
        await self.set("rp_disabled", self.disabled)
        await utils.answer(message, "✅ RP enabled in this chat")

    async def rpoffcmd(self, message):
        """Disable RP in chat"""
        cid = str(message.chat_id)
        if cid not in self.disabled:
            self.disabled.append(cid)
        await self.set("rp_disabled", self.disabled)
        await utils.answer(message, "❌ RP disabled in this chat")

    async def dmrponcmd(self, message):
        """Enable RP in DMs"""
        self.dm = True
        await self.set("rp_dm", True)
        await utils.answer(message, "✅ RP enabled in DMs")

    async def dmrpoffcmd(self, message):
        """Disable RP in DMs"""
        self.dm = False
        await self.set("rp_dm", False)
        await utils.answer(message, "❌ RP disabled in DMs")

    async def rphelpcmd(self, message):
        """Help"""
        await utils.answer(
            message,
            "<b>RPMod Help</b>\n\n"
            ".rpadd <cmd> <action>\n"
            ".rpdel <cmd>\n"
            ".rplist\n"
            ".rpclear\n"
            ".rpon / .rpoff\n"
            ".dmrpon / .dmrpoff"
        )