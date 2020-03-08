from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from data_types.notes.topic import Topic
from common import NEW_LINE

NOTE_SEP = NEW_LINE + ' ---' + NEW_LINE
TOPICS_SEP = ','


@dataclass
class Note:
    value: str
    creation_date: datetime = None
    modification_date: datetime = None
    name: Optional[str] = None
    keywords: Optional[str] = None
    topics: Optional[List[Topic]] = None

    def to_str(self) -> str:
        return NOTE_SEP.join([self.name, self.value, ','.join(self.topics)])

    def from_str(self, raw_note: str) -> 'Note':
        splitted_note = raw_note.split(NOTE_SEP)
        name = splitted_note[0]
        value = splitted_note[1]
        topics = splitted_note[2].split(TOPICS_SEP)
        return Note(value, name=name, topics=topics)

    @classmethod
    def get_default(cls):
        return Note('', name='', topics=[])


