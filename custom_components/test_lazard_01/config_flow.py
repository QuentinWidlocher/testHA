"""Config flow for csgo_gamestate."""
from homeassistant.helpers import config_entry_flow
from .const import DOMAIN

config_entry_flow.register_webhook_flow(DOMAIN, "Webhook")
