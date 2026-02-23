from backend.utils import random_code

async def generate_user_image_name(user_id: id) -> str:
    return f"pp_{user_id:09d}_{random_code(9)}"