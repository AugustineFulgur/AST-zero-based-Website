class MyRouter(object):
    def db_for_read(self, model, **hints):
        if hasattr(model, '_database'):
            return model._database
        return 'default'
 
    def db_for_write(self, model, **hints):
        if hasattr(model, '_database'):
            return model._database
        return  'default'
 
    def allow_relation(self, obj1, obj2, **hints):
 
        return None
 
    def allow_syncdb(self, db, model):
        if hasattr(model, '_database'):
            model_db = model._database
        else:
            model_db = 'default'
            
        if db == model_db:
            return True
        else:
            return False