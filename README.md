# Warzone Integration

[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]

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

1. Go to "Configuration" -> "Integrations" click "+" and search for "Warzone".

## Libraries

Thanks to https://github.com/EthanC/CallofDuty.py

Using this in lib because of python version mismatch. When home assistant runs on python 3.9 by default we can use this like normal.

<!---->

[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/jacokok/warzone.svg?style=for-the-badge