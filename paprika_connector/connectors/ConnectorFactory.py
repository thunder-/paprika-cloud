class ConnectorFactory:
    def __init__(self):
        pass

    @staticmethod
    def create_connector(datasource):
        if datasource['type'] == 'mysql':
            from paprika_connector.connectors.MysqlConnector import MysqlConnector
            return MysqlConnector(datasource)
        if datasource['type'] == 'oracle':
            from paprika_connector.connectors.OracleConnector import OracleConnector
            return OracleConnector(datasource)
