import inspect
from injectark import Injectark
from mediark.integration.core.common import config
from mediark.integration.factories import factory_builder


test_tuples = [
    ('BaseFactory', [
        ('AuthProvider', 'StandardAuthProvider'),
        ('TenantProvider', 'StandardTenantProvider'),
        # general
        ('Connector', 'MemoryConnector'),
        ('Transactor', 'MemoryTransactor'),
        #suppliers
        ('TenantSupplier', 'MemoryTenantSupplier'),
        ('MigrationSupplier', 'MemoryMigrationSupplier'),
        ('EmailSupplier', 'MemoryEmailSupplier'),
        ('PlanSupplier', 'MemoryPlanSupplier'),
        #repositories
        ('MediaRepository', 'MemoryMediaRepository'),
        ('EmailRepository', 'MemoryEmailRepository'),
        #service
        ('IdService', 'StandardIdService'),
        ('FileStoreService', 'MemoryFileStoreService'),
        #managers
        ('SessionManager', 'SessionManager'),
        ('MediaStorageManager', 'MediaStorageManager'),
        ('EmailManager', 'EmailManager'),
        ('SetupManager', 'SetupManager'),
        #informers
        ('FileInformer', 'StandardFileInformer'),
        ('StandardInformer', 'StandardInformer'),
    ]),
    ('CheckFactory', [
        ('TenantSupplier', 'MemoryTenantSupplier'),
        ('MediaRepository', 'MemoryMediaRepository'),
        ('EmailRepository', 'MemoryEmailRepository'),
    ]),
    ('CloudFactory', [
        ('SwiftAuthSupplier', 'SwiftAuthSupplier'),
        ('FileStoreService', 'SwiftFileStoreService'),
        ('EmailSupplier', 'HttpEmailSupplier'),
    ]),
    ('DirectoryFactory', [
        ('FileStoreService', 'DirectoryFileStoreService'),
        ('EmailSupplier', 'ConsoleEmailSupplier'),
    ]),
    ('HttpFactory', [
        ('StandardInformer', 'HttpMediarkInformer'),
        ('HttpClientSupplier', 'HttpClientSupplier'),
    ]),
    ('SqlFactory', [
        ('SqlParser', 'SqlParser'),
        ('Connector', 'SqlConnector'),
        ('Transactor', 'SqlTransactor'),
        ('MediaRepository', 'SqlMediaRepository'),
        ('EmailRepository', 'SqlEmailRepository'),
        ('TenantSupplier', 'SchemaTenantSupplier'),
        ('MigrationSupplier', 'SchemaMigrationSupplier'),
        ('PlanSupplier', 'SqlPlanSupplier'),
    ]),
]


def test_factories():
    for factory_name, dependencies in test_tuples:
        factory = factory_builder.build(config, name=factory_name)

        injector = Injectark(factory=factory)

        for abstract, concrete in dependencies:
            result = injector.resolve(abstract)
            assert type(result).__name__ == concrete
