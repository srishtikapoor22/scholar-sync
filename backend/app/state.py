from pydantic import BaseModel
from typing import TypedDict, List,Optional
from typing import Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class Claim(BaseModel):
    text: str
    page_label: str
    category: str
    audit_result: Optional[str]=None

class AuditState(TypedDict):
    pdf_content: str
    claims: List[Claim]
    messages: Annotated[Sequence[BaseMessage], add_messages]
    search_performed: bool