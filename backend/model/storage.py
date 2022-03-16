rooms = []


def add_room(room):
    global rooms
    room.id = str(len(rooms) + 1)
    rooms.append(room)
    print("IN add_room - room: ", room)
    return room


def get_rooms():
    global rooms
    print("IN get_rooms - rooms: ", rooms)
    return rooms


def remove_room(id):
    global rooms
    for room in rooms:
        if room.id == id:
            print("IN remove_room - room: ", room)
            del room
    print("IN remove_room - not found room with id: ", id)


def get_room_by_id(id):
    global rooms
    for room in rooms:
        if room.id == id:
            print("IN get_room_by_id - room: ", room)
            return room
    print("IN get_room_by_id - not found room with id: ", id)
    return None
