from nordvpn_switcher import initialize_VPN,rotate_VPN
import time

##############
## WINDOWS ###
##############

# [1] save settings file as a variable

instructions = initialize_VPN() #this will guide you through a step-by-step guide, including a help-menu with connection options

for i in range(3):
    rotate_VPN(instructions) #refer to the instructions variable here
    print('\nDo whatever you want here (e.g.scraping). Pausing for 10 seconds...\n')
    time.sleep(10)

# [2] if you'd like to skip the step-by-step menu (because you want to automate your script fully without any required human intervention, use the area_input parameter

instructions = initialize_VPN(area_input=['Belgium,France,Netherlands']) # <-- Be aware: the area_input parameter expects a list, not a string

for i in range(3):
    rotate_VPN(instructions) #refer to the instructions variable here
    print('\nDo whatever you want here (e.g.scraping). Pausing for 10 seconds...\n')
    time.sleep(10)

# [3] of course, you can try one of the built-in randomizers if you can't be bothered with selecting specific regions

#The following options are avilable:
#random countries X
#random countries europe X
#random countries americas X
#random countries africa east india X
#random countries asia pacific X
#random regions australia X
#random regions canada X
#random regions germany X
#random regions india X
#random regions united states X

instructions = initialize_VPN(area_input=['random countries europe 8'])

for i in range(3):
    rotate_VPN(instructions) #refer to the instructions variable here
    print('\nDo whatever you want here (e.g.scraping). Pausing for 10 seconds...\n')
    time.sleep(10)

# [4] instead of saving the instructions as a variable, you could save your settings in your work directory. Just set the save parameter to 1

initialize_VPN(save=1)

for i in range(3):
    rotate_VPN() #Call the rotate_VPN without any parameter. It will look for a settings file in your work directory
    print('\nDo whatever you want here (e.g.scraping). Pausing for 10 seconds...\n')
    time.sleep(10)

# [5] If you'd like to use an already saved settings file in your work directory (for example: a colleague/friend has sent you his/her settings file),
# use the stored settings parameter

initialize_VPN(save=1,area_input = ['random countries 20']) #save settings file to work directory
print('Imagine you close your python environment and run your script on a later date. Just load your saved settings by running the following line of code:\n')
time.sleep(7)
initialize_VPN(stored_settings=1) #the function will look for a settingsfile in your work directory, launch NordVPN, disconnect if necessary and validate the stored settings file.

for i in range(3):
    rotate_VPN()
    print('\nDo whatever you want here (e.g.scraping). Pausing for 10 seconds...\n')
    time.sleep(10)


# [6] save settings file to work directory and perform a 'complete rotation'

# --> a complete rotation will fetch a list of the currently 4000+ active available servers of NordVPN.
# The rotation will rotate between all the available servers completely by random.
# The difference with picking particular regions is that NordVPN will NOT pick the 'most appropriate' (fastest) server within a particular region when rotating.
# Instead, complete rotation will pick a specific server at random, which mens you're unlikely to revisit the same server twice in a row.
# Because of this, the 'complete rotation' option is ideal for webscraping purposes

initialize_VPN(save=1,area_input=['complete rotation'])

for i in range(3):
    rotate_VPN()
    print('\nDo whatever you want here (e.g.scraping). Pausing for 10 seconds...\n')
    time.sleep(10)

# [7] You can be as creative as you like. For example, the following code will perform an infinite loop of picking a random server every hour

instructions = initialize_VPN(area_input=['complete rotation'])

while True:
    rotate_VPN(instructions)
    time.sleep(3600)

# [8] To implement the google and youtube captcha-check, use the google_check parameter

instructions = initialize_VPN(area_input=['random regions united states 8'])

for i in range(3):
    rotate_VPN(google_check = 1)
    print('\nDo whatever you want here (e.g.scraping). Pausing for 10 seconds...\n')
    time.sleep(10)


# [9] Now you can rotate in all states in the USA with this function

