from Box2D import b2ContactListener


class collision_handler(b2ContactListener):
    def __init__(self, callback_parent):
        b2ContactListener.__init__(self)
        self.callback_parent = callback_parent

    def BeginContact(self, contact):
        fixture_a = contact.fixtureA
        fixture_b = contact.fixtureB
        body_a, body_b = fixture_a.body.userData.get_obj_code(), fixture_b.body.userData.get_obj_code()
        if body_a == 200 or body_b == 200:
            if body_a == 400 or body_b == 400:
                print("agent, static")
                self.callback_parent.collision_detected = True
            elif body_a == 500 or body_b == 500:
                print("agent, dynamic")
                self.callback_parent.collision_detected = True
            elif body_a == 100 or body_b == 100:
                print("agent, walls")
                self.callback_parent.collision_detected = True
            elif body_a == 300 or body_b == 300:
                print("agent, target")
                self.callback_parent.reached_target = True

    def EndContact(self, contact):
        pass

    def PreSolve(self, contact, oldManifold):
        pass

    def PostSolve(self, contact, impulse):
        pass
