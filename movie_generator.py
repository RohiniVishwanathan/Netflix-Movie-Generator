import pandas as pd
import random
import pyfiglet
import time
from rich.console import Console
from rich.table import Table
from rich.style import Style
import simpleaudio as sa  # Using simpleaudio for WAV playback

# Initialize Rich console
console = Console()

# Load the cleaned Netflix dataset
df = pd.read_csv("cleaned_netflix_movies.csv")

# Define the path to the Netflix sound file (Now in WAV format)
NETFLIX_SOUND_PATH = "netflix_tadum.wav"  # Make sure this file is in your project folder

# Create Netflix-style color theme
netflix_red = Style(color="red", bold=True)

# Function to play Netflix "Ta-Dum" sound using simpleaudio
def play_intro_sound():
    try:
        wave_obj = sa.WaveObject.from_wave_file(NETFLIX_SOUND_PATH)  # Load the sound file
        play_obj = wave_obj.play()  # Play the sound
        play_obj.wait_done()  # Wait for it to finish playing
        time.sleep(1.5)  # Short delay for cinematic effect
    except Exception as e:
        console.print(f"[bold red]⚠️ Error playing sound: {e}[/bold red]")

# Function to display a Netflix-styled banner
def show_banner():
    banner = pyfiglet.figlet_format("NETFLIX MOVIE GENERATOR")
    console.print(f"[bold red]{banner}[/bold red]")

# Function to recommend a movie based on genre
def recommend_movie(genre):
    matching_movies = df[df["genres"].str.contains(genre, case=False, na=False)]

    if matching_movies.empty:
        console.print(f"[bold red]⚠️ No movies found for the genre: {genre}[/bold red]")
        return

    random_movie = matching_movies.sample(1).iloc[0]

    # Create a visually appealing table output
    table = Table(title="🎬 [bold red]Netflix Movie Recommendation[/bold red]", border_style="red")
    table.add_column("🎞 Title", style="bold white", justify="left")
    table.add_column("📅 Release Year", justify="center", style="yellow")
    table.add_column("🌎 Country", style="green")
    table.add_column("⏳ Duration (mins)", justify="right", style="cyan")

    table.add_row(
        f"[bold red]{random_movie['title']}[/bold red]", 
        f"[yellow]{random_movie['release_year']}[/yellow]", 
        f"[green]{random_movie['country']}[/green]", 
        f"[cyan]{random_movie['duration']}[/cyan]"
    )

    console.print(table)

# Main script execution
if __name__ == "__main__":
    console.print("\n" + "-" * 50, style=netflix_red)
    
    # Play the Ta-Dum sound before showing the banner
    play_intro_sound()
    
    # Show the Netflix banner after sound
    show_banner()

    console.print("\n[bold red]🎥 Welcome to the Netflix Movie Generator![/bold red]\n")
    console.print("🔴 [bold red]Pick a genre, and we’ll recommend a Netflix-style movie![/bold red] 🔴")

    while True:
        genre_input = console.input("\n🎭 [bold white]Enter a genre (or type 'exit' to quit): [/bold white]")
        if genre_input.lower() == "exit":
            console.print("\n[bold red]Goodbye! 🍿 Enjoy your movie night![/bold red] 🎬")
            break
        recommend_movie(genre_input)

