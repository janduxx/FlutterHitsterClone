import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Replace with your Spotify API credentials
CLIENT_ID = "28cb945996d04097b8b516575cc6322a"
CLIENT_SECRET = "210fcc76945a427982a0e08a0deacff0"

# Authenticate with Spotify (Client Credentials flow)
auth_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET
)
sp = spotipy.Spotify(auth_manager=auth_manager)


def track_name_to_uri(title: str, artist: str):
    """Search for a track URI by title and artist."""
    query = f"{title} {artist}"
    results = sp.search(q=query, type="track", limit=1)
    tracks = results.get("tracks", {}).get("items", [])
    if tracks:
        track = tracks[0]
        return track["uri"], track["name"], track["artists"][0]["name"]
    return None


def convert_json_to_uris(input_file: str, output_file: str):
    """Read songs from JSON, fetch URIs, and save them to another JSON file."""
    with open(input_file, "r", encoding="utf-8") as f:
        songs = json.load(f)

    uris = []
    for song in songs:
        title = song.get("title", "")
        artist = song.get("interpret", "")
        result = track_name_to_uri(title, artist)
        if result:
            uri, found_title, found_artist = result
            uris.append(uri)
            print(f"Found: {found_title} by {found_artist} → {uri}")
        else:
            print(f"❌ Not found: {title} by {artist}")

    # Save URIs to output JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(uris, f, indent=2)

    print(f"\n✅ Saved {len(uris)} URIs to {output_file}")


# Example usage
if __name__ == "__main__":
    convert_json_to_uris("songs.json", "uris.json")