def modulo_rotation_by_usa():
    timezone_language_mapping = {
        "America/New_York": ["EN-US", "en"],
        "America/Chicago": ["EN-US", "en"],
        "America/Denver": ["EN-US", "en"],
        "America/Los_Angeles": ["EN-US", "en"],
        "America/Seattle": ["EN-US", "en"],
        "America/Salt_Lake_City": ["EN-US", "en"],
        "America/San_Francisco": ["EN-US", "en"],
        "America/Dallas": ["EN-US", "en"],
        "America/Kansas_City": ["EN-US", "en"],
        "America/Saint_Louis": ["EN-US", "en"],
        "America/Atlanta": ["EN-US", "en"],
        "America/Charlotte": ["EN-US", "en"],
        "America/Miami": ["EN-US", "en"],
        "America/Manassas": ["EN-US", "en"],
        "America/Buffalo": ["EN-US", "en"],
        "America/Phoenix": ["EN-US", "en"],
    }
    vpn_options = {
        "America/New_York": ["New York,Manassas"],
        "America/Chicago": ["Chicago,Saint Louis"],
        "America/Denver": ["Denver,Chicago"],
        "America/Los_Angeles": ["Los Angeles,Phoenix"],
        "America/Seattle": ["Seattle,Vancouver"],
        "America/Salt_Lake_City": ["Salt Lake City,Denver"],
        "America/San_Francisco": ["San Francisco,Los Angeles,Salt Lake City"],
        "America/Dallas": ["Dallas,Chicago"],
        "America/Kansas_City": ["Chicago,Saint Louis"],
        "America/Saint_Louis": ["Saint Louis,Dallas"],
        "America/Atlanta": ["Atlanta,Charlotte"],
        "America/Charlotte": ["Charlotte,Manassas,New York"],
        "America/Miami": ["Miami,Atlanta,Charlotte"],
        "America/Manassas": ["Manassas,New York"],
        "America/Buffalo": ["Buffalo,New York"],
        "America/Phoenix": ["Phoenix,Los Angeles"],
        }
    def choose_timezone_and_language():
        timezone = random.choice(list(timezone_language_mapping.keys()))
        languages_stealth = timezone_language_mapping[timezone]
        languages_lang = timezone_language_mapping[timezone][1]
        return timezone, languages_stealth, languages_lang
        
    timezonex, languagesx, languages_lang = choose_timezone_and_language()
    print("Timezone selecionado:", timezonex)
    print("Idioma do stealth:", languagesx)
    print("Idioma do lang:", languages_lang)
    while True:
        start_time = time.time()
        vpn_options_for_timezone = vpn_options.get(timezonex, [])
        if vpn_options_for_timezone:
            random_a = random.random()
            if random_a > 0.5:
                vpn_option = random.choice(vpn_options_for_timezone)
            else:
                vpn_option = random.choice(vpn_options_for_timezone)
                vpn_option = random.choice(vpn_options_for_timezone)   
            try:
                print(F" Rotação de ip em progresso  ")
                vpn_instruction = initialize_VPN(area_input=[vpn_option])
                rotate_VPN(instructions=vpn_instruction)
                print(F" Rotação de ip concluida  ")
                print(F" Aguardando 10 segundos ")
                time.sleep(10)
                return True, timezonex, languagesx, languages_lang
            except Exception as e:
                print(f"Erro ao conectar via VPN: {e}")
            end_controler = time.time()
            end_fim = end_controler - start_time
            if int(end_fim) >= 20:
                continue
            print(end_fim)
            time.sleep(1)    

# [10] Now you can rotate in all states in the USA and a few more countries with this function

