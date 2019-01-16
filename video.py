class VideoBase:
    v_id = int()
    layer = 25
    popularity = float()
    frequency = 1

    def __str__(self):
        return self.v_id.__str__() + " " + self.layer.__str__() + " " + self.popularity.__str__() + " " + self.frequency.__str__()


class VideoEnhancement:
    v_id = int()
    layer = 5
    popularity = float()
    frequency = 1

    def __str__(self):
        return self.v_id.__str__() + " " + self.layer.__str__() + " " + self.popularity.__str__() + " " + self.frequency.__str__()
