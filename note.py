from collections import UserDict


class Field:
    def __init__(self, value):
        # self.__value = None
        self.value = value

    # @property
    # def value(self):
    #     return self.__value

    # @value.setter
    # def value(self, value):
    #     self.__value = value

    def __str__(self):
        return str(self.value)


class Tag(Field):
    def __repr__(self):
        return str(self.value)

class Note(Field):
    def __repr__(self):
        return str(self.value)

class Record:
    def __init__(self, tags: tuple, note: str) -> None:
        self.tags = [Tag(tag) for tag in tags] if tags else []
        self.note = Note(note)

    def __str__(self):
        return f"note: {self.note}, with tags: {' '.join(str(tag) for tag in self.tags)}"


class NoteBook(UserDict):
    def add_record(self, new_note: Record) -> None:
        self.data[tuple(new_note.tags)] = new_note.note
        return f"New note: '{new_note.note}', with tags: '{', '.join(str(tag) for tag in new_note.tags)}' added successfully"


notebooks = NoteBook()
new_note_1 = Record(("#buy", "#birthday", "#grandma"), "by grandma present for her present")
new_note_2 = Record(("#fun", "#fest", "#weekend"), "sun we will went at atlas weekend")
print(new_note_1)
print(new_note_2)
print(notebooks.add_record(new_note_1))
print(notebooks.add_record(new_note_2))


for key, el in notebooks.items():
    print(key, el)

