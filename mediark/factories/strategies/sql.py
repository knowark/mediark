sql = {
    # Parser
    "SqlParser": {
        "method": "sql_query_parser"
    },

    # Managers
    "ConnectionManager": {
        "method": "sql_connection_manager",
    },
    "TransactionManager": {
        "method": "sql_transaction_manager",
    },

    # Repositories
    "MediaRepository": {
        "method": "sql_media_repository",
    },

    # Suppliers
    "TenantSupplier": {
        "method": "schema_tenant_supplier"
    },
    "MigrationSupplier": {
        "method": "schema_migration_supplier"
    }
}
