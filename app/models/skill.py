from sqlmodel import SQLModel, Field, Relationship


class SkillBase(SQLModel):
    id: int = Field(primary_key=True, nullable=False)
    tag: str | None
    description: str | None


class Skill(SkillBase, table=True):
    category_id: int = Field(foreign_key='skillcategory.id')
    category: 'SkillCategory' = Relationship(back_populates='skills')