def modulo_rotation_by_timezone():

        timezone_language_mapping = {
            "America/New_York": ["EN-US", "en"],
            "America/Chicago": ["EN-US", "en"],
            "America/Denver": ["EN-US", "en"],
            "America/Los_Angeles": ["EN-US", "en"],
            "America/Seattle": ["EN-US", "en"],
            "America/Salt_Lake_City": ["EN-US", "en"],
            "America/San_Francisco": ["EN-US", "en"],
            "America/Dallas": ["EN-US", "en"],
            "America/Kansas_City": ["EN-US", "en"],
            "America/Saint_Louis": ["EN-US", "en"],
            "America/Atlanta": ["EN-US", "en"],
            "America/Charlotte": ["EN-US", "en"],
            "America/Miami": ["EN-US", "en"],
            "America/Manassas": ["EN-US", "en"],
            "America/Buffalo": ["EN-US", "en"],
            "America/Phoenix": ["EN-US", "en"],
            "America/Argentina/Buenos_Aires": ["ES-AR", "es"],
            "America/Sao_Paulo": ["PT-BR", "pt"],
            "America/Mexico_City": ["ES-MX", "es"],
            "America/Santiago": ["ES-CL", "es"],
            "America/Toronto": ["EN-CA", "en"],
            "America/Vancouver": ["EN-CA", "en"],
            "Europe/London": ["EN-GB", "en"],
            "Europe/Paris": ["FR-FR", "fr"],
            "Europe/Madrid": ["ES-ES", "es"],
            "Europe/Rome": ["IT-IT", "it"],
            "Australia/Sydney": ["EN-AU", "en"],
            "New_Zealand": ["EN-NZ", "en"],
            "North_America/Ottawa": ["EN-CA", "en"],
            "North_America/Havana": ["ES-CU", "es"],

        }

        vpn_options = {
            "America/New_York": ["New York,Manassas"],
            "America/Chicago": ["Chicago,Saint Louis"],
            "America/Denver": ["Denver,Chicago"],
            "America/Los_Angeles": ["Los Angeles,Phoenix"],
            "America/Seattle": ["Seattle,Vancouver"],
            "America/Salt_Lake_City": ["Salt Lake City,Denver"],
            "America/San_Francisco": ["San Francisco,Los Angeles,Salt Lake City"],
            "America/Dallas": ["Dallas,Chicago"],
            "America/Kansas_City": ["Chicago,Saint Louis"],
            "America/Saint_Louis": ["Saint Louis,Dallas"],
            "America/Atlanta": ["Atlanta,Charlotte"],
            "America/Charlotte": ["Charlotte,Manassas,New York"],
            "America/Miami": ["Miami,Atlanta,Charlotte"],
            "America/Manassas": ["Manassas,New York"],
            "America/Buffalo": ["Buffalo,New York"],
            "America/Phoenix": ["Phoenix,Los Angeles"],
            "America/Argentina/Buenos_Aires": ["Argentina,Chile"],
            "America/Sao_Paulo": ["Brazil,Argentina"],
            "America/Mexico_City": ["Mexico,Costa rica"],
            "America/Santiago": ["Chile,Argentina"],
            "America/Toronto": ["Toronto,Buffalo"],
            "America/Vancouver": ["Vancouver,Seattle"],
            "Europe/London": ["United Kingdom,Spain"],
            "Europe/Paris": ["Vancouver,Buffalo"],
            "Europe/Madrid": ["Spain,Los Angeles"],
            "Europe/Rome": ["Italy,Los Angeles"],
            "Australia/Sydney": ["New Zealand,Sydney"],
            "New_Zealand": ["New Zealand,Sydney"],
            "North_America/Ottawa": ["Vancouver,Montreal"],
            "North_America/Havana": ["Montreal,Seattle"],

        }

        def choose_timezone_and_language():
            timezone = random.choice(list(timezone_language_mapping.keys()))
            languages_stealth = timezone_language_mapping[timezone]
            languages_lang = timezone_language_mapping[timezone][1]
            return timezone, languages_stealth, languages_lang

        timezonex, languagesx, languages_lang = choose_timezone_and_language()
        print("Timezone selecionado:", timezonex)
        print("Idioma do stealth:", languagesx)
        print("Idioma do lang:", languages_lang)

        vpn_options_for_timezone = vpn_options.get(timezonex, [])
        if vpn_options_for_timezone:
            random_a = random.random()
            if random_a > 0.5:
                vpn_option = random.choice(vpn_options_for_timezone)
            else:
                vpn_option = random.choice(vpn_options_for_timezone)
                vpn_option = random.choice(vpn_options_for_timezone)   
            try:
                print(F" Rotação de ip em progresso  ")
                vpn_instruction = initialize_VPN(area_input=[vpn_option])
                rotate_VPN(instructions=vpn_instruction)
                print(F" Rotação de ip concluida  ")
                print(F" Aguardando 10 segundos ")
                time.sleep(10)
                return True, timezonex, languagesx, languages_lang
            except Exception as e:
                print(f"Erro ao conectar via VPN: {e}")
                print("Reiniciando conexão VPN...")
                terminate_VPN(instructions=vpn_instruction)
                
                timezonex, languagesx, languages_lang = choose_timezone_and_language()
                print("Timezone 2  selecionado:", timezonex)
                print("Idioma do stealth 2:", languagesx)
                print("Idioma do lang 2 :", languages_lang)

                vpn_options_for_timezone = vpn_options.get(timezonex, [])
                if vpn_options_for_timezone:
                    vpn_option = random.choice(vpn_options_for_timezone)
                    try:
                        print(F" Rotação de ip em progresso 2 ")
                        vpn_instruction2 = initialize_VPN(area_input=[vpn_option])
                        rotate_VPN(instructions=vpn_instruction2)
                        print(F" Rotação de ip concluida  2")
                        print(F" Aguardando 10 segundos 2 ")
                        time.sleep(10)
                        return True, timezonex, languagesx, languages_lang
                    except Exception as e:
                        print(f"Erro ao conectar via VPN: {e}")
                        print("Reiniciando conexão VPN...")
                        #terminate_VPN(instructions=vpn_instruction2)
                        return False    
##############
## LINUX #####
##############

# [1] Perform a complete rotation and skip the settings menu for complete automation
# the 'skip settings' parameter is only available for Linux users (since setting additional settings such as whitelisting ports is only available on Linux)

instr = initialize_VPN(area_input=['complete rotation'],skip_settings=1)

for i in range(3):
    rotate_VPN(instr)
    print('\nDo whatever you want here (e.g. scraping). Pausing for 10 seconds...\n')
    time.sleep(10)
