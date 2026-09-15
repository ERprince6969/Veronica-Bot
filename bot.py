import discord
from discord import app_commands
from discord.ext import commands
import random
from datetime import datetime
import os
from flask import Flask, jsonify
from threading import Thread

flask_app = Flask(__name__)

@flask_app.route('/')
def index():
    online = bot.is_ready()
    latency = round(bot.latency * 1000) if online else None
    status_color = "#57F287" if online else "#ED4245"
    status_text = "Online" if online else "Offline"
    bot_name = bot.user.name if online and bot.user else "Bot"
## sta roba html l'ha fatta claude
    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{bot_name} Status</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Segoe UI', sans-serif;
      background: #1a1a2e;
      color: #e0e0e0;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
    }}
    .card {{
      background: #16213e;
      border-radius: 16px;
      padding: 48px 56px;
      text-align: center;
      box-shadow: 0 8px 32px rgba(0,0,0,0.4);
      max-width: 400px;
      width: 90%;
    }}
    .dot {{
      width: 18px; height: 18px;
      border-radius: 50%;
      background: {status_color};
      display: inline-block;
      margin-right: 8px;
      box-shadow: 0 0 12px {status_color};
      animation: pulse 2s infinite;
    }}
    @keyframes pulse {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.5; }}
    }}
    h1 {{ font-size: 2rem; margin-bottom: 8px; color: #ffffff; }}
    .status {{
      font-size: 1.1rem;
      color: {status_color};
      font-weight: 600;
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .ping-btn {{
      display: inline-block;
      background: #5865F2;
      color: white;
      text-decoration: none;
      padding: 12px 32px;
      border-radius: 8px;
      font-size: 1rem;
      font-weight: 600;
      transition: background 0.2s;
      margin-top: 8px;
    }}
    .ping-btn:hover {{ background: #4752c4; }}
    .latency {{
      margin-top: 20px;
      font-size: 0.95rem;
      color: #aaa;
    }}
    .latency span {{ color: #57F287; font-weight: 600; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>🤖 {bot_name}</h1>
    <div class="status"><span class="dot"></span>{status_text}</div>
    <a href="/ping" class="ping-btn">🏓 Ping</a>
    {"<div class='latency'>Latenza: <span>" + str(latency) + " ms</span></div>" if latency is not None else ""}
  </div>
</body>
</html>"""
    return html

@flask_app.route('/ping')
def ping():
    online = bot.is_ready()
    latency = round(bot.latency * 1000) if online else None
    return jsonify({
        "status": "online" if online else "offline",
        "latency_ms": latency
    })

def run_flask():
    flask_app.run(host='0.0.0.0', port=5000)

Thread(target=run_flask, daemon=True).start()


class MyBot(commands.Bot):
    def __init__(self):
        # Intents necessari per leggere messaggi e vedere i membri
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="!", intents=intents, help_command=None)

    async def setup_hook(self):
        # Sincronizza i comandi slash con i server di Discord
        await self.tree.sync()
        print(f"--- Comandi Slash Sincronizzati ---")

bot = MyBot()

# --- LOGS & MONITORAGGIO ---
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    orario = datetime.now().strftime("%H:%M:%S")
    posizione = "DM" if message.guild is None else f"#{message.channel.name}"
    print(f"[{orario}] {message.author} in {posizione}: {message.content}")

    # Se è un messaggio privato (DM), il bot non processa i comandi
    if message.guild is None:
        return

    await bot.process_commands(message)

@bot.event
async def on_ready():
    # Stato Non Disturbare
    await bot.change_presence(
        status=discord.Status.dnd, 
        activity=discord.Game(name="Usa i comandi / ... coglione")
    )
    print(f'Bot online come {bot.user.name}')

# Sostituisci questo numero con il tuo vero ID utente di Discord
MIO_ID = vanilla unicorn  

# Check personalizzato basato sull'ID
def is_bot_owner():
    def predicate(interaction: discord.Interaction) -> bool:
        return interaction.user.id == MIO_ID
    return app_commands.check(predicate)

@bot.tree.command(name="di", description="Fai inviare un messaggio al bot (Solo creatore)")
@app_commands.describe(
    messaggio="Il testo che il bot deve inviare",
    canale="Canale facoltativo in cui inviare il messaggio"
)
@is_bot_owner()
async def di(interaction: discord.Interaction, messaggio: str, canale: discord.TextChannel = None):
    canale_destinazione = canale or interaction.channel
    
    await canale_destinazione.send(messaggio)
    await interaction.response.send_message(
        f"✅ Messaggio inviato in {canale_destinazione.mention}!", 
        ephemeral=True
    )

@bot.command(name="sync")
async def sync_commands(ctx):
    # Controllo di sicurezza: solo tu puoi usare questo comando
    if ctx.author.id != MIO_ID:
        return
    
    try:
        synced = await bot.tree.sync()
        await ctx.send(f"✅ Ho fetchato e sincronizzato {len(synced)} comandi slash!")
    except Exception as e:
        await ctx.send(f"❌ Errore durante la sincronizzazione: {e}")

# Gestione errore se qualcun altro prova a usarlo
@di.error
async def di_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message(
            "❌ Non sei autorizzato. Solo il mio creatore può usare questo comando.", 
            ephemeral=True
        )

# 1. Lancio della Moneta
@bot.tree.command(name="moneta", description="Lancia una moneta (Testa o Croce)")
async def moneta(interaction: discord.Interaction):
    esito = random.choice(["Testa", "Croce"])
    await interaction.response.send_message(f"🪙 ... è uscito: **{esito}**!")

# 2. Userinfo con Scelta Utente
@bot.tree.command(name="userinfo", description="Mostra i dati di un utente specifico")
@app_commands.describe(utente="L'utente da analizzare")
async def userinfo(interaction: discord.Interaction, utente: discord.Member = None):
    utente = utente or interaction.user

    embed = discord.Embed(title=f"Profilo di {utente.name}", color=discord.Color.blue())
    embed.set_thumbnail(url=utente.avatar.url if utente.avatar else utente.default_avatar.url)
    embed.add_field(name="ID Utente", value=utente.id, inline=False)
    embed.add_field(name="Account creato", value=utente.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="Entrato nel server", value=utente.joined_at.strftime("%d/%m/%Y"), inline=True)

    await interaction.response.send_message(embed=embed)

# 3. Foto Casuale
@bot.tree.command(name="random", description="Invia una foto casuale")
async def random_foto(interaction: discord.Interaction):
    links = [
        ""
    ]
    await interaction.response.send_message(random.choice(links))

# 4. Lancio del Dado
@bot.tree.command(name="dado", description="Lancia un dado da 6 facce")
async def dado(interaction: discord.Interaction):
    risultato = random.randint(1, 6)
    await interaction.response.send_message(f"🎲 Risultato del dado: **{risultato}**")

@bot.tree.command(name="serverinfo", description="Info sul server")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=guild.name, color=discord.Color.green())
    embed.add_field(name="Membri", value=guild.member_count)
    embed.add_field(name="Creato il", value=guild.created_at.strftime("%d/%m/%Y"))
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="8ball", description="Fai una domanda al destino")
async def eightball(interaction: discord.Interaction, domanda: str):
    risposte = [
        "Sì.", "No.", "Forse.", "Decisamente sì.",
        "Assolutamente no.", "Riprovaci."
    ]

    embed = discord.Embed(
        title="🎱 Coglione magico",
        color=discord.Color.purple()
    )
    embed.add_field(name="❓ Domanda", value=domanda, inline=False)
    embed.add_field(name="🔮 Risposta", value=random.choice(risposte), inline=False)

    await interaction.response.send_message(embed=embed)

# 5. Pulizia Messaggi
@bot.tree.command(name="pulisci", description="Elimina un numero preciso di messaggi")
@app_commands.describe(quantita="Quanti messaggi vuoi cancellare?")
@app_commands.checks.has_permissions(manage_messages=True)
async def pulisci(interaction: discord.Interaction, quantita: int = 5):
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=quantita)
    await interaction.followup.send(f"✅ Ho rimosso {len(deleted)} messaggi.", ephemeral=True)

# Avvio del Bot
bot.run('')
