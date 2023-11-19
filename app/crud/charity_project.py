from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


class CRUDCharityProject(CRUDBase):
    async def get_project_id(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        '''Берёт id проекта по его имени'''
        project_id = await session.execute(
            select(
                CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        project_id = project_id.scalars().first()
        return project_id

    async def delete(
        self,
        db_project: CharityProject,
        session: AsyncSession,
    ) -> CharityProject:
        '''Удаляет проект из базы'''
        await session.delete(db_project)
        await session.commit()
        return db_project

    async def update(
        self,
        db_project: CharityProject,
        project: CharityProjectUpdate,
        session: AsyncSession,
    ) -> CharityProject:
        '''Обновляет проект в базе'''
        object_data = jsonable_encoder(db_project)
        updated_data = project.dict(exclude_unset=True)

        for field in object_data:
            if field in updated_data:
                setattr(
                    db_project,
                    field,
                    updated_data[field],
                )
        session.add(db_project)
        await session.commit()
        await session.refresh(db_project)
        return db_project


charity_project_crud = CRUDCharityProject(CharityProject)
