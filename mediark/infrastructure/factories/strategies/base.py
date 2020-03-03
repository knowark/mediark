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
    "TransactionManager": {
        "method": "memory_transaction_manager",
    },

    "ImageFileStoreService": {
        "method": "memory_image_file_store_service"
    },
    "ImageRepository": {
        "method": "memory_image_repository",
    },
    "ImageStorageCoordinator": {
        "method": "image_storage_coordinator",
    },
    "AudioFileStoreService": {
        "method": "memory_audio_file_store_service"
    },
    "AudioRepository": {
        "method": "memory_audio_repository",
    },
    "AudioStorageCoordinator": {
        "method": "audio_storage_coordinator",
    },
    "MediarkReporter": {
        "method": "memory_mediark_reporter",
    },
    "DirectoryLoadSupplier": {
        "method": "directory_load_supplier"
    },
    "MediarkReporter": {
        "method": "memory_mediark_reporter",
    },
}
