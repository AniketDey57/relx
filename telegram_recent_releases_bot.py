import os
import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient, events
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Set up your Telegram and Spotify credentials
api_id = '10074048'
api_hash = 'a08b1ed3365fa3b04bcf2bcbf71aff4d'
bot_token = '6325844279:AAFpFPp-M9rzG5nh5ZDxNTA0GuMUBCkk7oI'
spotify_client_id = 'bd053f80b2a94d11a4ea5ef4daeb7d41'
spotify_client_secret = '9bcd116aee624d55b1933b5f2b8ffa4c'
redirect_uri = 'http://localhost:8888/callback'

# Initialize Telegram client
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Initialize Spotify client with user authentication
scope = "user-follow-read"
sp = Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                       client_secret=spotify_client_secret,
                                       redirect_uri=redirect_uri,
                                       scope=scope))

@client.on(events.NewMessage(pattern='/recent_releases'))
async def recent_releases(event):
    # Calculate the date range (past week)
    today = datetime.now()
    last_week = today - timedelta(days=7)

    # Get followed artists
    followed_artists = sp.current_user_followed_artists(limit=5000)
    artist_ids = [artist['id'] for artist in followed_artists['artists']['items']]

    message = "Recent Releases from Followed Artists:\n\n"

    # Loop through each followed artist
    for artist_id in artist_ids:
        # Fetch albums of the artist
        albums = sp.artist_albums(artist_id, album_type='album', limit=50)
        
        for album in albums['items']:
            # Check if the album release date is within the past week
            release_date = album['release_date']
            if datetime.strptime(release_date, '%Y-%m-%d') >= last_week:
                message += f"Album: {album['name']}\n"
                message += f"Artist: {album['artists'][0]['name']}\n"
                message += f"Release Date: {release_date}\n"
                message += f"Link: {album['external_urls']['spotify']}\n\n"

    if message == "Recent Releases from Followed Artists:\n\n":
        message = "No recent releases found for followed artists."
        
    await event.respond(message)

# Start the bot
async def main():
    await client.start()
    print("Bot is running...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
