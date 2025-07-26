from typing import Annotated

from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState


@tool
def reddit_tool(state: Annotated[dict, InjectedState]) -> str:
	"""Tool to retrieve data from Reddit posts"""
	return f"Took me 1.5 hours to move 500 meters in Marathahalli! The drainage system is working its magic again after one sharp spell of rain. Please tell me its wfh tomorrow. #RainyDay"


@tool
def google_news_tool(state: Annotated[dict, InjectedState]) -> str:
	"""Tool to retrieve data from Google News posts"""
	return f"Heavy water logging reported at Marathahalli underpass on Outer Ring Road due to incessant rains. Traffic movement is severely affected. Commuters are advised to avoid this stretch and use alternative routes."

@tool
def twitter_tool(state: Annotated[dict, InjectedState]) -> str:
	"""Tool to retrieve data from Twitter posts"""
	return f"Marathahalli underpass is a swimming pool right now. Literally haven't moved in 45 minutes. Avoid ORR at all costs! Unbelievable that this happens after EVERY heavy rain. @BBMPCOMM @BlrCityPolice what are you guys doing? #BangaloreRains #Marathahalli #ORR"

@tool
def local_data_tool(state: Annotated[dict, InjectedState]) -> str:
	"""Tool to retrieve data from Local data posts from the A-Live Grid app"""
	return f"Terrible water logging in ORR marathahalli near kalamandir, dont take this route ppl"


