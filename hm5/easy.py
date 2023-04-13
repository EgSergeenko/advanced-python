import asyncio
import os
import random

from aiohttp import ClientSession

URL_TEMPLATE = 'https://picsum.photos/id/{image_id}/536/354.jpg'
MIN_IMAGE_ID, MAX_IMAGE_ID = 0, 1084


async def parse_images(
    url: str,
    n: int,
    output_dir: str,
    loop: asyncio.AbstractEventLoop,
) -> None:
    async with ClientSession(loop=loop) as session:
        image_ids = random.sample(range(MIN_IMAGE_ID, MAX_IMAGE_ID), n)
        urls = [url.format(image_id=image_id) for image_id in image_ids]
        tasks = [parse_image(session, url) for url in urls]
        images = await asyncio.gather(*tasks)

    for idx, image in enumerate(images):
        image_path = os.path.join(
            output_dir, '{idx}.jpg'.format(idx=idx),
        )
        with open(image_path, 'wb') as image_file:
            image_file.write(image)


async def parse_image(session: ClientSession, url: str) -> bytes:
    async with session.get(url) as response:
        return await response.content.read()


if __name__ == '__main__':
    output_dir = 'artifacts/easy'
    os.makedirs(output_dir, exist_ok=True)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(
        parse_images(URL_TEMPLATE, 3, output_dir, loop),
    )

    loop.close()
