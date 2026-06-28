from flask import jsonify
from CTFd.models import Challenges, Solves
from CTFd.plugins import register_plugin_assets_directory
from CTFd.utils.decorators import authed_only
from CTFd.utils.user import get_current_user

DISCORD_CHALLENGE_NAME = "disc0rd"
DISCORD_URL = "https://discord.gg/UkU85VvZx"
SCRIPT_TAG = (
    '<script defer src="/plugins/wolf_discord/assets/solve-discord.js"></script>'
)


def _inject_script(response):
    if response.mimetype != "text/html":
        return response

    body = response.get_data(as_text=True)
    if SCRIPT_TAG in body:
        return response

    if "</body>" in body:
        body = body.replace("</body>", f"{SCRIPT_TAG}</body>", 1)
    else:
        body = f"{body}{SCRIPT_TAG}"

    response.set_data(body)
    return response


def load(app):
    register_plugin_assets_directory(
        app,
        base_path="/plugins/wolf_discord/assets/",
        endpoint="wolf_discord_assets",
    )
    app.after_request(_inject_script)

    @app.route("/plugins/wolf_discord/discord_url")
    @authed_only
    def discord_url():
        user = get_current_user()

        challenge = Challenges.query.filter_by(
            name=DISCORD_CHALLENGE_NAME
        ).first()

        if challenge is None:
            return jsonify({"success": False, "error": "challenge_not_found"}), 404

        solve = Solves.query.filter_by(
            user_id=user.id,
            challenge_id=challenge.id,
        ).first()

        if solve is None:
            return jsonify({"success": False, "error": "not_solved"}), 403

        return jsonify({
            "success": True,
            "url": DISCORD_URL,
        })
