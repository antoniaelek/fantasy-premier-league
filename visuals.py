colors = ['rgba(255, 182, 0, .9)', 'rgba(255, 0, 193, .9)', 'rgba(255, 182, 193, .9)']


def map_position_to_color(position):
    if position == 'Goalkeeper':
        return 'rgba(0,53,166, 0.4)'
    elif position == 'Defender':
        return 'rgba(101,255,71, 0.4)'
    elif position == 'Midfielder':
        return 'rgba(254,213,0, 0.4)'
    else:
        return 'rgba(236,0,0, 0.4)'
