from fastapi import APIRouter, Header, status

from beanie import PydanticObjectId
from src.notes.schemas import NoteCreateSchema, NoteReadSchema
from src.notes.services import note_svc

note_router = APIRouter()

# Custom headers: X-Org-ID and X-User-ID


@note_router.post("/", response_model=NoteReadSchema,
                  status_code=status.HTTP_201_CREATED)
async def create_note(
    payload: NoteCreateSchema,
    x_org_id: PydanticObjectId = Header(..., alias="X-Org-ID"),
    x_user_id: PydanticObjectId = Header(..., alias="X-User-ID")
):
    note = await note_svc.create_note(x_org_id, x_user_id, payload)
    return note


@note_router.get("/", response_model=list[NoteReadSchema])
async def list_notes(
    x_org_id: PydanticObjectId = Header(..., alias="X-Org-ID"),
    x_user_id: PydanticObjectId = Header(..., alias="X-User-ID")
):
    notes = await note_svc.list_notes(x_org_id, x_user_id)
    return notes


@note_router.get("/{note_id}", response_model=NoteReadSchema)
async def get_note(
    note_id: PydanticObjectId,
    x_org_id: PydanticObjectId = Header(..., alias="X-Org-ID"),
    x_user_id: PydanticObjectId = Header(..., alias="X-User-ID")
):
    note = await note_svc.get_note(x_org_id, x_user_id, note_id)
    return note


@note_router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: PydanticObjectId,
    x_org_id: PydanticObjectId = Header(..., alias="X-Org-ID"),
    x_user_id: PydanticObjectId = Header(..., alias="X-User-ID")
):
    await note_svc.delete_note(x_org_id, x_user_id, note_id)
    return {"message": "Note deleted successfully"}
