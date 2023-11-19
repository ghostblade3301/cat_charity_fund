from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_project_name_duplicate,
    check_project_exists,
    check_charity_project_investition,
    check_project_for_closure,
    to_check_that_project_closed,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.finances import to_close, to_invest


router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_projects = await charity_project_crud.get_multi(session)
    return all_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    '''Только для суперюзеров.'''
    await check_project_name_duplicate(
        charity_project.name,
        session,
    )
    new_charity_project = await charity_project_crud.create(
        charity_project,
        session,
    )
    await to_invest(new_charity_project, session)
    await session.refresh(new_charity_project)
    return new_charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    '''Только для суперюзеров.'''
    charity_project = await check_project_exists(
        project_id,
        session,
    )
    await check_charity_project_investition(charity_project)
    charity_project = await charity_project_crud.delete(
        charity_project,
        session,
    )
    return charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    object_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    '''Только для суперюзеров.'''
    charity_project = await check_project_exists(
        project_id, session
    )
    await to_check_that_project_closed(charity_project)

    if object_in.name:
        await check_project_name_duplicate(object_in.name, session)

    if object_in.full_amount:
        closed_project = await check_project_for_closure(
            object_in.full_amount,
            project_id,
            session,
        )
        if closed_project:
            await to_close(charity_project)

    charity_project = await charity_project_crud.update(
        charity_project,
        object_in,
        session,
    )
    return charity_project