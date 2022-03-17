rooms = {}


def add_room(room):
    global rooms
    i = str(len(rooms) + 1)
    rooms[i] = {
        'id': i,
        'contractAddress': ''
    }
    print("IN add_room - room: ", room)
    return room


def get_rooms():
    global rooms
    print("IN get_rooms - rooms: ", rooms)
    return list(rooms.items())


def remove_room(id):
    global rooms
    del rooms[id]
    print("IN remove_room - not found room with id: ", id)


def get_room_by_id(id):
    global rooms
    if id in rooms:
        print("IN get_room_by_id - room: ", rooms[id])
        return rooms[id]
    print("IN get_room_by_id - not found room with id: ", id)
    return None


def upd_room_data_by_id(id, upd):
    global rooms
    rooms[id].update(upd)
    print("IN get_room_by_id - not found room with id: ", id)
    return None
