from fastapi import APIRouter, Request, status, Depends
from beanie import PydanticObjectId

from src.dependencies.tenant import TenantContext
from src.dependencies.rbac import require_role
from src.notes.schemas import NoteCreateSchema, NoteReadSchema
from src.notes.services import note_svc

tenant_ctx = TenantContext()

note_router = APIRouter()


@note_router.post("/", response_model=NoteReadSchema,
                  status_code=status.HTTP_201_CREATED)
async def create_note(request: Request,
                      payload: NoteCreateSchema,
                      ctx=Depends(require_role("writer", "admin")),
                      ):

    org = ctx["org"]
    user = ctx["user"]

    note = await note_svc.create_note(org, user, payload)
    return note


@note_router.get("/", response_model=list[NoteReadSchema])
async def list_notes(request: Request, ctx=Depends(
        require_role("reader", "writer", "admin"))):

    org = ctx["org"]
    user = ctx["user"]

    notes = await note_svc.list_notes(org, user)
    return notes


@note_router.get("/{note_id}", response_model=NoteReadSchema)
async def get_note(request: Request, note_id: PydanticObjectId,
                   ctx=Depends(require_role("reader", "writer", "admin"))):
    org = ctx["org"]
    user = ctx["user"]
    note = await note_svc.get_note(org, user, note_id)
    return note


@note_router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(request: Request, note_id: PydanticObjectId,
                      ctx=Depends(require_role("admin"))):
    org = ctx["org"]
    user = ctx["user"]

    await note_svc.delete_note(org, user, note_id)
    return {"message": "Note deleted successfully"}
