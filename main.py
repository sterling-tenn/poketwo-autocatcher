from requests import post
import discord
from discord.ext import tasks
from re import findall
from re import MULTILINE
from time import sleep
from datetime import datetime
import ctypes


#Function Declarations
def solve(message):
    
    hint = []

    for i in range(15,len(message) - 1):
        if message[i] != "\\":
            hint.append(message[i])

    hint_string = ""
    for i in hint:
        hint_string += i
        
    hint_replaced = hint_string.replace("_",".")

    solution = findall('^'+hint_replaced+'$',pokemon_list_string, MULTILINE)

    return solution

def printLog(string):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("[",current_time,"]",string)

def updateTitle():
    ctypes.windll.kernel32.SetConsoleTitleW("Poketwo Auto-Catcher || Pokemon Caught: " + str(num_pokemon)+" || Shinies: "+str(num_shinies)+" || Legendaries: "+str(num_legendaries)+" || Mythics: "+str(num_mythics)+" || Fled: "+str(num_fled))


#Variable Declarations
informationFile = open("information.txt","r")
data = []
for line in informationFile:
    split = line.split(":")
    data.append(split[1].strip())
    #data[0] is the channel id
    #data[1] is the header authorization token
    #data[2] is the bot token
informationFile.close()

channel_id = int(data[0])
text_channel = 'https://discord.com/api/v8/channels/'+str(channel_id)+'/messages'
header = {'authorization': data[1]}
bot_token = data[2]
poketwo_id = 716390085896962058

