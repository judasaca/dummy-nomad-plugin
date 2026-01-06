from pydantic import BaseModel, Field


class BaseWorkflowInput(BaseModel):
    """Base input model for workflows"""

    # upload_id: str = Field(
    #    ...,
    #    description='Unique identifier for the upload associated with the workflow.',
    # )
    user_id: str = Field(
        ..., description='Unique identifier for the user who initiated the workflow.'
    )


class ExampleWorkflowInput(BaseWorkflowInput):
    """Input model for the workflow"""

    cid: int = Field(
        ..., description='PubChem compound identifier for a chemical compound.'
    )


class GetRequestInput(BaseWorkflowInput):
    """Input model for the activity"""

    iterations: int = Field(..., description='Timeout for the request.')
