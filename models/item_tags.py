from db import db


items_tags = db.Table(
    "items_tags",
    db.metadata,
    db.Column("item_id", db.Integer, db.ForeignKey("item.id")),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")),
)
