from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Event:
    name: str
    link: str
    time: Optional[datetime] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    venue: Optional[str] = None
    description: Optional[str] = None

    def __str__(self):
        time_parts = []
        if self.time:
            time_parts.append(f"on {self.time.strftime('%Y-%m-%d')}")
        if self.start_time:
            time_parts.append(f"from {self.start_time}")
        if self.end_time:
            time_parts.append(f"to {self.end_time}")

        time_str = " ".join(time_parts) if time_parts else "time not specified"

        return f"Event: {self.name} {time_str}"

    def to_dict(self):
        return {
            "name": self.name,
            "time": self.time.isoformat() if self.time else None,
            "link": self.link,
            "start_time": self.start_time if self.start_time else None,
            "end_time": self.end_time if self.end_time else None,
            "venue": self.venue if self.venue else None,
            "description": self.description if self.description else None
        }

    def get_time_info(self) -> str:
        if self.time:
            return self.time.strftime('%Y-%m-%d')
        elif self.start_time:
            return self.start_time.split('|')[0].strip()
        else:
            return "Unknown date"
