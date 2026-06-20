# meta developer: chatgpt
# meta name: RPMod

from .. import loader, utils


@loader.tds
class RPMod(loader.Module):
    """Stable RP module for Hikka"""

    strings = {"name": "RPMod"}

    async def client_ready(self):
        self.rp = await self.get("rp_commands", {})
        self.disabled = await self.get("rp_disabled", [])
        self.dm = await self.get("rp_dm", True)

    # =========================
    # RP WATCHER
    # =========================

    async def watcher(self, message):
        if not getattr(message, "text", None):
            return

        # only your messages
        me = await message.client.get_me()
        if message.sender_id != me.id:
            return

        text = message.text.lower().strip()

        chat_id = str(message.chat_id)

        # chat disabled
        if chat_id in self.disabled:
            return

        # DM toggle
        if message.is_private and not self.dm:
            return

        # must exist in RP list
        if text not in self.rp:
            return

        reply = await message.get_reply_message()
        if not reply:
            return

        action = self.rp[text]

        # delete ONLY your command message
        try:
            await message.delete()
        except:
            pass

        me_name = me.first_name
        target_name = reply.sender.first_name

        await utils.answer(
            message,
            f"💕 <b>{me_name}</b> {action} <b>{target_name}</b>"
        )

    # =========================
    # COMMANDS (ENGLISH ONLY)
    # =========================

    async def rpaddcmd(self, message):
        """Add RP command"""
        args = utils.get_args_raw(message)

        if not args or " " not in args:
            await utils.answer(message, "Usage: .rpadd <command> <action>")
            return

        cmd, action = args.split(" ", 1)
        self.rp[cmd.lower()] = action

        await self.set("rp_commands", self.rp)
        await utils.answer(message, f"✅ Added: {cmd}")

    async def rpdellcmd(self, message):
        """Delete RP command"""
        args = utils.get_args_raw(message).lower()

        if not args:
            await utils.answer(message, "Usage: .rpdel <command>")
            return

        if args in self.rp:
            del self.rp[args]
            await self.set("rp_commands", self.rp)
            await utils.answer(message, f"🗑 Deleted: {args}")
        else:
            await utils.answer(message, "❌ Not found")

    async def rplistcmd(self, message):
        """List RP commands"""
        if not self.rp:
            await utils.answer(message, "No RP commands")
            return

        out = "\n".join([f"• {k} → {v}" for k, v in self.rp.items()])
        await utils.answer(message, f"<b>RP commands:</b>\n\n{out}")

    async def rpclearcmd(self, message):
        """Clear RP commands"""
        self.rp = {}
        await self.set("rp_commands", self.rp)
        await utils.answer(message, "🧹 Cleared")

    async def rponcmd(self, message):
        """Enable RP in chat"""
        cid = str(message.chat_id)
        if cid in self.disabled:
            self.disabled.remove(cid)

        await self.set("rp_disabled", self.disabled)
        await utils.answer(message, "✅ RP ON")

    async def rpoffcmd(self, message):
        """Disable RP in chat"""
        cid = str(message.chat_id)
        if cid not in self.disabled:
            self.disabled.append(cid)

        await self.set("rp_disabled", self.disabled)
        await utils.answer(message, "❌ RP OFF")

    async def dmrponcmd(self, message):
        """Enable RP in DMs"""
        self.dm = True
        await self.set("rp_dm", True)
        await utils.answer(message, "✅ DM RP ON")

    async def dmrpoffcmd(self, message):
        """Disable RP in DMs"""
        self.dm = False
        await self.set("rp_dm", False)
        await utils.answer(message, "❌ DM RP OFF")

    async def rphelpcmd(self, message):
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