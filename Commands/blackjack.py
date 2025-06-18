import discord
from discord.ext import commands
import random

suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

def calculate_hand_value(hand):
    value = sum(values[card[0]] for card in hand)
    # Adjust for Aces if needed
    num_aces = sum(1 for card in hand if card[0] == 'A')
    while value > 21 and num_aces:
        value -= 10
        num_aces -= 1
    return value

def hand_to_string(hand, hide_second=False):
    if hide_second:
        return f"{hand[0][0]}{hand[0][1]} [Hidden]"
    return ' '.join(f"{card[0]}{card[1]}" for card in hand)

class BlackjackView(discord.ui.View):
    def __init__(self, cog, ctx, game):
        super().__init__(timeout=120)  # 2 min timeout
        self.cog = cog
        self.ctx = ctx
        self.game = game

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        # Only the game starter can press the buttons
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("You are not part of this game!", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.primary)
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        card = self.game['deck'].pop()
        self.game['player'].append(card)
        player_val = calculate_hand_value(self.game['player'])
        if player_val > 21:
            # Bust
            dealer_str = hand_to_string(self.game['dealer'])
            embed = self.cog.make_embed(self.ctx.author, self.game['player'], self.game['dealer'], hide_dealer=False, result=f"BUST! Dealer's hand: {dealer_str}\nGame over.")
            for item in self.children:
                item.disabled = True
            await interaction.response.edit_message(embed=embed, view=self)
            del self.cog.sessions[self.ctx.author.id]
        else:
            embed = self.cog.make_embed(self.ctx.author, self.game['player'], self.game['dealer'], hide_dealer=True)
            await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Stand", style=discord.ButtonStyle.secondary)
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Dealer plays
        dealer = self.game['dealer']
        player = self.game['player']
        deck = self.game['deck']
        dealer_val = calculate_hand_value(dealer)
        player_val = calculate_hand_value(player)
        while dealer_val < 17:
            dealer.append(deck.pop())
            dealer_val = calculate_hand_value(dealer)

        # Determine winner
        if dealer_val > 21 or player_val > dealer_val:
            result = "You win! 🎉"
        elif player_val == dealer_val:
            result = "It's a tie! 🤝"
        else:
            result = "Dealer wins! 😭"
        embed = self.cog.make_embed(self.ctx.author, player, dealer, hide_dealer=False, result=result)
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)
        del self.cog.sessions[self.ctx.author.id]

class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sessions = {}  # key: user.id, value: game state dict

    def make_embed(self, user, player, dealer, hide_dealer=True, result=None):
        embed = discord.Embed(title="Blackjack", color=discord.Color.green())
        player_str = hand_to_string(player)
        dealer_str = hand_to_string(dealer, hide_second=hide_dealer)
        embed.add_field(name=f"{user.display_name}'s Hand", value=f"{player_str} (Total: {calculate_hand_value(player)})", inline=False)
        if hide_dealer:
            embed.add_field(name="Dealer's Hand", value=f"{dealer_str}", inline=False)
        else:
            embed.add_field(name="Dealer's Hand", value=f"{hand_to_string(dealer)} (Total: {calculate_hand_value(dealer)})", inline=False)
        if result:
            embed.add_field(name="Result", value=result, inline=False)
        embed.set_footer(text="Blackjack by DiscordBot")
        return embed

    @commands.command()
    async def blackjack(self, ctx):
        """Start a new blackjack game (only for you, uses buttons!)"""
        user = ctx.author
        if user.id in self.sessions:
            await ctx.send(f"{user.mention} You already have a game in progress!")
            return

        # Build the deck, shuffle
        deck = [(rank, suit) for suit in suits for rank in ranks]
        random.shuffle(deck)
        player = [deck.pop(), deck.pop()]
        dealer = [deck.pop(), deck.pop()]

        self.sessions[user.id] = {
            'deck': deck,
            'player': player,
            'dealer': dealer,
            'active': True
        }

        embed = self.make_embed(user, player, dealer, hide_dealer=True)
        view = BlackjackView(self, ctx, self.sessions[user.id])
        await ctx.send(embed=embed, view=view)

def setup(bot):
    bot.add_cog(Blackjack(bot))