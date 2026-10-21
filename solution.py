import heapq


class Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=0, value=0):
        self.key, self.value = key, value
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self.capacity = capacity
        self.map = {}
        # sentinels: head.next is most recent, tail.prev is least recent
        self.head, self.tail = Node(), Node()
        self.head.next, self.tail.prev = self.tail, self.head

    def _remove(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _add_front(self, node):
        node.prev, node.next = self.head, self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        node = self.map.get(key)
        if node is None:
            return -1
        self._remove(node)
        self._add_front(node)
        return node.value

    def put(self, key, value):
        node = self.map.get(key)
        if node:
            node.value = value
            self._remove(node)
            self._add_front(node)
            return
        if len(self.map) == self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.map[lru.key]
        node = Node(key, value)
        self.map[key] = node
        self._add_front(node)


def can_attend_all(events):
    ev = sorted(events)
    return all(ev[i][1] <= ev[i + 1][0] for i in range(len(ev) - 1))


def min_rooms_required(events):
    if not events:
        return 0
    starts = sorted(s for s, _ in events)
    ends = sorted(e for _, e in events)
    rooms = best = j = 0
    for s in starts:
        while ends[j] <= s:  # a meeting ending at s frees its room first
            j += 1
            rooms -= 1
        rooms += 1
        best = max(best, rooms)
    return best


def assign_rooms(events):
    """Returns {event_index: 'Room A'...}; reuses the earliest-free room."""
    order = sorted(range(len(events)), key=lambda i: events[i])
    busy, free, out, n = [], [], {}, 0  # busy: (end, room_id); free: heap of ids
    for i in order:
        s, e = events[i]
        while busy and busy[0][0] <= s:
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            r = heapq.heappop(free)
        else:
            r, n = n, n + 1
        out[i] = "Room " + chr(ord("A") + r) if r < 26 else f"Room {r + 1}"
        heapq.heappush(busy, (e, r))
    return out


if __name__ == "__main__":
    c = LRUCache(2)
    c.put(1, 1); c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)
    assert c.get(2) == -1
    c.put(4, 4)
    assert c.get(1) == -1 and c.get(3) == 3 and c.get(4) == 4
    c.put(3, 30); assert c.get(3) == 30
    assert can_attend_all([(9, 10), (10, 11), (11, 12)])
    assert not can_attend_all([(9, 11), (10, 12)])
    assert can_attend_all([])
    assert min_rooms_required([(9, 10), (10, 11), (11, 12)]) == 1
    assert min_rooms_required([(0, 30), (5, 10), (15, 20)]) == 2
    assert min_rooms_required([(1, 5), (2, 6), (3, 7)]) == 3
    assert min_rooms_required([]) == 0
    print(assign_rooms([(0, 30), (5, 10), (15, 20)]))
    print("ok")
