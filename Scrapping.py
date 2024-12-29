import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium_stealth import stealth
import random
import json


def autoScout(url):
    chrome_options = Options()

    # run in headless mode
    chrome_options.add_argument("--headless")

    # disable the AutomationControlled feature of Blink rendering engine
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    # start the browser window in maximized mode
    chrome_options.add_argument('--start-maximized')

    # disable extensions
    chrome_options.add_argument('--disable-extensions')

    # disable sandbox mode
    chrome_options.add_argument('--no-sandbox')

    # disable shared memory usage
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Set up the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Change the property value of the navigator for webdriver to undefined
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # Step 3: Rotate user agents
    user_agents = [
        # Add your list of user agents here
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    ]

    # select random user agent
    user_agent = random.choice(user_agents)

    # pass in selected user agent as an argument
    chrome_options.add_argument(f'user-agent={user_agent}')

    # set user agent using execute_cpd_cmd
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    driver.get(url)
    time.sleep(5)
    script_tag = driver.find_element(By.CSS_SELECTOR, 'script#__NEXT_DATA__')
    json_data = script_tag.get_attribute('innerHTML')

    # Parse the JSON data
    driver.quit()
    data = json.loads(json_data)

    image_urls = data["props"]['pageProps']['listingDetails']['images']
    price = data["props"]['pageProps']['listingDetails']['prices']['public']['priceRaw']
    manufacturer_brand = data["props"]['pageProps']['listingDetails']['vehicle']["make"]
    model = data["props"]['pageProps']['listingDetails']['vehicle']["model"]
    car_title = manufacturer_brand + " " + model
    mileage = str(data["props"]['pageProps']['listingDetails']['vehicle']['mileageInKmRaw']) + " km"
    power = data["props"]['pageProps']['listingDetails']['vehicle']["powerInKw"] + " " + data["props"]['pageProps']['listingDetails']['vehicle']["powerInHp"]
    EngineSize = data["props"]['pageProps']['listingDetails']['vehicle']['displacementInCCM']
    firstregistration = data["props"]['pageProps']['listingDetails']['vehicle']['firstRegistrationDate'][-4:]
    color = data["props"]['pageProps']['listingDetails']['vehicle']['bodyColor']
    transmission = data["props"]['pageProps']['listingDetails']['vehicle']['transmissionType']
    fuel = data["props"]['pageProps']['listingDetails']['vehicle']['fuelCategory']['formatted']

    car_features = []
    equipment_categories = ["comfortAndConvenience", "entertainmentAndMedia", "safetyAndSecurity"]
    # Loop through each category
    for category in equipment_categories:
        equipment_list = data["props"]['pageProps']['listingDetails']['vehicle']["equipment"][category]
        for item in equipment_list:
            car_features.append(item['id'])
    car_features.append(power)
    car_features.append(EngineSize)

    api_data = {
        "car_title": car_title,
        "manufacturer_brand": manufacturer_brand,
        "model": model,
        "EngineSize": EngineSize,
        "car_features": car_features,
        "car_images": image_urls,
        "car_price": price,
        "mileage": mileage,
        "fuel": fuel,
        "transmission": transmission,
        "power": power,
        "color": color,
        "firstregistration": firstregistration[-4:],
    }

    api_data["car_features"] = filter_car_features_autoScout(api_data)

    return api_data


def price_auto_scout(url):
    chrome_options = Options()

    # run in headless mode
    chrome_options.add_argument("--headless")

    # disable the AutomationControlled feature of Blink rendering engine
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    # start the browser window in maximized mode
    chrome_options.add_argument('--start-maximized')

    # disable extensions
    chrome_options.add_argument('--disable-extensions')

    # disable sandbox mode
    chrome_options.add_argument('--no-sandbox')

    # disable shared memory usage
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Set up the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Change the property value of the navigator for webdriver to undefined
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # Step 3: Rotate user agents
    user_agents = [
        # Add your list of user agents here
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    ]

    # select random user agent
    user_agent = random.choice(user_agents)

    # pass in selected user agent as an argument
    chrome_options.add_argument(f'user-agent={user_agent}')

    # set user agent using execute_cpd_cmd
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    driver.get(url)
    time.sleep(5)  # Let the page load
    script_tag = driver.find_element(By.CSS_SELECTOR, 'script#__NEXT_DATA__')
    json_data = script_tag.get_attribute('innerHTML')

    driver.quit()

    # Parse the JSON data
    data = json.loads(json_data)

    car_price = data["props"]['pageProps']['listingDetails']['prices']['public']['priceRaw']

    return car_price


