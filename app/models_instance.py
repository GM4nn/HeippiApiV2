from flask_sqlalchemy import SQLAlchemy,BaseQuery
from werkzeug.security import generate_password_hash,check_password_hash,safe_str_cmp

class exSql():
    db = SQLAlchemy(session_options={'query_cls': BaseQuery})
    genera_hash = generate_password_hash
    check_password = check_password_hash
    safe_str_cmp = safe_str_cmp

