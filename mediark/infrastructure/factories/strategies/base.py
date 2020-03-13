base = {
    # Security
    "AuthProvider": {
        "method": "standard_auth_provider"
    },
    "SessionCoordinator": {
        "method": "session_coordinator"
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
    "SetupSupplier": {
        "method": "memory_setup_supplier"
    },
    "TransactionManager": {
        "method": "memory_transaction_manager",
    },
    "MediaRepository": {
        "method": "memory_media_repository",
    },
    "ImageRepository": {
        "method": "memory_image_repository",
    },
    "MediaStorageCoordinator": {
        "method": "media_storage_coordinator",
    },
    "ImageStorageCoordinator": {
        "method": "image_storage_coordinator",
    },
    "AudioRepository": {
        "method": "memory_audio_repository",
    },
    "AudioStorageCoordinator": {
        "method": "audio_storage_coordinator",
    },
    "MediarkReporter": {
        "method": "standard_mediark_reporter",
    },
    "FileReporter": {
        "method": "standard_file_reporter",
    },
    "FileStoreService": {
        "method": "memory_file_store_service"
    }
}
