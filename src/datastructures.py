
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._members = [{
            "id": self._generateId(),
            "first_name": "",
            "last_name": last_name,
            "age": 0
        }]

        # example list of members
        self._members = [{"id": 1, "first_name": "Mary", "last_name": "leyva", "age": 28}]

    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        return randint(0, 100)

    def add_member(self, member):
        # fill this method and update the return
        member = {
            "id": self._generateId(),
            "first_name": member.first_name,
            "last_name": member.last_name,
            "age": member.age}
        self._members.append(member)
        return member    

    def delete_member(self, id):
        # fill this method and update the return
        member = list(filter(lambda item: item["id"] == id, self._members))
        obj = self.get_member(id)
        obj.delete(dict(member))
        return self._members

    def get_member(self, id):
        # fill this method and update the return
        member = list(filter(lambda item: item["id"] == id, self._members))
        return member[0]

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members

    def update_member(self, id, member):
        obj = self.get_member(id)
        obj.update(dict(member))
        return obj