from queue import Queue


class Channel:
    c_id = int()
    availability = int()

    def __str__(self):
        return self.c_id.__str__() + " " + self.availability.__str__()


class History:
    v_id = int()
    layer = int()

    def __str__(self):
        return self.v_id.__str__() + " " + self.layer.__str__()


class ChannelHistory:
    c_id = int()
    history_queue = Queue()

    def __str__(self):
        return self.c_id.__str__() + " " + self.history_queue.__str__()
