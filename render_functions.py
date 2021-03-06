from enum import Enum, auto


class RenderOrder(Enum):
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


def render_all(con, entities, player, game_map, fov_recompute, root_console, screen_width, screen_height, colours):
    # Draw all the tiles in the game map 
    if fov_recompute:
        for x, y in game_map:
            wall = not game_map.transparent[x, y]
            
            if game_map.fov[x, y]:
                if wall:
                    con.draw_char(x, y, None, fg=None, bg=colours.get('light_wall'))
                else:
                    con.draw_char(x, y, None, fg=None, bg=colours.get('light_ground'))
                    
                game_map.explored[x][y] = True
                    
            elif game_map.explored[x][y]:
                if wall:
                    con.draw_char(x, y, None, fg=None, bg=colours.get('dark_wall'))
                else:
                    con.draw_char(x, y, None, fg=None, bg=colours.get('dark_ground'))
                    
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)
        
    # Draw all entities in the list
    for entity in entities_in_render_order:
        draw_entity(con, entity, game_map.fov)
        
    con.draw_str(1, screen_height - 2, 'HP: {0:02}/{1:02}'.format(player.fighter.hp, player.fighter.max_hp))
        
    root_console.blit(con, 0, 0, screen_width, screen_height, 0, 0)
    
    
def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)
        
        
def draw_entity(con, entity, fov):
    if fov[entity.x, entity.y]:
        con.draw_char(entity.x, entity.y, entity.char, entity.colour, bg=None)
        
    
def clear_entity(con, entity):
    # erase the character that represents this object
    con.draw_char(entity.x, entity.y, ' ', entity.colour, bg=None)
    
