from pydantic import BaseModel
from typing import TypedDict, List,Optional
from typing import Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import Field

class Claim(BaseModel):
    text: str
    page_label: str
    category: str
    audit_result: Optional[str]=None
    is_time_sensitive: bool=Field(
        default=True,
        description="STRICT RULE: Set to FALSE for CS fundamentals (Linked Lists, Binary Search, Big O). "
                "Set to TRUE ONLY for specific software versions, APIs, or hardware (React 19, CUDA, H100)."
    )

class AuditState(TypedDict):
    pdf_content: str
    claims: List[Claim]
    messages: Annotated[Sequence[BaseMessage], add_messages]
    search_performed: bool