def mobile_de_scrap(url):
    if "&lang=en" not in url:
        url += "&lang=en"

    chrome_options = Options()

    # run in headless mode
    chrome_options.add_argument("--headless")

    # disable the AutomationControlled feature of Blink rendering engine
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    # start the browser window in maximized mode
    chrome_options.add_argument('--start-maximized')

    # disable extensions
    chrome_options.add_argument('--disable-extensions')

    # disable sandbox mode
    chrome_options.add_argument('--no-sandbox')

    # disable shared memory usage
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Set up the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Change the property value of the navigator for webdriver to undefined
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # Step 3: Rotate user agents
    user_agents = [
        # Add your list of user agents here
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    ]

    # select random user agent
    user_agent = random.choice(user_agents)

    # pass in selected user agent as an argument
    chrome_options.add_argument(f'user-agent={user_agent}')

    # set user agent using execute_cpd_cmd
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    driver.get(url)
    time.sleep(5)
    # Wait until the script containing "__INITIAL_STATE__" is loaded
    script_tag = driver.find_element(By.XPATH, '//script[contains(text(), "__INITIAL_STATE__")]')
    script_text = script_tag.get_attribute('innerHTML')

    driver.quit()

    data = script_text.strip(" ").split(" = ")[1].split("window.__PUBLIC_CONFIG__")[0].strip(" ")
    data = json.loads(data)

    car_id = next(iter(data["search"]["vip"]["ads"]))

    attrs = data["search"]["vip"]["ads"][car_id]['data']['ad']['attributes']

    images = data["search"]["vip"]["ads"][car_id]['data']['ad']['galleryImages']
    image_urls = []

    for i in range(len(images)):
        image_urls.append(images[i]["srcSet"].split("w, ")[1].split(" ")[0])

    EngineSize = None
    mileage = None
    fuel = None
    transmission = None
    power = None
    color = None
    firstregistration = None
    sensors = None
    airbag = None
    interior = None

    # Extract attributes
    for i in range(len(attrs)):
        if attrs[i]["tag"] == "cubicCapacity":
            EngineSize = attrs[i].get("value", None)
            if EngineSize:
                EngineSize = EngineSize.replace("\xa0", " ")

        elif attrs[i]["tag"] == "mileage":
            mileage = attrs[i].get("value", None)
            if mileage:
                mileage = mileage.replace("\xa0", " ")

        elif attrs[i]["tag"] == "fuel":
            fuel = attrs[i].get("value", None)

        elif attrs[i]["tag"] == "transmission":
            transmission = attrs[i].get("value", None)

        elif attrs[i]["tag"] == "power":
            power = attrs[i].get("value", None)
            if power:
                power = power.replace("\xa0", " ")

        elif attrs[i]["tag"] == "color":
            color = attrs[i].get("value", None)

        elif attrs[i]["tag"] == "firstRegistration":
            firstregistration = attrs[i].get("value", None)

        elif attrs[i]["tag"] == "parkAssists":
            sensors = attrs[i].get("value", None)
            if sensors:
                sensors = sensors.split(", ")
                try:
                    sensors[sensors.index("Rear")] = "Rear Camera"
                except (ValueError, AttributeError):
                    pass
                try:
                    sensors[sensors.index("Front")] = "Front Camera"
                except (ValueError, AttributeError):
                    pass

        elif attrs[i]["tag"] == "airbag":
            airbag = attrs[i].get("value", None)

        elif attrs[i]["tag"] == "interior":
            interior = attrs[i].get("value", None)

    car_price = data["search"]["vip"]["ads"][car_id]['data']['ad']['price']["grossAmount"]
    manufacturer_brand = data["search"]["vip"]["ads"][car_id]['data']['ad']['make']
    model = data["search"]["vip"]["ads"][car_id]['data']['ad']['model']
    car_title = manufacturer_brand + " " + model
    sub_title = data["search"]["vip"]["ads"][car_id]['data']['ad']["subTitle"]
    car_features = data["search"]["vip"]["ads"][car_id]['data']['ad']['features']
    car_features.append(f"{EngineSize}")
    car_features.append(f"{power}")
    car_features.append(f"{interior}")
    car_features.append(f"{color}")
    car_features.append(f"{airbag}")

    api_data = {
        "car_title": car_title,
        "manufacturer_brand": manufacturer_brand,
        "model": model,
        "EngineSize": EngineSize,
        "car_features": car_features,
        "car_images": image_urls,
        "car_price": car_price,
        "mileage": mileage,
        "fuel": fuel if fuel else "Electrical",
        "transmission": transmission,
        "power": power,
        "color": color,
        "firstregistration": firstregistration[-4:],
        "sub_title": sub_title,
        "interior": interior
    }
    api_data["car_features"] = filter_car_features_mobileDE(api_data)

    return api_data


