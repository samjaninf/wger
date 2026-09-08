# Changelog for the next release

> [!IMPORTANT]
> This release comes with some breaking changes for self-hoster. Please read carefully.

## New features


### Others
* 

### Bug fixes

* 

## New settings
*(for self-hoster)*

* 

## Breaking API changes
*(only relevant if you have your own scripts or interact with the REST API)*

## Upgrade steps

  ```bash
  docker compose pull 
  docker compose down powersync
  docker compose up -d web
  docker compose up -d powersync
  ```
