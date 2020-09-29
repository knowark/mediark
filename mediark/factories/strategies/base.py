base = {
    # Query parser
    "QueryParser": {
        "method": "query_parser"
    },
    # Providers
    "AuthProvider": {
        "method": "standard_auth_provider"
    },
    "TenantProvider": {
        "method": "standard_tenant_provider"
    },
    # Suppliers
    "TenantSupplier": {
        "method": "memory_tenant_supplier"
    },
    "MigrationSupplier": {
        "method": "memory_migration_supplier"
    },
    # Repositories
    "MediaRepository": {
        "method": "memory_media_repository",
    },
    # Managers
    "TransactionManager": {
        "method": "memory_transaction_manager",
    },
    "SessionManager": {
        "method": "session_manager"
    },
    "MediaStorageManager": {
        "method": "media_storage_manager",
    },
    # Informers
    "MediarkInformer": {
        "method": "standard_mediark_informer",
    },
    "FileInformer": {
        "method": "standard_file_informer",
    },
    # Services
    "IdService": {
        "method": "standard_id_service"
    },
    "FileStoreService": {
        "method": "memory_file_store_service"
    }
}
