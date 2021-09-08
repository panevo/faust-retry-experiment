import logging
import json
from app import app

from .models import PageView

page_view_topic = app.topic("page_views", value_type=PageView)
hello_world_topic = app.topic("hello_world")

page_views = app.Table("page_views", default=int)

logger = logging.getLogger(__name__)


# @app.agent(page_view_topic)
# async def downtime_notification(stream):
#     async for event in stream.events():

#         async with event:
#             logger.info(f"Notification received with id={event.value.id}")

#             if int(event.value.id) % 2 == 0:
#                 logger.info(f"Acknowledge {event.value.id}")
#                 # await event.ack()
#             else:
#                 raise Exception("Task failed")

#             yield None


@app.agent(page_view_topic)
async def downtime_notification(stream):
    async for event in stream.noack().events():

        logger.info(f"Notification received with id={event.value.id}, retry={event.value.retry}")

        if int(event.value.id) % 2 == 0:
            logger.info(f"Acknoledge {event.value.id}")
            event.ack()
        else:
            await page_view_topic.send(key=event.value.id, value=PageView(**{"id": event.value.id, "user": event.value.user, "retry": event.value.retry+1}))
    
        yield event


# @app.agent(page_view_topic)
# async def count_page_views(views):
#     async for view in views.group_by(PageView.id):
#         logger.info(f"Event received. Page view Id {view.id}")

#         yield view


# @app.timer(interval=3.0)
# async def producer():
#     await hello_world_topic.send(key="faust", value=b'{"message": "Hello world! (Faust Version)"}')


@app.agent(hello_world_topic)
async def consumer(events):
    async for event in events:
        logger.info(event)

        yield event
