import asyncio
from app.db.session import AsyncSessionLocal
from app.auth.models import User
from sqlalchemy import select, update

async def promote():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).where(User.email=='testuser@example.com'))
        user = result.scalars().first()
        if user:
            user.is_superuser = True
            await db.commit()
            print('User promoted to Admin!')
        else:
            print('User not found.')

if __name__ == "__main__":
    asyncio.run(promote())
