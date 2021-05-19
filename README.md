# Warzone Integration

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadgecustom]][hacs]

This is a warzone integration for home assistant

This integration exposes a sensor for the current battle royal data from warzone.

**This component will set up the following platforms.**

Platform | Description
-- | --
`sensor` | Show warzone battle royal stats.

## Sensors

Sensor | Description
-- | --
`sensor.warzone_cash` | Cash
`sensor.warzone_contracts` | Contracts
`sensor.warzone_deaths` | Deaths
`sensor.warzone_downs` | Downs
`sensor.warzone_gamesplayed` | Games Played
`sensor.warzone_kdratio` | Kill Death Ratio
`sensor.warzone_kills` | Kills
`sensor.warzone_level` | Current Season Level
`sensor.warzone_revives` | Revives
`sensor.warzone_score` | Score
`sensor.warzone_scoreperminute` | Score Per Minute
`sensor.warzone_timeplayed` | Time Played
`sensor.warzone_tokens` | Tokens
`sensor.warzone_topfive` | Top 5
`sensor.warzone_topten` | Top 10
`sensor.warzone_toptwentyfive` | Top 25
`sensor.warzone_wins` | Wins

## Installation

- Go to "Configuration" -> "Integrations" click "+" and search for "Warzone".

## Configuration

- Username: The email address you would use to login to https://profile.callofduty.com/
- Password: The password you would use to login to https://profile.callofduty.com/
- Platform: The platform the profile is on
- Profile: The player profile stats you want to track

>Please note the Username and password used to login does not have to be your main account. You can create a new account to access the api but then you have to either set the profile you want to track to public or add the user you are logging in from as a friend.

## Libraries

Thanks to https://github.com/EthanC/CallofDuty.py

Using this in lib because of python version mismatch. When home assistant runs on python 3.9 by default we can use this like normal.

<!---->

[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[hacsbadgecustom]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/jacokok/warzone.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/v/release/jacokok/warzone?style=for-the-badge
[releases]: https://github.com/jacokok/warzone/releases