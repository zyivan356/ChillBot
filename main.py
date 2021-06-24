import discord
from discord import utils


#config

TOKEN = 'ODU3NTcyMDc4NzU5NTc1NjAy.YNRiPA.IBmR7In2fLzWtkH1zuBriVRGRJ4'

POST_ID = 857600054323445781

ROLES = {
    '<:refrigerator:857595228923232257>': 857568459018076211,
    '<:microwave:857596363198169088>': 857568741507858473,
    '<:dishwasher:857596818494193674>': 857568803931947028,
    '<:airconditioning:857597326104985620>': 857568715515625472,
    '<:stove:857597623669751828>': 857568783459418152,
    '<:iron:857598312398716928>': 857568830996873216,
    '<:washingmachine:857598593519452180>': 857568806900465664,
    '<:intercom:857598843980742676>': 857569262477639690,
    '<:teapot2:857597940817592360>': 857569296343367721,
}

EXCROLES = ()

MAX_ROLES_PER_USER = 1

#script

intents = discord.Intents.all()

# запуск бота

client = discord.Client(intents=intents)


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_raw_reaction_add(self, payload):
        if payload.message_id == POST_ID:
            channel = self.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            member = utils.get(message.guild.members,
                               id=payload.user_id)

            try:
                emoji = str(payload.emoji)
                role = utils.get(message.guild.roles, id=ROLES[emoji])

                if (len([i for i in member.roles if i.id not in EXCROLES]) <= MAX_ROLES_PER_USER):
                    await member.add_roles(role)
                    print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
                else:
                    await message.remove_reaction(payload.emoji, member)
                    print('[ERROR] Too many roles for user {0.display_name}'.format(member))

            except KeyError as e:
                print('[ERROR] KeyError, no role found for ' + emoji)
            except Exception as e:
                print(repr(e))

    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.get(message.guild.members,
                           id=payload.user_id)

        try:
            emoji = str(payload.emoji)
            role = utils.get(message.guild.roles, id=ROLES[emoji])

            await member.remove_roles(role)
            print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))

        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))





client = discord.Client(intents=intents)
client = MyClient(intents=intents)
client.run(TOKEN)