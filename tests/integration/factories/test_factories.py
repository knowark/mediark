import inspect
from injectark import Injectark
from mediark.integration.core.common import config
from mediark.integration.factories import factory_builder


test_tuples = [
    ('BaseFactory', [
        ('QueryParser', 'QueryParser'),
        ('AuthProvider', 'StandardAuthProvider'),
        ('TenantProvider', 'StandardTenantProvider'),
        ('MediaRepository', 'MemoryMediaRepository'),
        ('IdService', 'StandardIdService'),
        ('FileStoreService', 'MemoryFileStoreService'),
        ('TransactionManager', 'MemoryTransactionManager'),
        ('SessionManager', 'SessionManager'),
        ('MediaStorageManager', 'MediaStorageManager'),
        ('FileInformer', 'StandardFileInformer'),
        ('MediarkInformer', 'StandardMediarkInformer'),
        ('TenantSupplier', 'MemoryTenantSupplier'),
        ('MigrationSupplier', 'MemoryMigrationSupplier'),
    ]),
    ('CheckFactory', [
        ('TenantSupplier', 'MemoryTenantSupplier'),
        ('MediaRepository', 'MemoryMediaRepository'),
    ]),
    ('CloudFactory', [
        ('SwiftAuthSupplier', 'SwiftAuthSupplier'),
        ('FileStoreService', 'SwiftFileStoreService'),
    ]),
    ('DirectoryFactory', [
        ('FileStoreService', 'DirectoryFileStoreService'),
    ]),
    ('HttpFactory', [
        ('MediarkInformer', 'HttpMediarkInformer'),
        ('HttpClientSupplier', 'HttpClientSupplier'),
    ]),
    ('SqlFactory', [
        ('QueryParser', 'SqlParser'),
        ('ConnectionManager', 'DefaultConnectionManager'),
        ('TransactionManager', 'SqlTransactionManager'),
        ('MediaRepository', 'SqlMediaRepository'),
        ('TenantSupplier', 'SchemaTenantSupplier'),
        ('MigrationSupplier', 'SchemaMigrationSupplier'),
    ]),
]


def test_factories():
    for factory_name, dependencies in test_tuples:
        factory = factory_builder.build(config, name=factory_name)

        injector = Injectark(factory=factory)

        for abstract, concrete in dependencies:
            result = injector.resolve(abstract)
            assert type(result).__name__ == concrete
