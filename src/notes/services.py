from fastapi import HTTPException, status
from beanie import Link, PydanticObjectId

from src.notes.models import Note
from src.notes.schemas import NoteCreateSchema, NoteReadSchema
from src.organizations.models import Organization
from src.users.models import User


class NoteService:

    async def get_organization(self, org_id):
        org = await Organization.get(org_id)
        if not org:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found")
        return org

    async def get_user(self, user_id):
        user = await User.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found")
        return user

    async def find_note(self, note_id):
        note = await Note.get(note_id)
        if not note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found")
        return note

    async def resolve_link(self, link_or_doc):
        if isinstance(link_or_doc, Link):
            return await link_or_doc.fetch()
        return link_or_doc

    async def create_note(self, org_id: PydanticObjectId,
                          user_id: PydanticObjectId,
                          data: NoteCreateSchema) -> NoteReadSchema:

        org = await self.get_organization(org_id)
        user = await self.get_user(user_id)

        user_org = await self.resolve_link(user.org)

        if str(user_org.id) != str(org.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not belong to this organization")

        # Role-based restriction
        if user.role not in ("writer", "admin"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to create notes")

        note = Note(**data.model_dump(), org=org, author=user)
        await note.insert()
        return await NoteReadSchema.from_mongo(note)

    async def list_notes(self, org_id: PydanticObjectId,
                         user_id: PydanticObjectId) -> list[NoteReadSchema]:

        org = await self.get_organization(org_id)
        user = await self.get_user(user_id)

        user_org = await self.resolve_link(user.org)

        if str(user_org.id) != str(org.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid organization or user")

        notes = await Note.find(Note.org.id == org.id).to_list()
        return [await NoteReadSchema.from_mongo(note) for note in notes]

    async def get_note(self, org_id: PydanticObjectId,
                       user_id: PydanticObjectId,
                       note_id: PydanticObjectId) -> Note:
        org = await self.get_organization(org_id)
        user = await self.get_user(user_id)
        note = await self.find_note(note_id)

        user_org = await self.resolve_link(user.org)
        note_org = await self.resolve_link(note.org)

        if str(note_org.id) != str(org.id) or str(user_org.id) != str(org.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized access")

        return await NoteReadSchema.from_mongo(note)

    async def delete_note(self, org_id: PydanticObjectId,
                          user_id: PydanticObjectId,
                          note_id: PydanticObjectId):

        _ = await self.get_organization(org_id)
        user = await self.get_user(user_id)
        note = await self.find_note(note_id)

        user_org = await self.resolve_link(user.org)
        note_org = await self.resolve_link(note.org)

        if str(user_org.id) != str(note_org.id):
            raise HTTPException(status_code=403, detail="Unauthorized access")

        if user.role != "admin":
            raise HTTPException(
                status_code=403, detail="Only admins can delete notes")

        await note.delete()
        return {"message": "Note deleted successfully"}


note_svc = NoteService()
