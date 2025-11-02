from pydantic import BaseModel, Field
from typing_extensions import Optional

class OutputFormat(BaseModel):
    step: str = Field(
        ...,
        title="step",
        description="Field denoting the current step type of the model eg- START, PLAN, TOOL_CALL, TOOL_OUTPUT, RESULT",
    )
    content: Optional[str] = Field(
        None,
        title="content",
        description="The optional string content for the step",
    )
    tool_name: Optional[str] = Field(
        None,
        title="tool_name",
        description="The optional string name of the tool used in the step",
    )
    tool_input: Optional[str] = Field(
        None,
        title="tool_input",
        description="The optional string input of the tool used in the step",
    )
    tool_output: Optional[str] = Field(
        None,
        title="tool_output",
        description="The optional string output of the tool used in the step",
    )
