module SolveDiscord where

import Prelude

import Effect (Effect)

foreign import install :: String -> String -> Effect Unit

main :: Effect Unit
main =
  install "/api/v1/challenges/attempt" "/plugins/wolf_discord/discord_url"