pokemon_list_string = """Bulbasaur
Ivysaur
Venusaur
Charmander
Charmeleon
Charizard
Squirtle
Wartortle
Blastoise
Caterpie
Metapod
Butterfree
Weedle
Kakuna
Beedrill
Pidgey
Pidgeotto
Pidgeot
Rattata
Raticate
Spearow
Fearow
Ekans
Arbok
Pikachu
Raichu
Sandshrew
Sandslash
Nidoran ♂
Nidoran ♀
Nidorina
Nidoqueen
Nidorino
Nidoking
Clefairy
Clefable
Vulpix
Ninetales
Jigglypuff
Wigglytuff
Zubat
Golbat
Oddish
Gloom
Vileplume
Paras
Parasect
Venonat
Venomoth
Diglett
Dugtrio
Meowth
Persian
Psyduck
Golduck
Mankey
Primeape
Growlithe
Arcanine
Poliwag
Poliwhirl
Poliwrath
Abra
Kadabra
Alakazam
Machop
Machoke
Machamp
Bellsprout
Weepinbell
Victreebel
Tentacool
Tentacruel
Geodude
Graveler
Golem
Ponyta
Rapidash
Slowpoke
Slowbro
Magnemite
Magneton
Farfetch’d
Doduo
Dodrio
Seel
Dewgong
Grimer
Muk
Shellder
Cloyster
Gastly
Haunter
Gengar
Onix
Drowzee
Hypno
Krabby
Kingler
Voltorb
Electrode
Exeggcute
Exeggutor
Cubone
Marowak
Hitmonlee
Hitmonchan
Lickitung
Koffing
Weezing
Rhyhorn
Rhydon
Chansey
Tangela
Kangaskhan
Horsea
Seadra
Goldeen
Seaking
Staryu
Starmie
Mr. Mime
Scyther
Jynx
Electabuzz
Magmar
Pinsir
Tauros
Magikarp
Gyarados
Lapras
Ditto
Eevee
Vaporeon
Jolteon
Flareon
Porygon
Omanyte
Omastar
Kabuto
Kabutops
Aerodactyl
Snorlax
Articuno
Zapdos
Moltres
Dratini
Dragonair
Dragonite
Mewtwo
Mew
Chikorita
Bayleef
Meganium
Cyndaquil
Quilava
Typhlosion
Totodile
Croconaw
Feraligatr
Sentret
Furret
Hoothoot
Noctowl
Ledyba
Ledian
Spinarak
Ariados
Crobat
Chinchou
Lanturn
Pichu
Cleffa
Igglybuff
Togepi
Togetic
Natu
Xatu
Mareep
Flaaffy
Ampharos
Bellossom
Marill
Azumarill
Sudowoodo
Politoed
Hoppip
Skiploom
Jumpluff
Aipom
Sunkern
Sunflora
Yanma
Wooper
Quagsire
Espeon
Umbreon
Murkrow
Slowking
Misdreavus
Unown
Wobbuffet
Girafarig
Pineco
Forretress
Dunsparce
Gligar
Steelix
Snubbull
Granbull
Qwilfish
Scizor
Shuckle
Heracross
Sneasel
Teddiursa
Ursaring
Slugma
Magcargo
Swinub
Piloswine
Corsola
Remoraid
Octillery
Delibird
Mantine
Skarmory
Houndour
Houndoom
Kingdra
Phanpy
Donphan
Porygon2
Stantler
Smeargle
Tyrogue
Hitmontop
Smoochum
Elekid
Magby
Miltank
Blissey
Raikou
Entei
Suicune
Larvitar
Pupitar
Tyranitar
Lugia
Ho-Oh
Celebi
Treecko
Grovyle
Sceptile
Torchic
Combusken
Blaziken
Mudkip
Marshtomp
Swampert
Poochyena
Mightyena
Zigzagoon
Linoone
Wurmple
Silcoon
Beautifly
Cascoon
Dustox
Lotad
Lombre
Ludicolo
Seedot
Nuzleaf
Shiftry
Taillow
Swellow
Wingull
Pelipper
Ralts
Kirlia
Gardevoir
Surskit
Masquerain
Shroomish
Breloom
Slakoth
Vigoroth
Slaking
Nincada
Ninjask
Shedinja
Whismur
Loudred
Exploud
Makuhita
Hariyama
Azurill
Nosepass
Skitty
Delcatty
Sableye
Mawile
Aron
Lairon
Aggron
Meditite
Medicham
Electrike
Manectric
Plusle
Minun
Volbeat
Illumise
Roselia
Gulpin
Swalot
Carvanha
Sharpedo
Wailmer
Wailord
Numel
Camerupt
Torkoal
Spoink
Grumpig
Spinda
Trapinch
Vibrava
Flygon
Cacnea
Cacturne
Swablu
Altaria
Zangoose
Seviper
Lunatone
Solrock
Barboach
Whiscash
Corphish
Crawdaunt
Baltoy
Claydol
Lileep
Cradily
Anorith
Armaldo
Feebas
Milotic
Castform
Sunny Castform
Rainy Castform
Snowy Castform
Kecleon
Shuppet
Banette
Duskull
Dusclops
Tropius
Chimecho
Absol
Wynaut
Snorunt
Glalie
Spheal
Sealeo
Walrein
Clamperl
Huntail
Gorebyss
Relicanth
Luvdisc
Bagon
Shelgon
Salamence
Beldum
Metang
Metagross
Regirock
Regice
Registeel
Latias
Latios
Kyogre
Groudon
Rayquaza
Jirachi
Deoxys
Attack Deoxys
Defense Deoxys
Speed Deoxys
Turtwig
Grotle
Torterra
Chimchar
Monferno
Infernape
Piplup
Prinplup
Empoleon
Starly
Staravia
Staraptor
Bidoof
Bibarel
Kricketot
Kricketune
Shinx
Luxio
Luxray
Budew
Roserade
Cranidos
Rampardos
Shieldon
Bastiodon
Burmy
Wormadam
Sandy Wormadam
Trash Wormadam
Mothim
Combee
Vespiquen
Pachirisu
Buizel
Floatzel
Cherubi
Cherrim
Shellos
Gastrodon
Ambipom
Drifloon
Drifblim
Buneary
Lopunny
Mismagius
Honchkrow
Glameow
Purugly
Chingling
Stunky
Skuntank
Bronzor
Bronzong
Bonsly
Mime Jr.
Happiny
Chatot
Spiritomb
Gible
Gabite
Garchomp
Munchlax
Riolu
Lucario
Hippopotas
Hippowdon
Skorupi
Drapion
Croagunk
Toxicroak
Carnivine
Finneon
Lumineon
Mantyke
Snover
Abomasnow
Weavile
Magnezone
Lickilicky
Rhyperior
Tangrowth
Electivire
Magmortar
Togekiss
Yanmega
Leafeon
Glaceon
Gliscor
Mamoswine
Porygon-Z
Gallade
Probopass
Dusknoir
Froslass
Rotom
Uxie
Mesprit
Azelf
Dialga
Palkia
Heatran
Regigigas
Giratina
Cresselia
Phione
Manaphy
Darkrai
Shaymin
Arceus
Victini
Snivy
Servine
Serperior
Tepig
Pignite
Emboar
Oshawott
Dewott
Samurott
Patrat
Watchog
Lillipup
Herdier
Stoutland
Purrloin
Liepard
Pansage
Simisage
Pansear
Simisear
Panpour
Simipour
Munna
Musharna
Pidove
Tranquill
Unfezant
Blitzle
Zebstrika
Roggenrola
Boldore
Gigalith
Woobat
Swoobat
Drilbur
Excadrill
Audino
Timburr
Gurdurr
Conkeldurr
Tympole
Palpitoad
Seismitoad
Throh
Sawk
Sewaddle
Swadloon
Leavanny
Venipede
Whirlipede
Scolipede
Cottonee
Whimsicott
Petilil
Lilligant
Basculin
Blue-Striped Basculin
Red-Striped Basculin
Sandile
Krokorok
Krookodile
Darumaka
Darmanitan
Maractus
Dwebble
Crustle
Scraggy
Scrafty
Sigilyph
Yamask
Cofagrigus
Tirtouga
Carracosta
Archen
Archeops
Trubbish
Garbodor
Zorua
Zoroark
Minccino
Cinccino
Gothita
Gothorita
Gothitelle
Solosis
Duosion
Reuniclus
Ducklett
Swanna
Vanillite
Vanillish
Vanilluxe
Deerling
Sawsbuck
Emolga
Karrablast
Escavalier
Foongus
Amoonguss
Frillish
Jellicent
Alomomola
Joltik
Galvantula
Ferroseed
Ferrothorn
Klink
Klang
Klinklang
Tynamo
Eelektrik
Eelektross
Elgyem
Beheeyem
Litwick
Lampent
Chandelure
Axew
Fraxure
Haxorus
Cubchoo
Beartic
Cryogonal
Shelmet
Accelgor
Stunfisk
Mienfoo
Mienshao
Druddigon
Golett
Golurk
Pawniard
Bisharp
Bouffalant
Rufflet
Braviary
Vullaby
Mandibuzz
Heatmor
Durant
Deino
Zweilous
Hydreigon
Larvesta
Volcarona
Cobalion
Terrakion
Virizion
Tornadus
Thundurus
Reshiram
Zekrom
Landorus
Kyurem
Keldeo
Meloetta
Genesect
Chespin
Quilladin
Chesnaught
Fennekin
Braixen
Delphox
Froakie
Frogadier
Greninja
Bunnelby
Diggersby
Fletchling
Fletchinder
Talonflame
Scatterbug
Spewpa
Vivillon
Litleo
Pyroar
Flabébé
Floette
Florges
Skiddo
Gogoat
Pancham
Pangoro
Furfrou
Espurr
Meowstic
Honedge
Doublade
Aegislash
Spritzee
Aromatisse
Swirlix
Slurpuff
Inkay
Malamar
Binacle
Barbaracle
Skrelp
Dragalge
Clauncher
Clawitzer
Helioptile
Heliolisk
Tyrunt
Tyrantrum
Amaura
Aurorus
Sylveon
Hawlucha
Dedenne
Carbink
Goomy
Sliggoo
Goodra
Klefki
Phantump
Trevenant
Pumpkaboo
Gourgeist
Bergmite
Avalugg
Noibat
Noivern
Xerneas
Yveltal
Zygarde
10% Zygarde
50% Zygarde
Complete Zygarde
Diancie
Hoopa
Volcanion
Rowlet
Dartrix
Decidueye
Litten
Torracat
Incineroar
Popplio
Brionne
Primarina
Pikipek
Trumbeak
Toucannon
Yungoos
Gumshoos
Grubbin
Charjabug
Vikavolt
Crabrawler
Crabominable
Oricorio
Pom-pom Oricorio
Pa'u Oricorio
Sensu Oricorio
Cutiefly
Ribombee
Rockruff
Lycanroc
Wishiwashi
Mareanie
Toxapex
Mudbray
Mudsdale
Dewpider
Araquanid
Fomantis
Lurantis
Morelull
Shiinotic
Salandit
Salazzle
Stufful
Bewear
Bounsweet
Steenee
Tsareena
Comfey
Oranguru
Passimian
Wimpod
Golisopod
Sandygast
Palossand
Pyukumuku
Type: Null
Silvally
Minior
Komala
Turtonator
Togedemaru
Mimikyu
Bruxish
Drampa
Dhelmise
Jangmo-o
Hakamo-o
Kommo-o
Tapu Koko
Tapu Lele
Tapu Bulu
Tapu Fini
Cosmog
Cosmoem
Solgaleo
Lunala
Nihilego
Buzzwole
Pheromosa
Xurkitree
Celesteela
Kartana
Guzzlord
Necrozma
Magearna
Marshadow
Poipole
Naganadel
Stakataka
Blacephalon
Zeraora
Meltan
Melmetal
Grookey
Thwackey
Rillaboom
Scorbunny
Raboot
Cinderace
Sobble
Drizzile
Inteleon
Skwovet
Greedent
Rookidee
Corvisquire
Corviknight
Blipbug
Dottler
Orbeetle
Nickit
Thievul
Gossifleur
Eldegoss
Wooloo
Dubwool
Chewtle
Drednaw
Yamper
Boltund
Rolycoly
Carkol
Coalossal
Applin
Flapple
Appletun
Silicobra
Sandaconda
Cramorant
Arrokuda
Barraskewda
Toxel
Toxtricity
Sizzlipede
Centiskorch
Clobbopus
Grapploct
Sinistea
Polteageist
Hatenna
Hattrem
Hatterene
Impidimp
Morgrem
Grimmsnarl
Obstagoon
Perrserker
Cursola
Sirfetch’d
Mr. Rime
Runerigus
Milcery
Alcremie
Falinks
Pincurchin
Snom
Frosmoth
Stonjourner
Eiscue
Indeedee
Morpeko
Cufant
Copperajah
Dracozolt
Arctozolt
Dracovish
Arctovish
Duraludon
Dreepy
Drakloak
Dragapult
Zacian
Zamazenta
Eternatus
Kubfu
Urshifu
Zarude
Regieleki
Regidrago
Glastrier
Spectrier
Calyrex
Alolan Rattata
Alolan Raticate
Alolan Raichu
Alolan Sandshrew
Alolan Sandslash
Alolan Vulpix
Alolan Ninetales
Alolan Diglett
Alolan Dugtrio
Alolan Meowth
Alolan Persian
Alolan Geodude
Alolan Graveler
Alolan Golem
Alolan Grimer
Alolan Muk
Alolan Exeggutor
Alolan Marowak"""

