base = {
    # Security
    "AuthProvider": {
        "method": "standard_auth_provider"
    },
    "SessionManager": {
        "method": "session_manager"
    },
    # Query parser
    "QueryParser": {
        "method": "query_parser"
    },
    "IdService": {
        "method": "standard_id_service"
    },
    "AuthProvider": {
        "method": "standard_auth_provider"
    },
    # Tenancy
    "TenantProvider": {
        "method": "standard_tenant_provider"
    },
    "TenantSupplier": {
        "method": "memory_tenant_supplier"
    },
    "MigrationSupplier": {
        "method": "memory_migration_supplier"
    },
    "TransactionManager": {
        "method": "memory_transaction_manager",
    },
    "MediaRepository": {
        "method": "memory_media_repository",
    },
    "MediaStorageManager": {
        "method": "media_storage_manager",
    },
    "MediarkInformer": {
        "method": "standard_mediark_informer",
    },
    "FileInformer": {
        "method": "standard_file_informer",
    },
    "FileStoreService": {
        "method": "memory_file_store_service"
    }
}
