def adjust_game(game, partner_skill):
    """Change the start, preserving the user's role and objective."""
    return {**game, 'adjusted_start': game['partner_variants'][partner_skill]}
