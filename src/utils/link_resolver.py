from beanie import Link


class BaseService:
    async def resolve_link(self, link_or_doc):
        if isinstance(link_or_doc, Link):
            return await link_or_doc.fetch()
        return link_or_doc
