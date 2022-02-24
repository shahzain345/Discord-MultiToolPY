import time
import discum


class MemberScrapper:
    def __init__(self, token):
        self.bot = discum.Client(token=token)

    def close_after_fetching(self, resp, guild_id):
        if self.bot.gateway.finishedMemberFetching(guild_id):
            lenmembersfetched = len(self.bot.gateway.session.guild(
                guild_id).members)  # this line is optional
            # this line is optional
            self.bot.gateway.removeCommand(
                {'function': self.close_after_fetching, 'params': {'guild_id': guild_id}})
            self.bot.gateway.close()

    def get_members(self, guild_id, channel_id):
        # get all user attributes, wait 1 second between requests
        self.bot.gateway.fetchMembers(guild_id, channel_id, keep="all", wait=1)
        self.bot.gateway.command(
            {'function': self.close_after_fetching, 'params': {'guild_id': guild_id}})
        self.bot.gateway.run()
        self.bot.gateway.resetSession()  # saves 10 seconds when gateway is run again
        return self.bot.gateway.session.guild(guild_id).members