def price_mobile_de(url):
    chrome_options = Options()

    # run in headless mode
    chrome_options.add_argument("--headless")

    # disable the AutomationControlled feature of Blink rendering engine
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    # start the browser window in maximized mode
    chrome_options.add_argument('--start-maximized')

    # disable extensions
    chrome_options.add_argument('--disable-extensions')

    # disable sandbox mode
    chrome_options.add_argument('--no-sandbox')

    # disable shared memory usage
    chrome_options.add_argument('--disable-dev-shm-usage')

    # Set up the WebDriver
    driver = webdriver.Chrome(options=chrome_options)

    # Change the property value of the navigator for webdriver to undefined
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # Step 3: Rotate user agents
    user_agents = [
        # Add your list of user agents here
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    ]

    # select random user agent
    user_agent = random.choice(user_agents)

    # pass in selected user agent as an argument
    chrome_options.add_argument(f'user-agent={user_agent}')

    # set user agent using execute_cpd_cmd
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    driver.get(url)
    time.sleep(5)
    # Wait until the script containing "__INITIAL_STATE__" is loaded
    script_tag = driver.find_element(By.XPATH, '//script[contains(text(), "__INITIAL_STATE__")]')
    script_text = script_tag.get_attribute('innerHTML')

    driver.quit()

    data = script_text.strip(" ").split(" = ")[1].split("window.__PUBLIC_CONFIG__")[0].strip(" ")
    data = json.loads(data)

    car_id = next(iter(data["search"]["vip"]["ads"]))
    car_price = data["search"]["vip"]["ads"][car_id]['data']['ad']['price']["grossAmount"]

    return car_price


def domain_detector(ad_link):
    if re.search(".*?(mobile\.de)/", ad_link):
        return "SuchenMobileDe"

    elif re.search(".*?(autoscout24\.de)/", ad_link):
        return "AutoScout24De"


