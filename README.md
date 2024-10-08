# BBC to Spotify

Want to listen to whatever your favourite BBC radio station is playing, without all the conversational interludes?

This tool grabs the current playlist for a given BBC radio station, and uses these songs to create or update a Spotify playlist of your choice.

It works for: BBC Radio 1, BBC Radio 1 Xtra, BBC Radio 2, BBC Radio 6 Music, and BBC Asian Network.

## Contents

<!-- vim-markdown-toc GFM -->

* [Requirements](#requirements)
* [Installation](#installation)
* [Configuration](#configuration)
    * [Create a Spotify app](#create-a-spotify-app)
    * [Authorize the CLI](#authorize-the-cli)
* [Usage](#usage)
    * [Authorization](#authorization)
    * [Creating a playlist](#creating-a-playlist)
    * [Updating a playlist](#updating-a-playlist)
* [FAQ](#faq)
    * [How can I find a playlist's ID?](#how-can-i-find-a-playlists-id)
    * [I don't want to store my credentials. Can I still use the CLI?](#i-dont-want-to-store-my-credentials-can-i-still-use-the-cli)
    * [What permission scopes are provided to the CLI?](#what-permission-scopes-are-provided-to-the-cli)

<!-- vim-markdown-toc -->

## Requirements

1. Nix

- Installable here: https://nixos.org/download.
- Ensure nix-command and flakes are enabled. Instructions here: https://nixos.wiki/wiki/Flakes.

2. A Spotify account

## Installation

- Enter a temporary nix shell with `bbc-to-spotify` installed:

```bash
nix shell github:archie-judd/bbc-to-spotify
```

- Install imperatively:

```bash
nix profile install github:archie-judd/bbc-to-spotify
```

- Install declaratively with a flake:

For example: https://nixos-and-flakes.thiscute.world/nixos-with-flakes/nixos-flake-and-module-system#install-system-packages-from-other-flakes.

---

Check install was successful by running the following command:

```bash
bbc-to-spotify --version
```

## Configuration

### Create a Spotify app

You need to create a Spotify app to generate client credentials that will be required for authorizing the CLI.

You can follow the steps here: https://developer.spotify.com/documentation/web-api/concepts/apps.

When asked for a redirect URI, it is recommended to use the following value, however you may use a different one if you would like.

```
http://localhost:8080/bbc-to-spotify
```

### Authorize the CLI

This process will generate a refresh token, and optionally store it with your client credentials in your home folder for future authentication.

Start the authorization helper by running:

```shell
bbc-to-spotify authorize
```

> See [Authorization](#authorization) for help on the authorize command.

You will be prompted for your client ID and client secret. You can copy them from your app's page.

You will then be taken through the steps to generate a refresh token, and asked if your credentials may be stored for future authentication.

> See [I don't want to store my credentials. Can I still use the CLI?](#i-dont-want-to-store-my-credentials-can-i-still-use-the-cli) if you want to use the CLI without storing your credentials.

## Usage

CLI commands take the following format.

```
bbc-to-spotify <command> [arguments]
```

Run `bbc-to-spotify <command> -h` for information on a specific command.

The available commands are: `authorize`, `create-playlist` and `update-playlist`.

### Authorization

`authorize` runs the authorization process to generate credentials that will be needed to run the `create-playlist` and `update-playlist` commands.

```
bbc-to-spotify authorize [options]
```

**Options**

`--redirect-uri <value>` (string):

> Redirect URI to use during authorization. Default value is `http://localhost:8080/bbc-to-spotify`.

`--verbose`, `-v` (flag):

> Increase the logging verbosity logging (`-vv` to increase further).

`--quiet`, `-q` (flag):

> Decrease the verbosity of logging (`-qq` to decrease further).

`--log-file <filepath>` (string):

> Write logs to this file. Suppresses logging in stdout.

### Creating a playlist

`create-playlist` is used to create a new Spotify playlist with songs from a BBC radio station's current playlist.

```
bbc-to-spotify create-playlist <name> <source> [options]
```

**Required arguments**

`name` (string):

> The name of the playlist to be created.

`source` (string):

> The BBC Radio station whose current playlist should be added to the Spotify playlist.
>
> Possible values:\
> `radio-1`\
> `radio-1-xtra`\
> `radio-2`\
> `radio-6`\
> `bbc-asian-network`

**Options**

`--dry-run` `-n` (flag):

> Run the command but do not create the destination playlist.

`--private`, `-p` (flag):

> Make the playlist private rather than public.

`--desc <description>` (string):

> The description to add to the destination playlist.

`--verbose`, `-v` (flag):

> Increase logging verbosity (`-vv` to increase further).

`--quiet`, `-q` (flag):

> Decrease logging verbosity (`-qq` to decrease further).

`--log-file <filepath>` (string):

> Write logs to this file. Suppresses logging in stdout.

### Updating a playlist

`update-playlist` is used to update an existing Spotify playlist with songs from a BBC radio station's current playlist.

```
bbc-to-spotify update-playlist <playlist-id> <source> [options]
```

**Required arguments**

`playlist-id` (string):

> The ID of the Spotify playlist on which to add the BBC station's current playlist tracks.

`source` (string):

> The BBC Radio station whose current playlist should be added to the Spotify playlist.
>
> Possible values:\
> `radio-1`\
> `radio-1-xtra`\
> `radio-2`\
> `radio-6`\
> `bbc-asian-network`

**Options**

`--dry-run` `-n` (flag):

> Run the command but do not update the destination playlist.

`--no-dups` `-N` (flag):

> Only add tracks that are not already in the destination playlist.

`--prune` `-p` (flag):

> Remove all duplicates and any tracks that are not in the source playlist.

`--prepend` `-P` (flag):

> Add new tracks to the beginning of the playlist (default behaviour is to add them at the end).

`--update-desc` `-u` (flag):

> Add a 'Last updated' timestamp to the destination playlist description.

`--verbose`, `-v` (flag):

> Increase logging verbosity (`-vv` to increase further).

`--quiet`, `-q` (flag):

> Decrease logging verbosity (`-qq` to decrease further).

`--log-file <filepath>` (string):

> Write logs to this file. Suppresses logging in stdout.

## FAQ

### How can I find a playlist's ID?

The playlists ID should be printed out after successfully executing the `create-playlist` command.

Alternatively you can get a Spotify playlist ID by clicking `...` on the playlist's page, and then clicking `Copy link to playlist` under the `Share` menu.

This will give you a full playlist link that looks like the following:

`https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U?si=9f6A6U2jTk-njyZJ64rk3g`

The playlist ID is the code after `playlist/` and before `?si` (`37i9dQZF1DWXRqgorJj26U`).

### I don't want to store my credentials. Can I still use the CLI?

Yes. You can then authorize `bbc-to-spotify` by setting the following environment variables before use: `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `SPOTIFY_REFRESH_TOKEN`.

You can get a refresh token by running `bbc-to-spotify authorize` and pressing `N` when asked to store credentials.

### What permission scopes are provided to the CLI?

The scopes `modify-playlist-public`and `modify-playlist-private` are provided. See more about scopes here: https://developer.spotify.com/documentation/web-api/concepts/scopes.
