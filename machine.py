class Content:
    v_id = int()
    layer_id = int()

    def __str__(self):
        return self.v_id.__str__() + " " + self.layer_id.__str__()


class Distance:
    index = int()
    distance = float()

    def __str__(self):
        return self.index.__str__() + " " + self.distance.__str__()


class Machine:
    m_id = int()
    x = int()
    y = int()
    cache_size = 0
    contents = []
    channel = int

    def __str__(self):
        return self.m_id.__str__() + " " + self.x.__str__() + " " + self.y.__str__() + " " + self.channel.__str__()
