import randomimport subprocessimport psutilimport refrom subprocess import check_output,DEVNULLimport timeimport osfrom os import pathimport platformimport urllibfrom bs4 import BeautifulSoupimport requestsimport json##########################################def additional_settings_linux(additional_settings):    try:        additional_setting_execute = str(check_output(additional_settings))    except:        additional_setting_execute = "error"    else:        pass    if "successfully" in additional_setting_execute:        settings_input_message = "\nDone! Anything else?\n"    elif additional_setting_execute == "error":        settings_input_message = "\n\x1b[93mSomething went wrong. Please consult some examples by typing 'help'\x1b[0m\n"    elif "already" in additional_setting_execute:        settings_input_message = "\nThis setting has already been executed! Anything else?\n"    else:        settings_input_message = "\n\x1b[93mNordVPN throws an unexpected message, namely:\n" + additional_setting_execute + "\nTry something different.\x1b[0m\n"    return settings_input_message##########################################def saved_settings_check(initialize=0):    print("\33[33mTrying to load saved settings...\33[0m")    try:        instructions = json.load(open("settings_nordvpn.txt"))    except FileNotFoundError:        raise Exception("\n\nSaved settings not found.\n"                        "Run initialize_VPN() first and save the settings on your hard drive or store it into a Python variable.")    else:        print("\33[33mSaved settings loaded!\n\33[0m")        if instructions['opsys'] == "Linux" and len(instructions['additional_settings'][0][0]) > 0 and initialize == 0:            print("\033[93mWarning: you've provided additional settings for the NordVPN app without executing the initialize_VPN function.\n"                "It is not certain whether these settings are in effect at the moment.\033[0m\n")    return instructions#######################################################INITIALIZE VPN#########################################################def initialize_VPN(stored_settings=0,save=0):    ###load stored settings if needed and set input_needed variables to zero if settings are provided###    if stored_settings == 1:        instructions = saved_settings_check(initialize=1)        additional_settings_needed = 0        input_needed = 0    else:        input_needed = 1        additional_settings_needed = 1        additional_settings_list = list()    ###performing system check###    opsys = platform.system()    ##windows##    if opsys == "Windows":        print("\33[33mYou're using Windows.\n"              "Performing system check...\n"              "###########################\n\33[0m")        #seek and set windows installation path#        option_1_path = 'C:/Program Files/NordVPN'        option_2_path = 'C:/Program Files (x86)/NordVPN'        custom_path = str()        if path.exists(option_1_path) == True:            cwd_path = option_1_path        elif path.exists(option_2_path) == True:            cwd_path = option_2_path        else:            custom_path = input("\x1b[93mIt looks like you've installed NordVPN in an uncommon folder. Would you mind telling me which folder? (e.g. D:/customfolder/nordvpn)\x1b[0m")            while path.exists(custom_path) == False:                custom_path = input("\x1b[93mI'm sorry, but this folder doesn't exist. Please double-check your input.\x1b[0m")            while os.path.isfile(custom_path+"/NordVPN.exe") == False:                custom_path = input("\x1b[93mI'm sorry, but the NordVPN application is not located in this folder. Please double-check your input.\x1b[0m")            cwd_path = custom_path        print("NordVPN installation check: \33[92m\N{check mark}\33[0m")        #check if nordvpn service is already running in the background        check_service = "nordvpn-service.exe" in (p.name() for p in psutil.process_iter())        if check_service is False:            raise Exception("NordVPN service hasn't been initialized, please start this service in [task manager] --> [services] and restart your script")        print("NordVPN service check: \33[92m\N{check mark}\33[0m")        # start NordVPN app and disconnect from VPN service if necessary#        print("Opening NordVPN app and disconnecting if necessary...")        open_nord_win = subprocess.Popen(["nordvpn", "-d"],shell=True,cwd=cwd_path,stdout=DEVNULL)        while ("NordVPN.exe" in (p.name() for p in psutil.process_iter())) == False:            time.sleep(3)        open_nord_win.kill()        print("NordVPN app launched: \33[92m\N{check mark}\33[0m")        print("#####################################")    ##linux##    elif opsys == "Linux":        print("\n\33[33mYou're using Linux.\n"              "Performing system check...\n"              "###########################\n\33[0m")        #check if nordvpn is installed on linux#        check_nord_linux = check_output(["nordvpn"])        if len(check_nord_linux) > 0:            print("NordVPN installation check: \33[92m\N{check mark}\33[0m")        else:            raise Exception("NordVPN is not installed on your Linux machine.\n"                  "Follow instructions on shorturl.at/ioDQ2 to install the NordVpn app.")        #check if user is logged in. If not, ask for credentials and log in or use credentials from stored settings if available.#        check_nord_linux_acc = str(check_output(["nordvpn","account"]))        if "not logged in" in check_nord_linux_acc:            if instructions['credentials'] in locals():                credentials = stored_settings['credentials']            else:                credentials = input("\n\033[34mYou are not logged in. Please provide your credentials in the form of LOGIN/PASSWORD\n\033[0m")            login = credentials.split("/")[0]            password = credentials.split("/")[1]            try:                login_nordvpn = check_output(["nordvpn","login","-u",login,"-p",password])            except subprocess.CalledProcessError:                raise Exception("\nSorry,something went wrong while trying to log in\n")            if "Welcome" in str(login_nordvpn):                pass            else:                raise Exception("\nSorry, NordVPN throws an unexpected message, namely:\n"+str(login_nordvpn))        else:            print("NordVPN login check: \33[92m\N{check mark}\33[0m")        #provide opportunity to execute additional settings.#        settings_input_message = "\n\033[34mDo you want to execute additional settings?\033[0m"        while additional_settings_needed == 1:            additional_settings = input(settings_input_message+                                        "\n_________________________\n\n"                                        "Press enter to continue\n"                                        "Type 'help' for available options\n").strip()            if additional_settings == "help":                options_linux = open("NordVPN_options/options_linux.txt", 'r').read().split('\n')                for line in options_linux:                    print(line)                additional_settings = input("").strip()            additional_settings = str(additional_settings).split(" ")            if len(additional_settings[0]) > 0:                settings_input_message = additional_settings_linux(additional_settings)                if any(re.findall(r'done|already been executed', settings_input_message,re.IGNORECASE)):                    additional_settings_list.append(additional_settings)            else:                additional_settings_needed = 0        #however, if provided, just skip the additional settings option and execute the stored settings.#        if 'instructions' in locals():            if len(instructions['additional_settings'][0][0]) > 0:                print("Executing stored additional settings....\n")                for count,instruction in enumerate(instructions['additional_settings']):                    print("Executing stored setting #"+str(count+1)+": "+instruction)                    additional_settings_linux(instruction)            else:                pass    else:        raise Exception("I'm sorry, NordVPN switcher only works for Windows and Linux machines.")    ###provide settings for VPN rotation###    ##open available options and store these in a dict##    areas_list = open("NordVPN_options/countrylist.txt", 'r').read().split('\n')    country_dict = {'countries':areas_list[0:60],'europe': areas_list[0:36], 'americas': areas_list[36:44],                    'africa east india': areas_list[49:60],'asia pacific': areas_list[49:60],                    'regions australia': areas_list[60:65],'regions canada': areas_list[65:68],                    'regions germany': areas_list[68:70], 'regions india': areas_list[70:72],                    'regions united states': areas_list[72:87],'special groups':areas_list[87:len(areas_list)]}    ##provide input if needed##    while input_needed == 1:        settings_servers = input("\n\033[34mI want to connect to...\n"                                 "_________________________\n"                                 "Type 'help' for available options\n\033[0m").strip().lower()        #define help menu#        if settings_servers.lower().strip() == 'help':            if opsys == "Windows":                notation_specific_server = " (e.g. Netherlands #742,Belgium #166)\n"            else:                notation_specific_server = " (e.g. nl742,be166)\n"            settings_servers = input("\nOptions:\n"                  "##########\n"                  "* type 'quick' to choose quickconnect \n"                  "* Single country or local region (e.g.Germany)\n"                  "* World regions (europe/americas/africa east india/asia pacific)\n"                  "* Random multiple countries and/or local regions (e.g.France,Netherlands,Chicago)\n"                  "* Random (n) countries (e.g. random countries 10)\n"                  "* Random (n) regions in country (e.g. random regions United States 6)\n"\                  "* Specialty group name (e.g. Dedicated IP,Double VPN)\n"                  "* Specific list of servers"+notation_specific_server).strip().lower()        #set base command according to running os#        if opsys == "Windows":            nordvpn_command = ["nordvpn", "-c"]        if opsys == "Linux":            nordvpn_command = ["nordvpn", "c"]        #create sample of regions from input. Pull a random sample from a larger region (or the world) if needed. Provide spelling checker and force input if needed#        if settings_servers == "quick":            quickconnect_check = input("\nYou are choosing for the quick connect option. Are you sure? (y/n)\n")            if 'y' in quickconnect_check:                sample_countries = [""]                input_needed = 0                pass        elif "#" in settings_servers or re.compile(r'^[a-zA-Z]+[0-9]+').search(settings_servers.split(',')[0]) is not None:            if opsys == "Windows":                nordvpn_command.append("-n")            sample_countries = [area.strip() for area in settings_servers.split(',')]            input_needed = 0        else:            if opsys == "Windows":                nordvpn_command.append("-g")            if "random" in settings_servers:                if "regions" in settings_servers:                    try:                        sample_countries = country_dict[re.sub("random", "", settings_servers).rstrip('0123456789.- ').lower().strip()]                        input_needed = 0                    except:                        input("\n\nThere are no specific regions available in this country, please try again.\nPress enter to continue.\n")                    if re.compile(r'[^0-9]').search(settings_servers.strip()):                        samplesize = int(re.sub("[^0-9]", "", settings_servers).strip())                        sample_countries = random.sample(sample_countries, samplesize)                else:                    if re.compile(r'[^0-9]').search(settings_servers.strip()):                        samplesize = int(re.sub("[^0-9]", "", settings_servers).strip())                        sample_countries = random.sample(country_dict['countries'], samplesize)                        input_needed = 0                    else:                        sample_countries = country_dict['countries']                        input_needed = 0            elif settings_servers in country_dict.keys():                sample_countries = country_dict[settings_servers]                input_needed = 0            else:                if settings_servers == "":                    input("\n\nYou must provide some kind of input.\nPress enter to continue and then type 'help' to view the available options.\n")                else:                    sample_countries = [area.strip() for area in settings_servers.split(',')] #take into account possible superfluous spaces#                    approved_regions = 0                    for region in sample_countries:                        if region in [area.lower() for area in areas_list]:                            approved_regions = approved_regions + 1                            pass                        else:                            input("\n\nThe region/group " + region + " is not available. Please check for spelling errors.\nPress enter to continue.\n")                    if approved_regions == len(sample_countries):                        input_needed = 0        if "instructions" not in locals():        for number,element in enumerate(sample_countries):            if element.count(" ") > 0 and opsys == "Linux":                    sample_countries[number] = re.sub(" ","_",element)            else:                pass        instructions = {'opsys':opsys,'command':nordvpn_command,'settings':sample_countries}        if opsys == "Windows":            instructions['cwd_path'] = cwd_path        if opsys == "Linux":            instructions['additional_settings'] = additional_settings_list            if 'credentials' in locals():                instructions['credentials'] = credentials        if save == 1:            print("\nSaving settings in project folder...\n")            try:                os.remove("settings_nordvpn.txt")            except FileNotFoundError:                pass            instructions_write = json.dumps(instructions)            f = open("settings_nordvpn.txt", "w")            f.write(instructions_write)            f.close()    print("\nDone!\n")    return instructions#############rotate VPN#############def rotate_VPN(instructions=None,google_check = 0):    if instructions is None:        instructions = saved_settings_check()    opsys = instructions['opsys']    command = instructions['command']    settings = instructions['settings']    if opsys == "Windows":        cwd_path = instructions['cwd_path']    for i in range(2):        try:            current_ip = new_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')        except urllib.error.URLError:            print("Can't fetch current ip. Retrying...")            time.sleep(10)            continue        else:            print("\nYour current ip-address is:", current_ip)            break    else:        raise Exception("Can't fetch current ip, even after retrying... Check your internet connection.")    for i in range(4):        if len(settings) > 1:            settings_pick = list([random.choice(settings)])        else:            settings_pick = settings        input = command + settings_pick        if settings[0] == "":            print("\nConnecting you to the best possible server (quick connect option)...")        else:            print("\n\33[34mConnecting you to", settings_pick[0], "...\n\33[0m")        try:            if opsys == "Windows":                new_connection = subprocess.Popen(input, shell=True, cwd=cwd_path)                new_connection.wait()            else:                new_connection = check_output(input)                print("Found a server! You're now on "+re.search('(?<=You are connected to )(.*)(?=\()', str(new_connection))[0].strip())        except:            print("\n An unknown error occurred while connecting to a different server! Retrying...\n")            time.sleep(15)            continue        for i in range(12):            try:                new_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')            except:                time.sleep(5)                continue            else:                if new_ip == current_ip:                    time.sleep(5)                    continue                else:                    break        else:            pass        if new_ip == current_ip:            print("ip-address hasn't changed. Retrying...\n")            time.sleep(10)            continue        else:            print("your new ip-address is:", new_ip)        if google_check == 1:            print("\n\33[33mPerforming captcha-check on Google search and Youtube...\n"                  "---------------------------\33[0m")            try:                google_search_check = BeautifulSoup(                    requests.get("https://www.google.be/search?q=why+is+python+so+hard").content,"html.parser")                youtube_video_check = BeautifulSoup(                    requests.get("https://www.youtube.com/watch?v=dQw4w9WgXcQ").content,"html.parser")                google_captcha = google_search_check.find('div',id="recaptcha")                youtube_captcha = youtube_video_check.find('div', id = "recaptcha")                if None not in (google_captcha,youtube_captcha):                    print("Google throws a captcha. I'll pick a different server...")                    time.sleep(5)                    continue            except:                print("Can't load Google page. I'll pick a different server...")                time.sleep(5)                continue            else:                print("Google and YouTube don't throw any Captcha's: \33[92m\N{check mark}\33[0m")                break        else:            break    else:        raise Exception("Unable to connect to a new server. Please check your internet connection.\n")    print("\nDone! Enjoy your new server.\n")##############################def terminate_VPN(instructions=None):    if instructions is None:        instructions = saved_settings_check()    opsys = instructions['opsys']    if opsys == "Windows":        cwd_path = instructions['cwd_path']    print("\nDisconnecting...")    if opsys == "Windows":        terminate = subprocess.Popen(["nordvpn", "-d"],shell=True,cwd=cwd_path,stdout=DEVNULL)    else:        terminate = subprocess.Popen(["nordvpn", "d"],stdout=DEVNULL)    terminate.wait()    print("Done!")