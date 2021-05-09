from fastapi import FastAPI, Depends, status, HTTPException
import schemas, models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(blogdata: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=blogdata.title, body=blogdata.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    if not new_blog:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Enabled to create blog")
    return new_blog


@app.put('/blog/{id}', status_code=status.HTTP_200_OK)
def update_blog(id, editData: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail="No blog found for update")

    blog.update(editData.dict(), synchronize_session=False)
    db.commit()
    return {"msg": "Blog updated successfully"}


@app.delete('/blog/{id}', status_code=status.HTTP_200_OK)
def delete_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail="No blog found for delete")
    blog.delete()
    db.commit()
    return {"msg": "Blog deleted"}


@app.get("/blog")
async def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="No blogs found")
    return blogs


@app.get("/blog/{id}")
def get_blog(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail="No blog detail found")
    return blog