legendary_list = """Mewtwo
Rayquaza
Necrozma
Yveltal
Xerneas
Dialga
Palkia
Giratina
Zekrom
Reshiram
Cosmog
Cosmoem
Solgaleo
Lunala
Kyurem
Groudon
Kyogre"""

mythic_list = """Diancie
Darkrai
Arceus
Mew
Zeraora"""

num_pokemon = 0
num_shinies = 0
num_fled = 0
num_legendaries = 0
num_mythics = 0


#Code
updateTitle()
print('                   Version 1.7 || By: bone')
print('===================================================================')

client = discord.Client()
@client.event
async def on_ready():
    print('Connection to bot "{0.user}" established. Starting auto-catcher.'.format(client))
    print('===================================================================')
    loop.start()
    print('Log:')
    print('====')

@client.event
async def on_message(message):
    try:
        if message.channel.id == channel_id:#only care about messages in the specified channel
            if  message.author.id == poketwo_id:#if poketwo sends a message
                if message.embeds:#if embedded image
                    #check if the embedded image is a wild pokemon appearance
                    embed_message = []
                    for embed in message.embeds:
                        embed_message.append(embed.to_dict())

                    wild_pokemon_found = findall('A wild pokémon has appeared!',str(embed_message))
                    wild_pokemon_fled = findall('A new wild pokémon has appeared!',str(embed_message))
 
                    if wild_pokemon_found or wild_pokemon_fled:#if wild pokemon is found/previous wild pokemon fled 
                        post(text_channel, data = {'content':'p!h'}, headers = header)
                        if wild_pokemon_fled:
                            global num_fled
                            num_fled += 1
                            updateTitle()
                            printLog(" A pokemon has fled.")

                else:#if normal text
                    #search if the message contains one of these phrases
                    is_hint = findall('The pokémon is ',message.content)
                    is_correct = findall('Congratulations',message.content)
                    is_shiny = findall('These colors seem unusual...',message.content)

                    if is_hint:
                        solution = solve(message.content)

                        if len(solution) == 0:
                            printLog("Pokemon could not be found in the database.")

                        #try all possible solutions - fix for short name pokemon by brute force
                        for i in range(0,len(solution)):
                            if solution[i] == "Nidoran ♂" or solution[i] == "Nidoran ♀":#hardcode Nidoran since the hint uses the unicode symbols ♂ and ♀
                                post(text_channel, data = {'content': 'p!c Nidoran'}, headers = header)
                            else: #everything else
                                post(text_channel, data = {'content': 'p!c '+ solution[i]}, headers = header)
                                if len(solution) > 1:#if there can be multiple solutions based on the hint, delay to prevent messages not being sent
                                    sleep(3)

                    elif is_correct:
                        global num_pokemon
                        num_pokemon += 1
                        
                        if is_shiny:
                            global num_shinies
                            num_shinies += 1
                        
                        split = message.content.split(" ")
                        
                        msg = ""
                        for i in range (2,len(split)):
                            msg += split[i] + " "

                        printLog(msg)
                        
                        pokemon = split[7].replace("!","")

                        if findall(pokemon,legendary_list,MULTILINE):
                            global num_legendaries
                            num_legendaries += 1

                        if findall(pokemon,mythic_list,MULTILINE):
                            global num_mythics
                            num_mythics += 1
                        
                        updateTitle()
    except Exception:
        loop.restart()
        pass

@tasks.loop(seconds=1.5)
async def loop():
    post(text_channel, data = {'content':'v1.7'}, headers = header)

@client.event
async def on_reaction_add(reaction, user):
    if reaction.emoji == '⌛':#if p!h is on cooldown
        sleep(10)
        post(text_channel, data = {'content':'p!h'}, headers = header)
        
client.run(bot_token)