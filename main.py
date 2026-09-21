from nicegui import ui

from database import engine, Base
from ui.dashboard import dashboard


Base.metadata.create_all(engine)

dashboard()

ui.run()