def filter_car_features_mobileDE(api_data):
    specs = api_data["car_features"]
    EngineSize = api_data["EngineSize"]
    power = api_data["power"]
    title = api_data["sub_title"]
    interior = api_data["interior"]
    color = api_data["color"]

    template = {
        "Comfort & Convenience": [
            'Arm rest', 'Autom. dimming interior mirror', 'Auxiliary heating', 'Cargo barrier',
            'Electric backseat adjustment', 'Electric seat adjustment', 'Electric side mirror',
            'Electric windows', 'Fold flat passenger seat', 'Heated rear seats', 'Heated seats',
            'Heated steering wheel', 'Induction charging for smartphones', 'Lumbar support',
            'Massage seats', 'Multifunction steering wheel', 'Seat ventilation', 'Sport seats'
        ],
        "Entertainment & Media": [
            'Android Auto', 'Apple CarPlay', 'Bluetooth', 'CD player', 'CD Multichanger', 'DAB radio',
            'Digital cockpit', 'Integrated music streaming', 'Navigation system', 'On-board computer',
            'Sound system', 'Tuner/Radio', 'TV', 'USB port', 'Voice control', 'WLAN/WiFi hotspot', 'Touchscreen'
        ],
        "Safety & Security": [
            'Alarm system', 'Emergency call system', 'Fatigue warning system', 'Hands-free kit',
            'Head-up display', 'Isofix', 'Paddle shifters', 'Passenger seat Isofix point', 'Driver Airbag',
            'Front Airbags', 'Front and Side Airbags', 'Front, Side and More Airbags'
        ],
        "Parking & Camera": [
            'Rear camera', 'Front camera', '360° Camera', 'Self-steering systems'
        ],
        "Performance": [
            f'{EngineSize}', f'{power}'
        ],
        "Interior": [
            "AMG", 'Leather steering wheel', 'Ambient lighting', 'Arm rest',
            'Autom. dimming interior mirror', 'Electric seat adjustment', 'Electric windows', 'Heated seats',
            'Keyless central locking', 'Multifunction steering wheel', 'Panoramic roof', 'Power Assisted Steering',
            'Sunroof', 'Paddle shifters', f"{interior}"
        ],
        "Interior Design": [
            'Passenger seat Isofix point', 'Automatic climatisation', 'Automatic climatisation, 2 zones',
            'Automatic climatisation, 3 zones', 'Automatic climatisation, 4 zones', 'Laser headlights'
        ],
        "Exterior": [
            "AMG", f'{color}', 'LED headlights', 'LED running lights', 'Alloy wheels', 'Xenon headlights',
            'All season tyres', 'Bi-xenon headlights', 'Four wheel drive', 'Roof rack', 'Spare tyre',
            'Steel wheels', 'Summer tyres', 'Winter tyres'
        ],
        "Packages": [
            'Winter package', 'Sports package', 'Interior AMG Line / interior AMG sport package',
            'Exterior AMG Line / exterior AMG sport package', 'Night Package'
        ]
    }

    ########################################################################################################

    if "AMG" in title:
        specs.append("AMG")
        specs.append('Interior AMG Line / interior AMG sport package')
        specs.append('Exterior AMG Line / exterior AMG sport package')

    ########################################################################################################

    removals = ['Isofix', 'Ski bag', "Smoker's package", 'Non-smoker vehicle', 'Disabled accessible']
    for unwanted in removals:
        if unwanted in specs:
            specs.remove(unwanted)
    ########################################################################################################

    # Normalize case
    specs = [spec.lower().capitalize() for spec in specs]
    template = {category: [item.lower().capitalize() for item in items] for category, items in template.items()}

    result = []
    used_specs = set()
    packages_content = []

    for category, items in template.items():
        matching_items = [item for item in specs if item in items]
        if matching_items:
            if category == "Packages":
                packages_content.append(category)
                packages_content.extend(matching_items)
            else:
                result.append(category)
                result.extend(matching_items)
            used_specs.update(matching_items)

    # Adding items not in the template to "Extras"
    extras = [item for item in specs if item not in used_specs]
    if extras:
        result.append("Extras")
        result.extend(extras)

    # Add "Packages" at the end
    if packages_content:
        result.extend(packages_content)

    return result


