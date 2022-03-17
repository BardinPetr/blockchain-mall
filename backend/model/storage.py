from error.exceptions import RoomNotExistsError, TicketNotExistsError

rooms = {}
tickets = {}
sign = 0
sign1 = 0


def add_room(room):
    global rooms
    i = str(len(rooms) + 1)
    room['id'] = i
    room['contractAddress'] = ''
    rooms[i] = room
    print("IN add_room - room: ", str(room))
    return room


def get_rooms():
    global rooms
    print("IN get_rooms - rooms: ", str(rooms))
    return list(rooms.values())


def remove_room(id):
    global rooms
    if id in rooms:
        room = rooms[id]
        del rooms[id]
        print("IN remove_room - removed room: " + str(room) + " with id: ", id)
        return room

    print("IN remove_room - not found room with id: ", id)
    raise RoomNotExistsError("Room with such ID not found")


def get_room_by_id(id):
    global rooms
    if id in rooms:
        print("IN get_room_by_id - room: ", str(rooms[id]))
        return rooms[id]

    print("IN get_room_by_id - not found room with id: ", id)
    raise RoomNotExistsError("Room with such ID not found")


def upd_room_data_by_id(id, upd):
    global rooms
    if id in rooms:
        rooms[id].update(upd)
        print("IN upd_room_data_by_id - updated room: " + str(rooms[id]) + " with id: ", id)
        return rooms[id]

    print("IN upd_room_data_by_id - not found room with id: ", id)
    raise RoomNotExistsError("Room with such ID not found")


def set_sign(_sign):
    global sign
    sign = _sign


def get_sign():
    global sign
    return sign


def set_sign1(_sign1):
    global sign1
    sign1 = _sign1


def get_sign1():
    global sign1
    return sign1


def add_ticket(ticket):
    global tickets
    i = str(len(tickets) + 1)
    ticket['id'] = i
    tickets[i] = ticket
    print("IN add_ticket - ticket: ", str(ticket))
    return ticket


def get_tickets():
    global ticket
    print("IN get_tickets - ticket: ", str(ticket))
    return list(ticket.values())


def remove_ticket(id):
    global tickets
    if id in tickets:
        ticket = tickets[id]
        del tickets[id]
        print("IN remove_ticket - removed ticket: " + str(ticket) + " with id: ", id)
        return ticket

    print("IN remove_ticket - not found ticket with id: ", id)
    raise TicketNotExistsError()


def get_ticket_by_id(id):
    global tickets
    if id in tickets:
        print("IN get_ticket_by_id - ticket: ", str(tickets[id]))
        return tickets[id]

    print("IN get_ticket_by_id - not found ticket with id: ", id)
    raise TicketNotExistsError()


def upd_ticket_data_by_id(id, upd):
    global tickets
    if id in tickets:
        tickets[id].update(upd)
        print("IN upd_ticket_data_by_id - updated ticket: " + str(tickets[id]) + " with id: ", id)
        return tickets[id]

    print("IN upd_ticket_data_by_id - not found ticket with id: ", id)
    raise TicketNotExistsError()