json = {
    "ImageRepository": {
        "method": "json_image_repository",
    },
    "AudioRepository": {
        "method": "json_audio_repository",
    },
    "ImageFileStoreService": {
        "method": "directory_image_file_store_service"
    },
    "AudioFileStoreService": {
        "method": "directory_audio_file_store_service"
    },

    # Tenancy
    "TenantProvider": {
        "method": "standard_tenant_provider"
    },

    "TenantSupplier": {
        "method": "json_tenant_supplier"
    },
}
