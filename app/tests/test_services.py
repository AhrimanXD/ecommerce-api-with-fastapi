from app.services import product_services
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import pytest
from app.db.database import Base
from app.schemas.products import ProductCreate
from app.models.products import Product




@pytest.fixture
def database():
  TEST_DATABASE_URL = 'sqlite:///:memory:'
  engine = create_engine(TEST_DATABASE_URL, connect_args = {"check_same_thread": False})

  Base.metadata.create_all(bind = engine)

  TestSessionLocal = sessionmaker(bind=engine, autocommit = False, autoflush = False)
  return TestSessionLocal

@pytest.fixture
def session(database):
  session = database()
  try:
    yield session
  finally:
    session.close()

@pytest.fixture
def test_product_input():
  input = ProductCreate(name = "Test Product",
                            description = "A description",
                            category_id = 1,
                            price = 10.0,
                            stock = 300,
                            size = 10,
                            unit = 'kg'
                            )
  return input


class TestProductServices:
  def test_create_product(self, session, test_product_input):
    product = product_services.create_product(test_product_input, session)
    
    assert product.name == "Test Product" and product.price == 10.0 and product.stock == 300

  def test_create_duplicate_product(self, session, test_product_input):
    product = product_services.create_product(test_product_input, session)
    with pytest.raises(Exception):
      product_services.create_product(test_product_input, session)

class TestCartServices:
  def test_add_to_cart(self):
    pass