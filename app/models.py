from app import db
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.search import add_to_index, remove_from_index, query_index

class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(clscls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.tablenama__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


engine = create_engine('postgresql://[username]:[password]@localhost/[path]', convert_unicode=True, echo=False)
Base = declarative_base()
metadata = Base.metadata


class Artobject(SearchableMixin, db.Model, Base):
    __tablename__ = '[nameOfTable in postgresql database]'
    __searchable__ = ['title', 'material', 'type', 'artist', 'location']

    #columns in table 
    id = Column(Integer, primary_key=True)
    title = Column(String)
    material = Column(String)
    type = Column(String)
    artist = Column(String)
    location = Column(String)
    url = Column(String)


    def __repr__(self):
        return '<Artobject {}>'.format(self.id, self.title, self.material, self.type, self.artist, self.location)




