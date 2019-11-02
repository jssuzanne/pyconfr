# noqa: flake8

import pytest


@pytest.mark.usefixtures('rollback_registry')
class TestProduct:

    def test_create_new_product(self, rollback_registry):
        rollback_registry.LMC.Product.insert(
            label="A product label",
            code="A product code",
        )
        assert rollback_registry.Product.query().count() == 1
        assert (
            rollback_registry.Product.query().one().code ==
            "A product code"
        )


from anyblok import Declarations
from anyblok.column import String, Integer


@Declarations.register(Declarations.Model.LMC, tablename="ProdDef")
class Product:

    id = Integer(primary_key=True, db_column_name="IDD")
    code = String(nullable=False, index=True, db_column_name="Attr1")
    label = String(nullable=False, db_column_name="Display")


from anyblok import Declarations
from anyblok.column import String, Integer


@Declarations.register(Declarations.Model.LMC)
class Product:

    id = Integer(primary_key=True)
    code = String(nullable=False, index=True)
    label = String(nullable=False)


from anyblok import Declarations
from anyblok.column import String, Integer


@Declarations.register(Declarations.Model.LMC, tablename="ProdDef")
class Product:
    __db_schema__ = "Lens"

    id = Integer(primary_key=True, db_column_name="IDD")
    code = String(nullable=False, index=True, db_column_name="Attr1")
    label = String(nullable=False, db_column_name="Display")



import pytest


@pytest.mark.usefixtures('rollback_registry')
class TestApiProduct:

    def test_addresses_post(self, rollback_registry, webserver):
        response = webserver.post_json('/api/v1/lmc/products',
                                       [{'code': 'C1', 'label': 'My product'}])
        assert response.status_code == 200
        assert response.json_body[0].get('code') == 'C1'
        assert rollback_registry.LMC.Product.query().filter_by(code='C1').one()

    def test_addresses_get(self, rollback_registry, webserver):
        """Address GET /api/v1/addresses"""
        rollback_registry.LMC.Product.insert(
            code="C1", label="My product")
        response = webserver.get('/api/v1/lmc/products')
        assert response.status_code == 200
        assert len(response.json_body) == 1
        assert response.json_body[0].get('code') == 'C1'



from anyblok_pyramid_rest_api.crud_resource import (
    CrudResource, resource)


@resource(
    collection_path='/api/v1/lmc/products',
    path='/api/v1/lmc/products/{id}',
    installed_blok=current_blok()
)
class LensProductResource(CrudResource):
    model = "Model.LMC.Product"



[AnyBlok]
db_schema.Model.LMC.*=Common
db_schema.Model.LMC.Product=Lense



