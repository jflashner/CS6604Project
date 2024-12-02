# Create PyDantic classes to represent the DebateGraph
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class ArgumentEntity(BaseModel):
    id: int
    side: Optional[str] = None
    type: str = "argument"
    content: str

class Relationship(BaseModel):
    source_id: int
    target_id: int
    relationship_type: str = Field(..., description="Relationship types: [claim, premise, conclusion, first principle, rebuttal]")

class DebateGraph(BaseModel):
    entities: List[ArgumentEntity]
    relationships: List[Relationship]

# Create an example Debate Graph for prompting
main_claim = ArgumentEntity(
    id=1,
    content="Climate change poses a serious threat to global ecosystems and human society"
)

supporting_premise1 = ArgumentEntity(
    id=2,
    content="Global temperatures have risen by approximately 1°C since pre-industrial times"
)

supporting_premise2 = ArgumentEntity(
    id=3,
    content="Rising temperatures are primarily caused by human greenhouse gas emissions"
)

conclusion = ArgumentEntity(
    id=4,
    content="Immediate action is required to reduce greenhouse gas emissions"
)

rebuttal = ArgumentEntity(
    id=5,
    content="Natural climate cycles have caused temperature variations throughout Earth's history"
)

first_principle = ArgumentEntity(
    id=6,
    content="Scientific measurements and data provide reliable evidence for understanding climate patterns"
)

# Create relationships between arguments
relationships = [
    Relationship(
        source_id=supporting_premise1.id,
        target_id=main_claim.id,
        relationship_type="premise"
    ),
    Relationship(
        source_id=supporting_premise2.id,
        target_id=main_claim.id,
        relationship_type="premise"
    ),
    Relationship(
        source_id=main_claim.id,
        target_id=conclusion.id,
        relationship_type="claim"
    ),
    Relationship(
        source_id=rebuttal.id,
        target_id=supporting_premise2.id,
        relationship_type="rebuttal"
    ),
    Relationship(
        source_id=first_principle.id,
        target_id=supporting_premise1.id,
        relationship_type="first principle"
    )
]

# Create the debate graph
debate_graph = DebateGraph(
    entities=[main_claim, supporting_premise1, supporting_premise2, conclusion, rebuttal, first_principle],
    relationships=relationships
)

# Dump the JSON representation
example_graph = debate_graph.model_dump_json(indent=2)
