class SonicEvent:
    def __init__(self, h, g, u, offset=0, track=0, channel=0):
        self.h = h
        self.g = g
        self.u = u
        self.offset = offset
        self.track = track #if h>=0 else 1
        self.channel = channel

    def assign_offset(self, o):
        self.offset = o
    
    def __eq__(self, other):
        return (self.h==other.h)and(self.u==other.u)
    
    def __str__(self):
        return "Sonic Event: \n<h,g,u>: " + str(self.h)+', '+str(self.g)+', '+str(self.u) +'\nOffset: ' + str(self.offset) + '\n'
