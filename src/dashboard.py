# Datetime
from datetime import datetime

import subprocess

# Rich 
from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.live import Live

# Time
import time

# Reels-AutoPilot config and helper
import config
import helpers as Helper
import logging
logging.getLogger("moviepy").setLevel(logging.ERROR)
logging.getLogger("instagrapi").setLevel(logging.ERROR)

# Init Console
console = Console()

#load config 
Helper.load_all_config()

# APP.PY
import time
import auth


# Create the layout structure of the console
def make_layout() -> Layout:
    layout = Layout(name="root")

    layout.split(
        Layout(name="header", size=20),
        Layout(name="main", ratio=1),
    )
    layout["header"].split_row(
        Layout(name="logo", minimum_size=20),
        Layout(name="links",ratio=1, minimum_size=20)
    )
    layout["main"].split_row(
        Layout(name="side"),
        Layout(name="body", ratio=2, minimum_size=60),
    )
    layout["body"].split(Layout(name="mainBody", ratio=4), Layout(name="footer"))
    return layout


# Display the configuration values in a table
def config_table() -> Panel:

    # Load All Config
    Helper.load_all_config()
    
    table = Table(title="",padding=0,show_lines=True,expand=True)
    table.add_column("KEY", style="cyan", no_wrap=True)
    table.add_column("VALUE", style="magenta")

    table.add_row("DOWNLOAD_DIR", " "+config.DOWNLOAD_DIR)
    table.add_row("IS_REMOVE_FILES", ' [green]On[/green]' if config.IS_REMOVE_FILES == 1 else ' [red]Off[/red]')
    table.add_row("REMOVE_FILE_AFTER_MINS", " "+str(config.REMOVE_FILE_AFTER_MINS))
    table.add_row("IS_ENABLED_REELS_SCRAPER", ' [green]On[/green]' if  config.IS_ENABLED_REELS_SCRAPER  else ' [red]Off[/red]')
    table.add_row("IS_ENABLED_AUTO_POSTER", ' [green]On[/green]' if config.IS_ENABLED_AUTO_POSTER == 1 else ' [red]Off[/red]')
    table.add_row("IS_POST_TO_STORY ", ' [green]On[/green]' if config.IS_POST_TO_STORY == 1 else ' [red]Off[/red]')
    table.add_row("FETCH_LIMIT", " "+str(config.FETCH_LIMIT))
    table.add_row("POSTING_INTERVAL_IN_MIN", " "+str(config.POSTING_INTERVAL_IN_MIN))
    table.add_row("SCRAPER_INTERVAL_IN_MIN", " "+str(config.SCRAPER_INTERVAL_IN_MIN))
    table.add_row("USERNAME", " "+config.USERNAME)
    table.add_row("ACCOUNTS", " "+",".join(config.ACCOUNTS))
    table.add_row("LIKE_AND_VIEW_COUNTS_DISABLED", '[red]Disabled[/red]' if config.LIKE_AND_VIEW_COUNTS_DISABLED == 1 else ' [green]Enabled[/green]' )
    table.add_row("DISABLE_COMMENTS", ' [red]Disabled[/red]' if  config.DISABLE_COMMENTS ==1 else ' [green]Enabled[/green]' )
    table.add_row("IS_ENABLED_YOUTUBE_SCRAPING",  ' [green]On[/green]' if config.IS_ENABLED_YOUTUBE_SCRAPING == 1 else ' [red]Off[/red]')
    table.add_row("CHANNEL_LINKS", " "+",".join(config.CHANNEL_LINKS))

    message_panel = Panel(
        Align.left(
            Group("\n", Align.left(table)),
            vertical="top",
        ),
        title="[b red]Configurations",
        border_style="bright_blue",
    )
    
    return message_panel


# Display the reels status in a table
def generate_table() -> Panel:


    reels = Helper.get_reels()
    total_count = sum(1 for reel in reels)
    posted_count = sum(1 for reel in reels if reel.is_posted == 1)
    remaining_count = sum(1 for reel in reels if reel.is_posted == 0)

    title = "Total Reels : " +str(total_count) + " | Posted Reels : "+ str(posted_count)+" | Remaining to Post : "+ str(remaining_count)


    table = Table(title=title,padding=0,show_lines=True,expand=True)
    table.add_column(" ID ")
    table.add_column(" Post ID ")
    table.add_column(" Account ")
    table.add_column(" Url ")
    table.add_column(" Status ")
    table.add_column(" Posted At ")


    for reel in Helper.get_latest_ten_reels() :
        table.add_row(
            f" {reel.id} ", f" {reel.post_id} ", f" {reel.account} " ,f"[link=https://instagram.com/p/{reel.code}] View Reel ","[red] Pending " if reel.is_posted == 0 else "[green] Posted ", f" {reel.posted_at} "
        )
    
    message_panel = Panel(
        Align.center(
            Group("\n", Align.left(table)),
            vertical="top",
        ),
        box=box.ROUNDED,
        padding=(1, 2),
        title="[b red]Reels-AutoPilot Status",
        border_style="bright_blue",
    )
    return message_panel

# Count the number of posted and remaining reels
def count_reels_status(reels):
    total_count = sum(1 for reel in reels)

    if total_count == 0 :
        posted_count = 100
        remaining_count = 0
        return posted_count, remaining_count
    else :
        posted_count = sum(1 for reel in reels if reel.is_posted == 1)
        posted_count =  posted_count * 100 /total_count;
        remaining_count = sum(1 for reel in reels if reel.is_posted == 0)
        remaining_count = remaining_count * 100/ total_count;
        return posted_count, remaining_count



# Display header with clock
class Header:

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row(
            "[b]Reels-AutoPilot[/b]",
            datetime.now().ctime().replace(":", "[blink]:[/]"),
        )
        return Panel(grid, style="white on blue")



# Create a progress bar to indicate the posting progress
job_progress = Progress(
    "{task.description}",
    SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
)
task_posted = job_progress.add_task("[green]Posted", start=0)
task_remaining = job_progress.add_task("[red]Remaining", start=0)


# Display the progress footer
def progress_footer() -> Panel:

    progress_table = Table.grid(expand=True)
    progress_table.add_row(
        Panel(job_progress, title="[b][red]Posting Progress[red]", border_style="green", padding=(1, 2)),
    )

    return progress_table

# Initialize the layout
layout = make_layout()
layout["logo"].update(Helper.make_sponsor_message())
layout['links'].update(Helper.make_my_information())
layout["mainBody"].update(generate_table())
layout["side"].update(Panel(config_table(), border_style="red"))
layout["footer"].update(progress_footer())




# Function to update the live view
def update_live():
    # Update the table and layout

    reels = Helper.get_reels()
    posted_count, remaining_count = count_reels_status(reels)
    job_progress.update(task_posted, completed=posted_count)
    job_progress.update(task_remaining, completed=remaining_count)
    layout["footer"].update(progress_footer())

    live.update(layout)


# Display the live view and update it periodically
with Live(layout, refresh_per_second=1, screen=True) as live:
    try:
        while True:  # infinite loop
            
            #time.sleep(1)
            update_live()

    except KeyboardInterrupt:
        # Gracefully exit when user presses Ctrl+C
        console.print("Exiting the app. Bye!", style="green")