def filter_car_features_autoScout(api_data):
    specs = api_data["car_features"]
    EngineSize = api_data["EngineSize"]
    power = api_data["power"]

    template = {
        "Comfort & Convenience": [
            "Adaptive Cruise Control",
            "Air conditioning",
            "Automatic climate control",
            "Automatic climate control, 2 zones",
            "Automatic climate control, 3 zones",
            "Automatic climate control, 4 zones",
            "Electrically adjustable seats",
            "Auxiliary heating",
            "Electric backseat adjustment",
            "Electric tailgate",
            "Electrical side mirrors",
            "Heated steering wheel",
            "Hill Holder",
            "Keyless central door lock",
            "Lumbar support",
            "Massage seats",
            "Rear seat heating",
            "Seat heating",
            "Seat ventilation",
            "Sliding door",
            "Sliding door left",
            "Sliding door right",
            "Split rear seats",
            "Start-stop system",
            "Armrest",
            "4WD",
            "Air suspension",
            "Bi-Xenon headlights",
            "Full-LED headlights",
            "Glare-free high beam headlights",
            "High beam assist",
            "Sport suspension",
            "Laser headlights"
        ],
        "Entertainment & Media": [
            "Android Auto",
            "Apple CarPlay",
            "Bluetooth",
            "CD player",
            "Digital cockpit",
            "Digital radio",
            "Integrated music streaming",
            "MP3",
            "Navigation system",
            "On-board computer",
            "Radio",
            "Sound system",
            "Touch screen",
            "USB",
            "Voice Control",
            "WLAN / WiFi hotspot",
            "Television"
        ],
        "Safety & Security": [
            "ABS",
            "Adaptive headlights",
            "Alarm system",
            "Blind spot monitor",
            "Catalytic Converter",
            "Central door lock",
            "Central door lock with remote control",
            "Daytime running lights",
            "Distance warning system",
            "Driver drowsiness detection",
            "Driver-side airbag",
            "Electronic parking brake",
            "Electronic stability control",
            "Emergency brake assistant",
            "Emergency system",
            "Fog lights",
            "Immobilizer",
            "Lane departure warning system",
            "Passenger-side airbag",
            "Rear airbag",
            "Side airbag",
            "Tire pressure monitoring system",
            "Traction control",
            "Traffic sign recognition"
        ],
        "Parking & Camera": [
            "360° camera",
            "Parking assist system camera",
            "Park Distance Control",
            "Parking assist system self-steering",
            "Parking assist system sensors front",
            "Parking assist system sensors rear"
        ],
        "Performance": [
            f"{EngineSize}",
            f"{power}"
        ],
        "Interior": [
            "Ambient lighting",
            "Automatically dimming interior mirror",
            "Cargo barrier",
            "Fold flat passenger seat",
            "Leather seats",
            "Leather steering wheel",
            "Lumbar support",
            "Ski bag",
            "Heated steering wheel",
            "Armrest"
        ],
        "Exterior": [
            "Alloy wheels",
            "All season tyres",
            "Awning",
            "Bi-Xenon headlights",
            "Daytime running lights",
            "Fog lights",
            "Full-LED headlights",
            "Roof rack",
            "Spoiler",
            "Steel wheels",
            "Summer tyres",
            "Sunroof",
            "Panorama roof",
            "Tinted windows",
            "Trailer hitch",
            "Winter tyres",
            "Xenon headlights"
        ],
        "Packages": [
            "Winter package",
            "Sport package",
            "Sport seats"
        ],
        "Extras": [
            "Biodiesel conversion",
            "Disabled accessible",
            "E10-enabled",
            "Electric tailgate",
            "Hands-free equipment",
            "Induction charging for smartphones",
            "Night view assist",
            "Power windows",
            "Range extender",
            "Shift paddles",
            "Wind deflector",
            "Remote boot lid closing"
        ]
    }

    ########################################################################################################

    removals = ['Isofix', "Smoker's package"]
    for unwanted in removals:
        if unwanted in specs:
            specs.remove(unwanted)
    ########################################################################################################

    # Normalize case
    specs = [spec.lower().capitalize() for spec in specs]
    template = {category: [item.lower().capitalize() for item in items] for category, items in template.items()}

    result = []
    used_specs = set()

    for category, items in template.items():
        matching_items = [item for item in specs if item in items]
        if matching_items:
            result.append(category)
            result.extend(matching_items)
            used_specs.update(matching_items)

    # Adding items not in the template to "Extras"
    extras = [item for item in specs if item not in used_specs]
    if extras:
        result.extend(extras)

    return result
