from typing import Optional
from xml.etree import ElementTree as ET

def parse_publication_date(pub_date_node: Optional[ET.Element]) -> str:
    if pub_date_node is None:
        return ""
    year = pub_date_node.findtext("Year")
    month = pub_date_node.findtext("Month")
    day = pub_date_node.findtext("Day")
    month_map = {
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
        "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
    }
    if year:
        date = year
        if month:
            month_num = month_map.get(month[:3], month)
            date += f"-{month_num}"
            if day and day.isdigit():
                date += f"-{int(day):02}"
        return date
    return ""
