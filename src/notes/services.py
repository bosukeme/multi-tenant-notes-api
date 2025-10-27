from beanie import PydanticObjectId

from src.utils.link_resolver import BaseService
from src.notes.models import Note
from src.notes.schemas import NoteCreateSchema, NoteReadSchema
from src.organizations.models import Organization
from src.users.models import User
from src.middlewares.errors import NoteNotFound, UnauthorizedAccess


class NoteService(BaseService):

    async def find_note(self, note_id):
        note = await Note.get(note_id)
        if not note:
            raise NoteNotFound()
        return note

    async def create_note(self,
                          org: Organization,
                          user: User,
                          data: NoteCreateSchema) -> NoteReadSchema:

        note = Note(**data.model_dump(), org=org, author=user)
        await note.insert()
        return await NoteReadSchema.from_mongo(note)

    async def list_notes(self,
                         org: Organization,
                         _: User) -> list[NoteReadSchema]:

        notes = await Note.find(Note.org.id == org.id).to_list()
        return [await NoteReadSchema.from_mongo(note) for note in notes]

    async def get_note(self,
                       org: Organization,
                       user: User,
                       note_id: PydanticObjectId) -> Note:

        note = await self.find_note(note_id)
        user_org = await self.resolve_link(user.org)
        note_org = await self.resolve_link(note.org)

        if str(note_org.id) != str(org.id) or str(user_org.id) != str(org.id):
            raise UnauthorizedAccess()

        return await NoteReadSchema.from_mongo(note)

    async def delete_note(self,
                          org: Organization,
                          user: User,
                          note_id: PydanticObjectId):

        note = await self.find_note(note_id)

        user_org = await self.resolve_link(user.org)
        note_org = await self.resolve_link(note.org)

        if str(user_org.id) != str(note_org.id):
            raise UnauthorizedAccess()

        await note.delete()
        return {"message": "Note deleted successfully"}


note_svc = NoteService()
