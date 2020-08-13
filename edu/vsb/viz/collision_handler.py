from Box2D import b2ContactListener


class collision_handler(b2ContactListener):
    def __init__(self, callback_parent):
        b2ContactListener.__init__(self)
        self.callback_parent = callback_parent

    def BeginContact(self, contact):
        fixture_a = contact.fixtureA
        fixture_b = contact.fixtureB

        body_a, body_b = fixture_a.body, fixture_b.body

    def EndContact(self, contact):
        pass

    def PreSolve(self, contact, oldManifold):
        pass

    def PostSolve(self, contact, impulse):
        pass
