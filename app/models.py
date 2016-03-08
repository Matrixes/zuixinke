#-*- coding:utf-8 -*-

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from markdown import markdown
from flask import current_app, request
from flask.ext.login import UserMixin
from . import db, login_manager
import bleach

class User(UserMixin,db.Model):
	__tablename__="users"
	id = db.Column(db.Integer,primary_key=True)
	email = db.Column(db.String(64),unique=True)
	username = db.Column(db.String(64),unique=True,index=True)
	password_hash = db.Column(db.String(128))
	confirmed = db.Column(db.Boolean,default=False)
	name = db.Column(db.String(64))
	location = db.Column(db.String(64))
	about_me = db.Column(db.Text())
	member_since = db.Column(db.DateTime(), default=datetime.now)
	last_seen = db.Column(db.DateTime(), default=datetime.now)
	avatar_hash = db.Column(db.String(32))

	posts = db.relationship('Post', backref='author', lazy='dynamic')


	@property
	def password(self):
		raise AttributeError('password is not a readable attribute！')

	@password.setter
	def password(self,password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.id})

	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('confirm') != self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		db.session.commit()
		return True

	def generate_reset_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'reset': self.id})

	def reset_password(self, token, new_password):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('reset') != self.id:
			return False
		self.password = new_password
		db.session.add(self)
		db.session.commit()
		return True

	def generate_email_change_token(self, new_email, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'change_email': self.id, 'new_email': new_email})

	def change_email(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token)
		except:
			return False
		if data.get('change_email') != self.id:
			return False
		new_email = data.get('new_email')
		if new_email is None:
			return False
		if self.query.filter_by(email=new_email).first() is not None:
			return False
		self.email = new_email
		#self.avatar_hash = hashlib.md5(
		#	self.email.encode('utf-8')).hexdigest()
		db.session.add(self)
		db.session.commit()
		return True

	def ping(self):
		self.last_seen = datetime.now()
		db.session.add(self)

	def gravatar(self, size=100, default='identicon', rating='g'):
		if request.is_secure:
			url = 'https://secure.gravatar.com/avatar'
		else:
			url = 'http://www.gravatar.com/avatar'
		hash = self.avatar_hash or hashlib.md5(
			 self.email.encode('utf-8')).hexdigest()
		return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)
	

	def __repr__(self):
		return self.username


class Category(db.Model):
	__tablename__="categories"
	id = db.Column(db.Integer,primary_key=True)
	tag = db.Column(db.String(64),unique=True)
	posts = db.relationship("Post", backref="category", lazy='dynamic')



class Post(db.Model):
	__tablename__="posts"
	id = db.Column(db.Integer,primary_key=True)
	title = db.Column(db.String(64))
	summary=db.Column(db.Text)
	summary_html=db.Column(db.Text)
	body = db.Column(db.Text)
	body_html = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))


	@staticmethod
	def on_changed_summary(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code','br','img','span','hr',
						'blockquote','em', 'i','strong','li','ol','button',
						'pre','strong','ul','h1','h2','h3','h4','h5','h6','p']

		allowed_styles = [
			'font','font-size','font-wight','background-color','border',
            'text-indent','padding','margin','color','background','float',
            'width','height','display'
		]


		allowed_attriutes = {
			'a':['href','title'],
			'img':['src','alt'],
            '*':['class','style']
		}
		target.summary_html = bleach.linkify(bleach.clean(
			markdown(value, output_format='html'),
			tags=allowed_tags,
			attributes=allowed_attriutes,
			styles=allowed_styles,
			strip=True))



	@staticmethod
	def on_changed_body(target, value, oldvalue, initiator):
		allowed_tags = ['a', 'abbr', 'acronym', 'b', 'code','br','img','span','hr',
							'blockquote','em', 'i','strong','li','ol','button'
							'pre','strong','ul','h1','h2','h3','h4','h5','h6','p']

		allowed_styles = [
			'font','font-size','font-wight','background-color','border',
            'text-indent','padding','margin','color','background','float',
            'width','height','display'
		]


		allowed_attriutes = {
			'a':['href','title','class'],
			'img':['src','alt'],
            '*':['class','style']
		}

		target.body_html = bleach.linkify(bleach.clean(
			markdown(value, output_format='html'),
			tags=allowed_tags,
			attributes=allowed_attriutes,
			styles=allowed_styles,
			strip=True))

        		


db.event.listen(Post.summary, 'set', Post.on_changed_summary)
db.event.listen(Post.body, 'set', Post.on_changed_body)



#class Like(db.Model):
	#__tablename__="Like"
	#id=db.Column(db.Integer,primary_key=True)
	#like_count=db.Column(db.Integer)

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))