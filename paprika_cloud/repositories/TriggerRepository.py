from paprika_connector.connectors.Repository import Repository
from paprika_connector.connectors.Helper import Helper
from datetime import datetime


class TriggerRepository(Repository):
    def __init__(self, connector):
        Repository.__init__(self, connector)

    def list(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = {}

        statement = "select tgr.*, get_trigger_type(tte_id) as tte from triggers tgr where active=1 order by name"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return []
        return result


    def list_hooks(self):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = {}

        statement = "select tgr.*, get_trigger_type(tte_id) as tte from triggers tgr where active=1 and get_trigger_type(tte_id)='hook' order by name"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return []
        return result

    def insert(self, trigger):
        connection = self.get_connection()
        cursor = connection.cursor()

        now = datetime.now()
        connector = self.get_connector()
        ds = connector.get_datasource()

        params = dict()
        params['name'] = trigger.get('name')
        params['description'] = trigger.get('description')
        params['datasource'] = trigger.get('datasource')
        params['selector'] = trigger.get('selector')
        params['updater'] = trigger.get('updater')
        params['options'] = trigger.get('options')
        params['tte_id'] = trigger.get('tte_id')
        params['repetition'] = trigger.get('repetition')
        params['intermission'] = trigger.get('intermission')
        params['expected'] = trigger.get('expected')
        params['url'] = trigger.get('url')
        params['patterns'] = trigger.get('patterns')
        params['recursive'] = trigger.get('recursive')
        params['depth'] = trigger.get('depth')
        params['username'] = trigger.get('username')
        params['password'] = trigger.get('password')
        params['created_at'] = now
        params['created_by'] = ds['username']
        params['updated_at'] = now
        params['updated_by'] = ds['username']

        statement = "insert into triggers" \
                    "  (name, " \
                    "   description, " \
                    "   datasource, " \
                    "   tte_id, " \
                    "   selector, " \
                    "   updater, " \
                    "   options, " \
                    "   repetition, " \
                    "   intermission, " \
                    "   expected, " \
                    "   url, " \
                    "   patterns, " \
                    "   recursive, " \
                    "   depth, " \
                    "   username, " \
                    "   password, " \
                    "   created_at, " \
                    "   created_by, " \
                    "   updated_at, " \
                    "   updated_by) " \
                    "values " \
                    "  (:name, " \
                    "   :description, " \
                    "   :datasource, " \
                    "   :tte_id, " \
                    "   :selector, " \
                    "   :updater, " \
                    "   :options, " \
                    "   :repetition, " \
                    "   :intermission, " \
                    "   :expected, " \
                    "   :url, " \
                    "   :patterns, " \
                    "   :recursive, " \
                    "   :depth, " \
                    "   :username, " \
                    "   :password, " \
                    "   :created_at, " \
                    "   :created_by, " \
                    "   :updated_at, " \
                    "   :updated_by)"
        statement, parameters = self.statement(statement, params)
        cursor.execute(statement, parameters)
        trigger['id'] = cursor.lastrowid
        connection.commit()
        return trigger

    def update(self, trigger):
        connection = self.get_connection()
        cursor = connection.cursor()

        now = datetime.now()
        connector = self.get_connector()
        ds = connector.get_datasource()

        params = dict()
        params['hashcode'] = trigger.get('hashcode')
        params['name'] = trigger.get('name')
        params['description'] = trigger.get('description')
        params['datasource'] = trigger.get('datasource')
        params['selector'] = trigger.get('selector')
        params['updater'] = trigger.get('updater')
        params['options'] = trigger.get('options')
        params['tte_id'] = trigger.get('tte_id')
        params['repetition'] = trigger.get('repetition')
        params['intermission'] = trigger.get('intermission')
        params['expected'] = trigger.get('expected')
        params['url'] = trigger.get('url')
        params['patterns'] = trigger.get('patterns')
        params['recursive'] = trigger.get('recursive')
        params['depth'] = trigger.get('depth')
        params['username'] = trigger.get('username')
        params['password'] = trigger.get('password')
        params['updated_at'] = now
        params['updated_by'] = ds['username']

        statement = "update triggers set " \
                    "   name=:name, " \
                    "   description=:description, " \
                    "   datasource=:datasource, " \
                    "   selector=:selector, " \
                    "   updater=:updater, " \
                    "   options=:options, " \
                    "   repetition=:repetition, " \
                    "   intermission=:intermission, " \
                    "   expected=:expected, " \
                    "   url=:url, " \
                    "   patterns=:patterns, " \
                    "   recursive=:recursive, " \
                    "   depth=:depth, " \
                    "   username=:username, " \
                    "   password=:password" \
                    " where hashcode=:hashcode"
        statement, parameters = self.statement(statement, params)
        print statement, parameters
        cursor.execute(statement, parameters)
        connection.commit()

    def find_by_hashcode(self, hashcode):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = {}
        params['hashcode'] = hashcode

        statement = "select * from triggers where hashcode=:hashcode and active=1"
        statement, parameters = self.statement(statement, params)

        cursor.execute(statement, parameters)
        result = Helper.cursor_to_json(cursor)
        if len(result) == 0:
            return None
        return result[0]

    def disable(self, hashcode):
        connection = self.get_connection()
        cursor = connection.cursor()

        params = {}
        params['hashcode'] = hashcode

        statement = "update triggers set active=0 where hashcode=:hashcode"
        statement, parameters = self.statement(statement, params)
        cursor.execute(statement, parameters)
        connection.commit()

