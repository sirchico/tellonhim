from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json, sys, shutil
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich.text import Text
from rich.layout import Layout
from rich.padding import Padding
# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless Chrome (without GUI)
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("--disable-extensions")  # Disable extensions
chrome_options.add_argument("--disable-plugins-discovery")  # Disable plugins
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--mute-audio")  # Mute audio
chrome_options.add_argument("--disable-background-timer-throttling")
chrome_options.add_argument("--disable-backgrounding-occluded-windows")
chrome_options.add_argument("--disable-renderer-backgrounding")
chrome_options.add_argument("--disable-usb-keyboard-detect")
chrome_options.add_argument("--disable-hang-monitor")
chrome_options.add_argument("--log-level=3")  # Suppress logs
chrome_options.add_argument("--silent")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--fast-start")
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--disable-features=VizDisplayCompositor")
chrome_options.add_argument("--single-process")  # Use a single process (reduces resources but can be less stable)
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
# Custom preferences to further reduce resource usage
prefs = {
       "profile.managed_default_content_settings.images": 2,
       "profile.default_content_setting_values.notifications": 2,
       "profile.default_content_setting_values.media_stream_camera": 2,
       "profile.default_content_setting_values.media_stream_mic": 2,
       "profile.default_content_setting_values.plugins": 2,
       "profile.default_content_setting_values.popups": 2,
       "profile.default_content_setting_values.geolocation": 2,
       "profile.default_content_setting_values.auto_select_certificate": 2,
       "profile.default_content_setting_values.fullscreen": 2,
       "profile.default_content_setting_values.mouselock": 2,
       "profile.default_content_setting_values.mixed_script": 2,
       "profile.default_content_setting_values.peer_connection": 2,
       "profile.default_content_setting_values.media_stream": 2,
       "profile.default_content_setting_values.automatic_downloads": 2,
       "profile.default_content_setting_values.midi_sysex": 2,
       "profile.default_content_setting_values.push_messaging": 2,
       "profile.default_content_setting_values.ssl_cert_decisions": 2,
       "profile.default_content_setting_values.ppapi_broker": 2,
       "profile.default_content_setting_values.protectedContent": 2,
       "profile.default_content_setting_values.app_banner": 2,
       "profile.default_content_setting_values.site_engagement": 2,
       "profile.default_content_setting_values.durable_storage": 2,
   }
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)
sys.stdout.write("\033[F") #back to previous line
sys.stdout.write("\033[K") #clear line

def is_rtl(text):
    return any("\u0600" <= char <= "\u06FF" or "\u0750" <= char <= "\u077F" or "\u08A0" <= char <= "\u08FF" for char in text)

def align_reverse_text(text):
    if is_rtl(text):
        # Reverse the text and align it to the right for RTL text
        reversed_text = text[::-1]
        return Text(reversed_text, justify="right"), "right"
    else:
        return Text(text, justify="left"), "left"
def create_answer_panels(answers):
    panels = []
    for answer in answers:
        answer_info = {
            "ID": str(answer.get("id", "N/A")),
            "Answer": str(answer.get("answer", "N/A")),
            "Likes Count": str(answer.get("likesCount", "N/A")),
            "Created At": str(answer.get("createdAt", "N/A")),
            "Tell": str(answer.get("tell", "N/A")),
            "Is Liked": str(answer.get("isLiked", "N/A")),
            "User ID": str(answer.get("userId", "N/A")),
        }

        table = Table(show_lines=True, pad_edge=False, collapse_padding=True)
        table.add_column("Field", style="dim", no_wrap=True, width=15)
        table.add_column("Value", width=40)
        for field, value in answer_info.items():
            text, _ = align_reverse_text(value)
            table.add_row(field, text)

        panels.append(Panel(table, border_style="bold green"))
    return panels

def check(user):
    terminal_size = shutil.get_terminal_size()
    terminal_width = terminal_size.columns
    try:
        driver.get(f"https://api.tellonym.me/profiles/name/{user}")
        page_content = driver.page_source
        soup = BeautifulSoup(page_content, 'html.parser')
        pre_tag = soup.find('pre')
        data = json.loads(pre_tag.text)
    finally:
        driver.quit()
    # Extract necessary fields from JSON
    info = {
        "Display Name": data.get("displayName", "N/A"),
        "Username": data.get("username", "N/A"),
        "About Me": data.get("aboutMe", "N/A"),
        "Real Followers": str(data.get("followerCount", "N/A")),
        "Anonymous Followers": str(data.get("anonymousFollowerCount", "N/A")),
        "Likes Count": str(data.get("likesCount", "N/A")),
        "Answer Count": str(data.get("answerCount", "N/A")),
        "Tells Count": str(data.get("tellCount", "N/A")),
        "Is Verified": str(data.get("isVerified", "N/A")),
        "Country Code": data.get("countryCode", "N/A"),
        "Is Active": str(data.get("isActive", "N/A")),
    }
    max_field_length = max(len(field) for field in info.keys())
    max_value_length = max(len(str(value)) for value in info.values() if value is not None)
    console = Console()
    table = Table(title="User Information", header_style="bold magenta")
    table.add_column("Field", style="dim", width=max_field_length + 2, no_wrap=True)
    table.add_column("Value", width=max_value_length + 2)
    for field, value in info.items():
        table.add_row(field, value)
    console.print(table, justify="center")

    # Answers
    answers = data.get("answers", [])
    answer_panels = create_answer_panels(answers)

    # Organize panels into rows of three
    rows = []
    num_panels_per_row = 3
    for i in range(0, len(answer_panels), num_panels_per_row):
        row = answer_panels[i:i + num_panels_per_row]
        rows.append(Group(*row))

    # Combine all answer rows into a single panel
    combined_rows_panel = Panel(Group(*rows), title="Answer Details", border_style="bold")

    # Print the combined answers panel
    console.print(Align.center(combined_rows_panel))
text = "Made by Chico, you are not allowed to sell this tool."
print(' ' * ((shutil.get_terminal_size().columns - len(text)) // 2) + text + "\n")
check(input("user = "))