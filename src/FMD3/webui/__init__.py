from nicegui import ui

from FMD3.Core import database
from FMD3.Core.database import Session
from FMD3.Core.database.predefined import max_chapter_number
from FMD3.Core.settings import Settings
from FMD3.Models.Chapter import Chapter
from FMD3.Sources import get_source, load_sources



Settings()
# Session = scoped_session(session_factory)
series_id = "3d269f6e-10e1-4e4c-b453-48b38814494a"
data =  [{"series_name":chapter.series.title,"ch_n":chapter.number, "vol_n":chapter.volume,"title":chapter.title} for chapter in Session.query(database.DLDChapters).all()]
last_chapter = max_chapter_number(series_id)
md_data = get_source("MangaDex").get_new_chapters("3d269f6e-10e1-4e4c-b453-48b38814494a",last_chapter)
series = Session.query(database.Series).filter_by(series_id=series_id).one()

with ui.row():
    with ui.column():
        ui.label("Downloaded")
        ui.aggrid({
        # 'defaultColDef': {'flex': 1},
        'columnDefs': [
            {'headerName': 'Name', 'field': 'series_name'},
            {'headerName': 'Chapter', 'field': 'ch_n'},
            {'headerName': 'Volume', 'field': 'vol_n'},
            {'headerName': 'Title', 'field': 'title'},
        ],
        'rowData':data
    }).style('width: 400px; height: 800px')
    with ui.column():
        ui.label("Available")
        ui.button("Download selected")
        ui.aggrid({
            'columnDefs': [
                {'headerName': 'Name', 'field': 'series_name'},
                {'headerName': 'Chapter', 'field': 'ch_n'},
                {'headerName': 'Volume', 'field': 'vol_n'},
                {'headerName': 'Title', 'field': 'title'},
            ],
            'rowData': [{"series_name":series.title,
                     "ch_n":chapter.number,
                     "vol_n":chapter.volume,
                     "title":chapter.title}
                    for chapter in md_data],
            'rowSelection': 'multiple',
        }).style('width: 400px; height: 800px')


# ui.button('Update', on_click=update)
# ui.button('Select all', on_click=lambda: grid.run_grid_method('selectAll'))
# ui.button('Show parent', on_click=lambda: grid.run_column_method('setColumnVisible', 'parent', True))

