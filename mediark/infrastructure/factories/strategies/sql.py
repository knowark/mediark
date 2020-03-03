sql = {
    # Parser
    "SqlParser": {
        "method": "sql_query_parser"
    },

    # Connections
    "ConnectionManager": {
        "method": "sql_connection_manager",
    },

    "TransactionManager": {
        "method": "sql_transaction_manager",
    },


    # Repositories
    "ImageRepository": {
        "method": "sql_image_repository",
    },
    "AudioRepository": {
        "method": "sql_audio_repository",
    },
    "TenantSupplier": {
        "method": "schema_tenant_supplier"
    },
}
