from ecs.transition.transition_component import TransitionComponent


class TransitionSystem:
    def __init__(self, display):
        self.display = display
        self.transition = False

    def update(self, entities):
        for e in entities:
            if e.has(TransitionComponent):
                fade_state = e.get(TransitionComponent).transition
                # Fade needs to happen
                if fade_state:
                    # Fade in
                    if e.get(TransitionComponent).alpha == 255:
                        e.get(TransitionComponent).fade_state = 0
                    else:
                        e.get(TransitionComponent).alpha += 5
                        return
                else:
                    if e.get(TransitionComponent).alpha == 0:
                        e.get(TransitionComponent).fade_state = 0
                    else:
                        e.get(TransitionComponent).alpha -= 5
                        return



